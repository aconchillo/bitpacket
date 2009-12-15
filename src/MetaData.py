#!/usr/bin/env python
#
# @file    MetaData.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 15:42
#
# Copyright (C) 2009 Aleix Conchillo Flaque
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

from utils.stream import read_stream, write_stream

from Field import Field

class MetaData(Field):

    def __init__(self, name, lengthfunc, data = ""):
        Field.__init__(self, name)
        self.__data = data
        self.__lengthfunc = lengthfunc

    def _encode(self, stream, context):
        write_stream(stream, self.__lengthfunc(context), self.__data)

    def _decode(self, stream, context):
        self.__data = read_stream(stream, self.__lengthfunc(context))

    def value(self):
        return self.__data

    def size(self):
        return len(self.__data)

    def str_value(self):
        return "0x" +  "".join(["%02X" % ord(c) for c in self.value()])

    def str_hex_value(self):
        return self.str_value()

    def str_eng_value(self):
        return self.str_value()
