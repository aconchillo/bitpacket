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

    def __init__(self, name, format):
        BitFieldBase.__init__(self, name)

        # This will store the string of bytes
        self.__bytes = ""

        # Calculate bit size from struct type
        self.__format = format
        self.__size = calcsize(format)

        # Set default endianness
        self.set_endianness(__DEFAULT_ENDIANNESS__)

    def value(self):
        return unpack(self.__str_format(), self.string())

    def set_value(self, *values):
        string = pack(self.__str_format(), *values)
        self.set_string(string)

    def string(self):
        return self.__bytes

    def set_string(self, string):
        self.__bytes = string[0:self.byte_size()]

    def binary(self):
        return _encode_string(self.__bytes, self.byte_size())

    def set_binary(self, bits):
        self.set_string(_decode_string(bits))

    def hex_value(self):
        value = 0
        for c in self.__bytes:
            value = (value << __BYTE_SIZE__) + ord(c)
        return value

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

    def __str_format(self):
        return self.__endianness + self.__format
