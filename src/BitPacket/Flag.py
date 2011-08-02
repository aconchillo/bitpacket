#
# @file    Flag.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Nov 17, 2010 13:02
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

from BitPacket.BitField import *

__FLAG_STR__ = ["Inactive", "Active"]


class Flag(BitField):

    Inactive = 0
    Active = 1

    def __init__(self, name, value = Inactive):
        BitField.__init__(self, name, 1, value)

    def activate(self):
        self.set_value(Flag.Active)

    def deactivate(self):
        self.set_value(Flag.Inactive)

    def str_value(self):
        return __FLAG_STR__[self.value()]

    def str_eng_value(self):
        return __FLAG_STR__[self.eng_value()]
