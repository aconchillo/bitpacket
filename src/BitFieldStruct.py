#!/usr/bin/env python
#
# @file    BitFieldStruct.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Oct 13, 2009 12:02
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

from struct import *

from BitFieldBase import BitFieldBase
from BitFieldBase import _byte_aligned
from BitFieldBase import _byte_start
from BitFieldBase import _encode_string

__ALLOWED_ENDIANNES__ = [ '@', '=', '<', '>', '!' ]

__DEFAULT_ENDIANNESS__ = '>'

# Size (in bits) of a byte
__BYTE_SIZE__ = 8

#Character 	Byte order 	Size and alignment
# @ 	native 	native
# = 	native 	standard
# < 	little-endian 	standard
# > 	big-endian 	standard
# ! 	network (= big-endian) 	standard

class BitFieldStruct(BitFieldBase):

    def __init__(self, name, size, format):
        BitFieldBase.__init__(self, name)

        if size == 0:
            raise ValueError, 'Number of element must be at least 1'

        # Numer of elements in the struct
        self.__count = size

        # This will store the string of bytes
        self.__bytes = ""

        # Calculate bit size from struct type
        self.__base_format = format
        self.__base_size = calcsize(format)
        self.__format = "%d%s" % (size, format)
        self.__size = calcsize(self.__format)

        # Set default endianness
        self.set_endianness(__DEFAULT_ENDIANNESS__)

    def value(self):
        values = unpack(self.__str_format(), self.string())
        if self.__count > 1:
            return values
        else:
            return values[0]

    def set_value(self, *values):
        string = pack(self.__str_format(), *values)
        self.set_string(string)

    def string(self):
        return self.__bytes

    def set_string(self, string, start = 0):
        if _byte_aligned(start):
            byte_start = _byte_start(start)
            self.__bytes = string[byte_start:self.byte_size() + byte_start]
        else:
            bits = _encode_string(string, start, self.byte_size())
            # If the bit start is byte aligned, _encode_string will
            # return the first valid byte, so we need start from 0.
            if _byte_aligned(start):
                start = 0
            self.set_binary(bits, start)

    def binary(self):
        return _encode_string(self.__bytes, self.byte_size())

    def set_binary(self, bits):
        self.set_string(_decode_string(bits))

    def hex_value(self):
        index = 0
        hex_values = []
        for i in range(self.__count):
            value = 0
            for k in range(self.__base_size):
                value = (value << __BYTE_SIZE__) + ord(self.__bytes[index])
                index += 1
            hex_values.append(value)
        if self.__count > 1:
            return tuple(hex_values)
        else:
            return hex_values[0]

    def eng_value(self):
        if self.__count > 1:
            return [self.calibration_curve()(value) for value in self.value()]
        else:
            return BitFieldBase.eng_value(self)

    def set_endianness(self, endianness):
        if endianness not in __ALLOWED_ENDIANNES__:
            raise KeyError, "'%s' is not an allowed endianness" % endianness
        self.__endianness = endianness

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.byte_size() * __BYTE_SIZE__

    def byte_size(self):
        '''
        Returns the size of the field in bytes.
        '''
        return self.__size

    def _base_format(self):
        return self.__base_format

    def __str_format(self):
        return self.__endianness + self.__format
