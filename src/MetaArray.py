#!/usr/bin/env python
#
# @file    MetaArray.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Mon Jan 18, 2010 18:21
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
            new_field.set_name("%d" % i)
            new_field._decode(stream, context)
            self.append(new_field)

    def __setitem__(self, name, value):
        '''
        Sets the given 'value' to the field identified by 'name'.

        If the names[0] does not exists in the array the function
        will instantiate a new field automatically (only if the index is  
        consecutive to the length of the array).
        '''
        names = name.split(".", 1)
        length = self.__length.value()
    
        if int(names[0]) < length:
            # Normal access
            pass
        elif int(names[0]) > length:
            raise IndexError("Index %s must be <= %s" % (names[0], length))
        else: # int(names[0]) == length
            new_field = self.__fieldfunc(None)
            new_field.set_name("%d" % length)

            Structure.append(self,new_field)

            self.__length.set_value (length + 1)

        Structure.__setitem__(self, name, value)

# import array

# from Integer import *

# ma = MetaArray("memory", UInt8, 
#                lambda ctx: MetaArray("address", UInt8, lambda ctx: UInt32("value")))
# ma.set_array(array.array("B", [1,
#                                2,
#                                0x12, 0x34, 0x56, 0x78, 
#                                0x9A, 0xBC, 0xDE, 0xFF]))
# print ma

# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
