#!/usr/bin/env python
#
# @file    Data.py
# @brief   An structure with a length followed by data (of the given length)
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
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

from Structure import Structure
from String import String

class Data(Structure):

    def __init__(self, name, lengthtype, data = "", wordsize = 1):
        Structure.__init__(self, name)
        self.__wordsize = wordsize

        self.__length = lengthtype("Length")
        self.__data = String("Data",
                             lambda ctx: self.__length.value() * wordsize,
                             data)

        Structure.append(self, self.__length)
        Structure.append(self, self.__data)

    def value(self):
        return self.__data.value()

    def set_value(self, value):
        self.__length.set_value(len(value) * self.__wordsize)
        self.__data.set_value(value)
