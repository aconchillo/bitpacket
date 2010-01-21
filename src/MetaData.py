#!/usr/bin/env python
#
# @file    MetaData.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 15:42
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

from Structure import Structure
from String import String

class MetaData(Structure):

    def __init__(self, name, lengthtype, wsizefunc):
        Structure.__init__(self, name)
        self.__length = lengthtype("Length")
        self.__data = String("Data", 
                             lengthfunc = lambda ctx: ctx["Length"] * wsizefunc(ctx))
        self.append(self.__length)
        self.append(self.__data)
