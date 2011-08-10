#
# @file    Mask.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Nov 17, 2010 13:02
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

from BitPacket.Value import *
from BitPacket.BitField import *

from operator import itemgetter

__STRUCT_MASK8_FMT__ = ">B"
__STRUCT_MASK16_FMT__ = ">H"
__STRUCT_MASK32_FMT__ = ">I"
__STRUCT_MASK64_FMT__ = ">Q"

__MASK_STR__ = ["Unmasked", "Masked"]


class Mask(BitField):

    def __init__(self, name, value = False):
        BitField.__init__(self, name, 1, value)

    def str_value(self):
        return __MASK_STR__[self.value()]

    def str_eng_value(self):
        return __MASK_STR__[self.eng_value()]


class MaskValue(Value):

    def __init__(self, name, format, masktype, value, **kwargs):
        Value.__init__(self, name, format, value)

        self.__masks = []
        self.__fields = []
        self.__fields_dict = {}

        # Add bit masks. Note that kwargs is a dictionary, hence not
        # ordered.
        masks = sorted(kwargs.items(), key=itemgetter(1))
        for mask in masks:
            self.__masks.append(mask[0])
            self.__dict__[mask[0]] = mask[1]

            field = masktype(mask[0])
            field._set_parent(self)
            self.__fields.append(field)
            self.__fields_dict[mask[0]] = field

        self.__update_masks()

    def mask(self, mask):
        self.set_value(self.value() | mask)
        self.__update_masks()

    def unmask(self, mask):
        self.set_value(self.value() & ~mask)
        self.__update_masks()

    def __update_masks(self):
        for mask in self.__masks:
            active = ((self.value() & self.__dict__[mask]) != 0)
            self.__fields_dict[mask].set_value(active)

    def fields(self):
        return self.__fields

    def str_value(self):
        return self.str_hex_value()

    def str_eng_value(self):
        return self.str_hex_value()


class Mask8(MaskValue):

    def __init__(self, name, masktype, value = 0, **kwargs):
        MaskValue.__init__(self, name, __STRUCT_MASK8_FMT__, masktype,
                           value, **kwargs)

class Mask16(MaskValue):

    def __init__(self, name, masktype, value = 0, **kwargs):
        MaskValue.__init__(self, name, __STRUCT_MASK16_FMT__, masktype,
                           value, **kwargs)

class Mask32(MaskValue):

    def __init__(self, name, masktype, value = 0, **kwargs):
        MaskValue.__init__(self, name, __STRUCT_MASK32_FMT__, masktype,
                           value, **kwargs)

class Mask64(MaskValue):

    def __init__(self, name, masktype, value = 0, **kwargs):
        MaskValue.__init__(self, name, __STRUCT_MASK64_FMT__, masktype,
                           value, **kwargs)


# from BitPacket.Boolean import *
# from BitPacket.Flag import *

# a =  Mask8("ValidityFlags", Mask, 0,
#            FLAG_1 = 0x01,
#            FLAG_2 = 0x02,
#            FLAG_3 = 0x04,
#            FLAG_4 = 0x08,
#            FLAG_5 = 0x10,
#            FLAG_6 = 0x20,
#            FLAG_7 = 0x40,
#            FLAG_8 = 0x80)

# a.mask(a.FLAG_1 | a.FLAG_2)

# print a

