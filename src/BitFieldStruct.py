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

import array

from struct import *

from BitField import BitField

__ALLOWED_ENDIANNES__ = [ '@', '=', '<', '>', '!' ]

__DEFAULT_ENDIANNESS__ = '>'

#Character 	Byte order 	Size and alignment
# @ 	native 	native
# = 	native 	standard
# < 	little-endian 	standard
# > 	big-endian 	standard
# ! 	network (= big-endian) 	standard

class BitFieldStruct(BitField):

    def __init__(self, name, format, default = 0):
        # Set default endianness
        self.set_endianness(__DEFAULT_ENDIANNESS__)

        # Calculate bit size from struct type
        self.__format = format
        size = calcsize(format) * 8

        # Initialize BitField and set converted value
        BitField.__init__(self, name, size)
        self.set_array(self.__value2array(default))

    def value(self):
        string = self.array().tostring()
        val = unpack(self.__str_format(), string)
        return val[0]

    def set_endianness(self, endianness):
        if endianness not in __ALLOWED_ENDIANNES__:
            raise KeyError, "'%s' is not an allowed endianness" % endianness
        self.__endianness = endianness

    def __value2array(self, value):
        packed = pack(self.__str_format(), value)
        data = array.array('B')
        data.fromstring(packed)
        return data

    def __str_format(self):
        return self.__endianness + self.__format
