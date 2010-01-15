#!/usr/bin/env python
#
# @file    MetaField.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Jan 15, 2010 10:22
#
# Copyright (C) 2010 Aleix Conchillo Flaque
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

from Field import Field

class MetaField(Field):

    def __init__(self, name,  fieldfunc):
        Field.__init__(self, name)
        self.__fieldfunc = fieldfunc
        self.__field = None

    def _encode(self, stream, context):
        if self.__field:
            self.__field._encode(stream, context)

    def _decode(self, stream, context):
        self.__field = self.__fieldfunc(context)
        self.__field._decode(stream, context)

    def value(self):
        if self.__field:
            return self.__field.value()
        return None

    def size(self):
        if self.__field:
            return self.__field.size()
        return 0

    def str_value(self):
        if self.__field:
            return self.__field.str_value()
        return ""

    def str_hex_value(self):
        if self.__field:
            return self.__field.str_hex_value()
        return ""

    def str_eng_value(self):
        if self.__field:
            return self.__field.str_eng_value()
        return ""

# import array

# from Integer import *

# f = MetaField("test", lambda ctx: UInt8('value'))
# f.set_array(array.array('B', [123]))
# print f

#if __name__ == '__main__':
#    import doctest
#    doctest.testmod()
