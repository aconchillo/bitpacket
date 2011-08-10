#!/usr/bin/env python
#
# @file    Integer.py
# @brief   Integer fields for signed/unsigned values of various sizes
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Tue Oct 13, 2009 12:03
#
# Copyright (C) 2009, 2010, 2011 Aleix Conchillo Flaque
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

from BitPacket.Value import Value


__STRUCT_INT8_LE_FMT__ = "<b"
__STRUCT_UINT8_LE_FMT__ = "<B"
__STRUCT_INT8_BE_FMT__ = ">b"
__STRUCT_UINT8_BE_FMT__ = ">B"

__STRUCT_INT16_LE_FMT__ = "<h"
__STRUCT_UINT16_LE_FMT__ = "<H"
__STRUCT_INT16_BE_FMT__ = ">h"
__STRUCT_UINT16_BE_FMT__ = ">H"

__STRUCT_INT32_LE_FMT__ = "<i"
__STRUCT_UINT32_LE_FMT__ = "<I"
__STRUCT_INT32_BE_FMT__ = ">i"
__STRUCT_UINT32_BE_FMT__ = ">I"

__STRUCT_INT64_LE_FMT__ = "<q"
__STRUCT_UINT64_LE_FMT__ = "<Q"
__STRUCT_INT64_BE_FMT__ = ">q"
__STRUCT_UINT64_BE_FMT__ = ">Q"


########################################################################

class Int8LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT8_LE_FMT__, value)

class UInt8LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT8_LE_FMT__, value)

class Int8BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT8_BE_FMT__, value)

class UInt8BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT8_BE_FMT__, value)

Int8 = Int8BE
UInt8 = UInt8BE

########################################################################

class Int16LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT16_LE_FMT__, value)

class UInt16LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT16_LE_FMT__, value)

class Int16BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT16_BE_FMT__, value)

class UInt16BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT16_BE_FMT__, value)

Int16 = Int16BE
UInt16 = UInt16BE

########################################################################

class Int32LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT32_LE_FMT__, value)

class UInt32LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT32_LE_FMT__, value)

class Int32BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT32_BE_FMT__, value)

class UInt32BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT32_BE_FMT__, value)

Int32 = Int32BE
UInt32 = UInt32BE

########################################################################

class Int64LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT64_LE_FMT__, value)

class UInt64LE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT64_LE_FMT__, value)

class Int64BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_INT64_BE_FMT__, value)

class UInt64BE(Value):

    def __init__(self, name, value = 0):
        Value.__init__(self, name, __STRUCT_UINT64_BE_FMT__, value)


Int64 = Int64BE
UInt64 = UInt64BE
