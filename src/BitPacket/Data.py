#!/usr/bin/env python
#
# @file    Data.py
# @brief   An structure with a length followed by data (of the given length)
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Jan 20, 2010 11:30
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

    **API reference**: :class:`Data`

'''

from BitPacket.Structure import Structure
from BitPacket.String import String

class Data(Structure):

    def __init__(self, name, lengthtype, data = "", wordsize = 1):
        Structure.__init__(self, name)
        self.__wordsize = wordsize

        self.__length = lengthtype("Length")
        self.__data = String("Data",
                             data,
                             lambda ctx: self.__length.value() * wordsize)

        Structure.append(self, self.__length)
        Structure.append(self, self.__data)

    def value(self):
        return self.__data.value()

    def set_value(self, value):
        length = len(value)
        if (length % self.__wordsize) == 0:
            self.__length.set_value(length / self.__wordsize)
            self.__data.set_value(value)
        else:
            raise ValueError("Data length must be a multiple of %d (%d given)" \
                                 % (self.__wordsize, length))
