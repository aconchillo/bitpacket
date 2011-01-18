#!/usr/bin/env python
#
# @file    Array.py
# @brief   An structure with a length followed by fields (same type)
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
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

__doc__ = '''

    **API reference**: :class:`Array`

'''

from Structure import Structure

__FIELD_SEPARATOR__ = "."

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
            Structure.__setitem__(self, "Length", value + 1)
            Structure.append(self, field)
        else:
            raise TypeError("Invalid field type for array '%s'" % self.name())

    def __setitem__(self, name, value):
        '''
        Sets the given 'value' to the field identified by 'name'.

        If the names[0] does not exists in the array the function
        will instantiate a new field automatically (only if the index is
        consecutive to the length of the array).
        '''
        names = name.split(__FIELD_SEPARATOR__, 1)
        length = self.__length.value()

        if int(names[0]) < length:
            # Normal access
            pass
        elif int(names[0]) == length:
            new_field = self.__basetype("%d" % length)
            Structure.append(self, new_field)
            self.__length.set_value (length + 1)
        else: # int(names[0]) > length
            raise IndexError("Index %s must be <= %s" % (names[0], length))

        Structure.__setitem__(self, name, value)

# from Integer import *

# class Sub32(UInt32):

#     def __init__(self, value):
#         UInt32.__init__(self, "foo", value)

# a = Array("test", UInt8, UInt32)
# a.append(UInt32("value", 23))
# a.append(Sub32(34))

# print a

if __name__ == "__main__":
    import doctest
    doctest.testmod()
