#!/usr/bin/env python
#
# @file    Value.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Oct 13, 2009 12:02
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

    Numeric fields
    ==============

    An object-oriented representation of bit field structures.

    These classes represent simple bit fields, and fixed and variable
    structures of bit fields which might be used to construct
    packets. BitField, BitStructure and BitVariableStructure implement
    the BitFieldBase abstract class, so all of them can be used
    together. This means that, for example, we can add any
    BitFieldBase sub-class into a BitStructure or
    BitVariableStructure.

'''

from struct import *

from utils.string import hex_string
from utils.stream import read_stream, write_stream

from Field import Field

__ALLOWED_ENDIANNES__ = [ '@', '=', '<', '>', '!' ]

__DEFAULT_ENDIANNESS__ = '>'

# Character     Byte order               Size and alignment
# @             native                   native
# =             native                   standard
# <             little-endian            standard
# >             big-endian               standard
# !             network (= big-endian)   standard

class Value(Field):

    def __init__(self, name, format, value):
        Field.__init__(self, name)

        # This will store the string of bytes
        self.__bytes = ""

        # Calculate bit size from struct type
        self.__format = format
        self.__size = calcsize(self.__format)

        # Set default endianness
        self.set_endianness(__DEFAULT_ENDIANNESS__)

        # Finally set default value
        self.set_value(value)

    def _encode(self, stream, context):
        write_stream(stream, self.size(), self.__bytes)

    def _decode(self, stream, context):
        self.__bytes = read_stream(stream, self.size())

    def set_endianness(self, endianness):
        if endianness not in __ALLOWED_ENDIANNES__:
            raise KeyError, "'%s' is not an allowed endianness" % endianness
        self.__endianness = endianness

    def value(self):
        value = unpack(self.__str_format(), self.__bytes)
        return value[0]

    def set_value(self, value):
        string = pack(self.__str_format(), value)
        self.set_string(string)

    def hex_value(self):
        value = 0
        for c in self.__bytes:
            value = (value << 8) + ord(c)
        return value

    def size(self):
        return self.__size

    def str_value(self):
        return str(self.value())

    def str_hex_value(self):
        return hex_string(self.hex_value(), self.size())

    def str_eng_value(self):
        return str(self.eng_value())

    def __str_format(self):
        return self.__endianness + self.__format
