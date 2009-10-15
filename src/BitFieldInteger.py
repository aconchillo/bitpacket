#!/usr/bin/env python
#
# @file    BitFieldInteger.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Oct 13, 2009 12:03
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


__doc__ = '''
'''

from BitFieldStruct import BitFieldStruct


__STRUCT_INT8_FMT__ = 'b'
__STRUCT_UINT8_FMT__ = 'B'
__STRUCT_INT16_FMT__ = 'h'
__STRUCT_UINT16_FMT__ = 'H'
__STRUCT_INT32_FMT__ = 'i'
__STRUCT_UINT32_FMT__ = 'I'
__STRUCT_INT64_FMT__ = 'q'
__STRUCT_UINT64_FMT__ = 'Q'


class BitFieldInteger(BitFieldStruct):

    def __init__(self, name, format, default = 0):
        BitFieldStruct.__init__(self, name, format, default)

    def str_value(self):
        '''
        Returns a human-readable representation for a float value.
        '''
        return '%d' % self.value()

    def str_eng_value(self):
        '''
        Returns a human-readable representation for a float value.
        '''
        return '%d' % self.eng_value()


class BitFieldInt8(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT8_FMT__, default)

class BitFieldUInt8(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT8_FMT__, default)

class BitFieldInt16(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT16_FMT__, default)

class BitFieldUInt16(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT16_FMT__, default)

class BitFieldInt32(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT32_FMT__, default)

class BitFieldUInt32(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT32_FMT__, default)

class BitFieldInt64(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT64_FMT__, default)

class BitFieldUInt64(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT64_FMT__, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
