#!/usr/bin/env python
#
# @file    BitField.py
# @brief   A field to represent single bit fields
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Sun Aug 02, 2009 12:34
#
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Aleix Conchillo Flaque
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

    A field to represent single bit fields.

    **API reference**: :class:`BitField`

    A packet might be formed by multiple fields that can be single bit
    fields, numeric fields, etc. Sometimes, byte-aligned fields are also
    formed by bit fields internally. The purpose of :mod:`BitField` is
    to provide these single bit fields.

    For example, the first byte of the IP header is formed by two
    nibbles:

    +---------+---------+
    | version |  hlen   |
    +=========+=========+
    | 4 bits  | 4 bits  |
    +---------+---------+

    The first nibble, *version*, can be constructed by the following
    piece of code:

    >>> bf = BitField("version", 4, 15)
    >>> print bf
    (version = 0x0F)

    That is, a 4 bits field with a default, optional, value 15.

'''

from BitPacket.utils.binary import byte_end, bin_to_int, int_to_bin
from BitPacket.utils.bitstream import BitStreamReader, BitStreamWriter
from BitPacket.utils.stream import read_stream, write_stream
from BitPacket.utils.string import hex_string

from BitPacket.Field import Field

from math import log

class BitField(Field):
    '''
    This class represents bit fields to be used by :class:`BitStructure`
    in order to build byte-aligned fields. Remember that BitPacket only
    works with byte-aligned fields, so it is not possible to create
    mixed (bit and byte) fields, that's why :mod:`BitField` can only be
    used inside a :class:`BitStructure`.
    '''

    def __init__(self, name, size, value = 0):
        '''
        Initialize the field with the given *name* and *size* (in
        bits). By default the field's value will be initialized to 0 or
        to *value* if specified.
        '''
        Field.__init__(self, name)
        self.__bits = []
        self.__size = size
        self.set_value(value)

    def _encode(self, stream):
        if isinstance(stream, BitStreamWriter):
            write_stream(stream, self.size(), self.__bits)
        else:
            raise TypeError("Stream for bit fields should be bit oriented "
                            "(hint: enclose it in a BitStructure)")

    def _decode(self, stream):
        if isinstance(stream, BitStreamReader):
            self.__bits = read_stream(stream, self.size())
        else:
            raise TypeError("Stream for bit fields should be bit oriented "
                            "(hint: enclose it in a BitStructure)")

    def value(self):
        '''
        Returns the value of this field. As single bit fields do not
        have a concrete type (signed integers, float...) this will
        return the unsigned integer representation of this field.
        '''
        return bin_to_int(self.__bits)

    def set_value(self, value):
        '''
        Sets a new unsigned integer *value* to the field.
        '''
        if value < 0:
            raise ValueError("Negative values not allowed in BitFields "
                             "(field: '%s')" % self.name())

        size = self.size()
        if value > 0:
            size = int(log(value, 2) + 1)
        if size <= self.size():
            self.__bits = int_to_bin(value, self.size())
        else:
            raise ValueError("Value is bigger than the field size "
                             "(value %d has bit size %d, '%s' bit size is %d)"
                             % (value, size, self.name(), self.size ()))

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.__size

    def str_value(self):
        '''
        Returns a human-readable representation of the value of this
        field. In case of bit fields the representation is an
        hexadecimal value.
        '''
        return hex_string(self.value(), byte_end(self.size()))

    def str_hex_value(self):
        '''
        Returns a human-readable representation of the hexadecimal value
        of this field. This will return the same as *str_value*.
        '''
        return hex_string(self.hex_value(), byte_end(self.size()))

    def str_eng_value(self):
        '''
        Returns a human-readable representation of the engineering
        value. This function will first calculate the engineering value
        (by applying the calibration curve) and will return the string
        representation of it. In case of bit fields the representation
        is an hexadecimal value.
        '''
        return hex_string(self.eng_value(), byte_end(self.size()))
