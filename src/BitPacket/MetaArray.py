#!/usr/bin/env python
#
# @file    MetaArray.py
# @brief   A meta array with an unknown length followed by fields (same type)
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Mon Jan 18, 2010 18:21
#
# Copyright (C) 2010, 2011 Aleix Conchillo Flaque
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

    **API reference**: :class:`MetaArray`

'''

from BitPacket.Structure import Structure

class MetaArray(Structure):

    def __init__(self, name, lengthtype, fieldfunc):
        Structure.__init__(self, name)
        self.__fieldfunc = fieldfunc
        self.__length = lengthtype("Length")

        self.append(self.__length)

    def _decode(self, stream, context):
        # Decode length value.
        self.__length._decode(stream, context)

        # Append fields and parse them.
        for i in range(self.__length.value()):
            new_field = self.__fieldfunc(context)
            new_field._set_name("%d" % i)
            new_field._decode(stream, context)
            self.append(new_field)


# import array

# from BitPacket.Integer import *

# ma = MetaArray("memory", UInt8,
#                lambda ctx: MetaArray("address", UInt8, lambda ctx: UInt32("value")))
# ma.set_array(array.array("B", [1,
#                                2,
#                                0x12, 0x34, 0x56, 0x78,
#                                0x9A, 0xBC, 0xDE, 0xFF]))
# print ma
