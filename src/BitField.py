#!/usr/bin/env python
#
# @file    BitField.py
# @brief   Single bit fields
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 12:34
#
# Copyright (C) 2009, 2010 Aleix Conchillo Flaque
#
# This file is part of BitPacket.
#
# BitPacket is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitPacket is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BitPacket.  If not, see <http://www.gnu.org/licenses/>.
#

__doc__ = '''

    Single bit fields
    =================

    **API reference**: :class:`BitField`

    A packet might be formed by multiple fields that can be single bit
    fields, numeric fields, etc. Sometimes, byte-aligned fields are
    formed by bit fields internally. The purpose of :mod:`BitField` is
    to provide these single bit fields that, at the end, will be used
    to form byte-aligned fields.

    For example, the first byte of the IP header is:

    +---------+---------+
    | version |  hlen   |
    +=========+=========+
    | 4 bits  | 4 bits  |
    +---------+---------+

    That is, a byte formed by two nibbles. The first nibble,
    *version*, can be constructed by the following piece of code:

    >>> bf = BitField('version', 4, 15)
    >>> print bf
    (version = 0x0F)

    That is, a 4 bits field with a default, optional, value 15.


    Assigning bytes
    ---------------

    The main purpose of :mod:`BitField` is to work together with
    :mod:`BitStructure` to form byte-aligned fields. When used with
    :mod:`BitStructure` the :func:`BitField.binary` and
    :func:`BitField.set_binary` functions are used, which allow
    working with bit strings (i.e. a string with 0 and 1). However, as
    a :mod:`Field` subclass, a byte string can still be set to a
    :mod:`BitField`. Two special considerations need to be taken into
    account:

      - The MSB bit of the given byte string will also be the MSB of
        the :mod:`BitField`.
      - When a byte string is returned from a :mod:`BitField`, the
        byte string will be byte-aligned. This means that the last
        byte could have bit zero-padding.

    Following the example above, we can assign a byte array to the
    *version* field:

    >>> data = array.array('B', [0x34])
    >>> bf.set_array(data)
    >>> print bf
    (version = 0x03)

    As a consequence of the first rule, we see that only the first
    four MSB have been used. Now, if we ask for this BitField array:

    >>> data = array.array('B')
    >>> bf.array(data)
    >>> print "0x%02X" % data[0]
    0x30

    we can see, because of the second rule, that the second nibble is
    padded with zeros. Again, this is because the *version* field is
    not byte-aligned. For these two reasons, :mod:`BitField` needs to
    be used with :mod:`BitStructure` to form byte-aligned fields.

'''

import array

from utils.binary import bin_to_int, int_to_bin
from utils.binary import byte_end, encode_bin, decode_bin
from utils.stream import read_stream, write_stream
from utils.string import hex_string

from Field import Field

class BitField(Field):
    '''
    This class represents bit fields to be used by BitStructure in
    order to build byte-aligned fields. Remember that BitPacket only
    works with byte-aligned fields, so it is not possible to create
    mixed (bit and byte) fields, that's why BitField can only be used
    by BitStructure.
    '''

    def __init__(self, name, size, default = 0):
        '''
        Initializes the field with the given 'name' and 'size' (in
        bits). By default the field's value will be initialized to 0
        or to 'default' if specified.
        '''
        Field.__init__(self, name)
        self.__bits = []
        self.__size = size
        self.set_value(default)

    def _encode(self, stream, context):
        try:
            binary = self.binary()
            write_stream(stream, byte_end(self.size()), decode_bin(binary))
        except (AssertionError, ValueError), err:
            raise ValueError('"%s" size error: %s' % (self.name(), err))

    def _decode(self, stream, context):
        try:
            binary = encode_bin(read_stream(stream, byte_end(self.size())))
            self.set_binary(binary)
        except ValueError, err:
            raise ValueError('"%s" size error: %s ' % (self.name(), err))

    def value(self):
        '''
        Returns the value of this field. As single bit fields do not
        have a concrete type (signed integers, float...) this will
        return the unsigned integer representation of this field.
        '''
        return bin_to_int(self.__bits)

    def set_value(self, value):
        '''
        Sets a new unsigned integer 'value' to the field.
        '''
        self.__bits = int_to_bin(value, self.size())

    def binary(self):
        '''
        Returns a binary string representing this field. The binary
        string is a sequence of 0's and 1's.
        '''
        return self.__bits

    def set_binary(self, binary):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's. The binary string can be longer than
        the real size of this field.
        '''
        self.__bits = binary[:self.size()]

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.__size

    def str_value(self):
        return hex_string(self.value(), byte_end(self.size()))

    def str_hex_value(self):
        return hex_string(self.hex_value(), byte_end(self.size()))

    def str_eng_value(self):
        return hex_string(self.eng_value(), byte_end(self.size()))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
