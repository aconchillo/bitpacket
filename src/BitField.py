#!/usr/bin/env python
#
# @file    BitField.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 12:34
#
# Copyright (C) 2007-2009 Aleix Conchillo Flaque
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

__doc__ = '''

    SINGLE BIT FIELDS

    A packet might be formed by mutiple fields that could be single
    bit fields, integer fields, structure fields or variable structure
    fields.

    An example of a packet could be:

    +-------+-----------+---------+------------------+
    |  id   |  address  | nbytes  |       data       |
    +-------+-----------+---------+------------------+
     <- 1 -> <--- 4 ---> <-- 2 --> <---- nbytes ---->

    That is, a packet with four fields:

        - Identifier: 1 byte
        - Memory address: 4 bytes
        - Number of data bytes: 2 bytes
        - Data: number of data bytes

    The first field could be constructed by the following piece of
    code:

    >>> bf = BitField('id', 8, 0x54)
    >>> bf.value() == 0x54
    True

    that would create a BitField instance of a field named 'id' of 1
    byte size and value 0x54.


    UNPACKING SINGLE BIT FIELDS

    In order to unpack a single field from a data buffer, one would
    create a BitField without any initialisation and assign the data
    buffer when ready:

    >>> data = array.array('B', [0x35])
    >>> bf = BitField('id', 8)
    >>> bf.set_array(data)
    >>> bf.array()
    array('B', [53])
    >>> print bf
    (id = 0x35)
    >>> bf.set_array(bf.array())
    >>> bf.set_value(bf.value())
    >>> print bf
    (id = 0x35)

'''

import array

from BitFieldBase import BitFieldBase
from BitFieldBase import _bin_to_int
from BitFieldBase import _int_to_bin
from BitFieldBase import _encode_array
from BitFieldBase import _decode_array

class BitField(BitFieldBase):
    '''
    This class represents a bit field to be used together with
    BitStructure and BitVariableStructure sub-classes in order to
    build packets.
    '''

    def __init__(self, name, size, default = None):
        '''
        Initializes the field with the given 'name' and 'size' (in
        bits). By default the field's value will be initialized to 0
        or to 'default' if specified.
        '''
        BitFieldBase.__init__(self, name)
        self.__bits = []
        self.__size = size
        if default != None:
            self.set_value(default)

    def value(self):
        '''
        Returns the integer value of the field.
        '''
        return self.hex_value()

    def set_value(self, value):
        '''
        Sets a new integer 'value' to the field.
        '''
        self.__bits = _int_to_bin(value, self.size())

    def array(self):
        '''
        Returns a byte array (big-endian) representing this field.
        '''
        if (self.size() & 7) != 0:
            raise ValueError, '"%s" size must be a multiple of 8' % self.name()
        return _decode_array(self.__bits)

    def set_array(self, data):
        '''
        Sets a byte array (big-endian) to the field. The array should
        be of type 'B' (unsigned char).
        '''
        if (self.size() & 7) != 0:
            raise ValueError, '"%s" size must be a multiple of 8' % self.name()
        self.__bits = _encode_array(data, self.byte_size())

    def binary(self):
        '''
        Returns a binary string representing this field. The binary
        string is a sequence of 0's and 1's.
        '''
        return self.__bits

    def set_binary(self, bits):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's.
        '''
        self.__bits = bits

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.__size

    def hex_value(self):
        return _bin_to_int(self.__bits)

    def str_value(self):
        '''
        Returns a human-readable representation of this field. This is
        is a default hexadecimal representation for all BitFields.
        '''
        return self.str_hex_value()

    def str_hex_value(self):
        '''
        Returns a human-readable representation of this field. This is
        is a default hexadecimal representation for all BitFields.
        '''
        hex_size = self.byte_size() * 2
        return '0x%0*X' % (hex_size, self.hex_value())

    def str_eng_value(self):
        '''
        Returns a human-readable representation of this field. This is
        is a default hexadecimal representation for all BitFields.
        '''
        return '0x%0*X' % (hex_size, self.eng_value())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
