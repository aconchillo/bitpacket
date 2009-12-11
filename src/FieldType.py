#!/usr/bin/env python
#
# @file    FieldType.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 11:58
#
# Copyright (C) 2007-2009 Aleix Conchillo Flaque
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

__TYPE_BIT__  = 0x01
__TYPE_BYTE__ = 0x02

__TYPES__ = { __TYPE_BIT__  : 'bit',
              __TYPE_BYTE__ : 'byte' }

class FieldType:

    def __init__(self, code):
        if code not in __TYPES__:
            raise KeyError, '%s is not a valid field type' % code

        self.__code = code

    def code(self):
        return self.__code

    def __str__(self):
        return __TYPES__[self.code()]


FieldTypeBit = FieldType(__TYPE_BIT__)
FieldTypeByte = FieldType(__TYPE_BYTE__)
