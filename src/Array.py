#!/usr/bin/env python
#
# @file    Array.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Mon Jan 18, 2010 18:20
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

from Structure import Structure

class Array(Structure):

    def __init__(self, name, lengthtype, basetype):
        Structure.__init__(self, name)
        self.__length = lengthtype("Length")
        self.__basetype = basetype

        Structure.append(self, self.__length)

    def append(self, field):
        if isinstance(field, self.__basetype):
            value = self["Length"]
            field.set_name(value)
            self["Length"] = value + 1
            Structure.append(self, field)
        else:
            raise TypeError("Invalid field type for array '%s'" % self.name())

# from Integer import *

# class Sub32(UInt32):

#     def __init__(self, value):
#         UInt32.__init__(self, "foo", value)

# a = Array("test", UInt8, UInt32)
# a.append(UInt32("value", 23))
# a.append(Sub32(34))

# print a


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
