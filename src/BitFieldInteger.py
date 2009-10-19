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

    Signed and unsigned integer bit fields.

    This module provides classes to define signed and unsigned
    integers bit fields, from 8-bit to 64-bit.

    In order to encode and decode integer values, the Python's
    'struct' module is used. So, the conversion from binary data to
    integer values depends on that module.


    SIGNED and UNSIGNED INTEGERS

    Multiple signed and unsigned integer classes are available. It is,
    for example, very easy to create a new 16-bit signed integer bit
    field:

    >>> value = BFInt16('int16', -1345)
    >>> print value
    (int16 = -1345)

    or a 16-bit unsigned one:

    >>> value = BFUInt16('uint16', 0x8000)
    >>> print value
    (uint16 = 32768)

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
        BitFieldStruct.__init__(self, name, 1, format)
        self.set_value(default)

    def value(self):
        return BitFieldStruct.value(self)[0]

    def str_value(self):
        '''
        Returns a human-readable representation for the integer value.
        '''
        return '%d' % self.value()

    def str_eng_value(self):
        '''
        Returns a human-readable representation for the engineering
        value.

        The engineering values is, by default, represented as an
        integer value.
        '''
        return '%d' % self.eng_value()

class BFInt8(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT8_FMT__, default)

class BFUInt8(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT8_FMT__, default)

class BFInt16(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT16_FMT__, default)

class BFUInt16(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT16_FMT__, default)

class BFInt32(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT32_FMT__, default)

class BFUInt32(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT32_FMT__, default)

class BFInt64(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT64_FMT__, default)

class BFUInt64(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT64_FMT__, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
