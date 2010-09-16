#!/usr/bin/env python
#
# @file    String.py
# @brief   A field to represent a stream of bytes
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Wed Jan 20, 2010 09:18
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

    **API reference**: :class:`String`

'''

from utils.stream import read_stream, write_stream

from Field import Field

class String(Field):

    def __init__(self, name, data = "", lengthfunc = lambda ctx: len(data)):
        Field.__init__(self, name)
        self.__data = data
        self.__lengthfunc = lengthfunc

    def _encode(self, stream, context):
        write_stream(stream, self.__lengthfunc(context), self.__data)

    def _decode(self, stream, contex):
        self.__data = read_stream(stream, self.__lengthfunc(contex))

    def size(self):
        return len(self.__data)

    def value(self):
        return self.__data

    def set_value(self, data):
        self.__data = data

    def str_value(self):
        string = ""
        value = self.value()
        if len(value) > 0:
            string = "0x" + "".join(["%02X" % ord(c) for c in value])
        return string

    def str_hex_value(self):
        return self.str_value()

    def str_eng_value(self):
        return self.str_value()
