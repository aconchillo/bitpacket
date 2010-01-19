#!/usr/bin/env python
#
# @file    Integer.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Oct 13, 2009 12:03
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

__doc__ = '''

    Integer fields
    ==============

    This module provides classes to define signed and unsigned
    integers bit fields, from 8-bit to 64-bit.

    In order to encode and decode integer values, the Python's
    'struct' module is used. So, the conversion from binary data to
    integer values depends on that module.


    Signed and unsigned
    -------------------

    Multiple signed and unsigned integer classes are available. It is,
    for example, very easy to create a new 16-bit signed integer bit
    field:

    >>> value = Int16("int16", -1345)
    >>> print value
    (int16 = -1345)

    or a 16-bit unsigned one:

    >>> value = UInt16("uint16", 0x8000)
    >>> print value
    (uint16 = 32768)

'''

from Value import Value


__STRUCT_INT8_FMT__ = 'b'
__STRUCT_UINT8_FMT__ = 'B'
__STRUCT_INT16_FMT__ = 'h'
__STRUCT_UINT16_FMT__ = 'H'
__STRUCT_INT32_FMT__ = 'i'
__STRUCT_UINT32_FMT__ = 'I'
__STRUCT_INT64_FMT__ = 'q'
__STRUCT_UINT64_FMT__ = 'Q'


class Int8(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_INT8_FMT__, default)

class UInt8(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_UINT8_FMT__, default)

class Int16(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_INT16_FMT__, default)

class UInt16(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_UINT16_FMT__, default)

class Int32(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_INT32_FMT__, default)

class UInt32(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_UINT32_FMT__, default)

class Int64(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_INT64_FMT__, default)

class UInt64(Value):

    def __init__(self, name, default = 0):
        Value.__init__(self, name, __STRUCT_UINT64_FMT__, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
