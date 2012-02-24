#!/usr/bin/env python
#
# @file    Real.py
# @brief   Real fields for values of various sizes
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Tue Oct 13, 2009 12:03
#
# Copyright (C) 2009, 2010, 2011, 2012 Aleix Conchillo Flaque
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

    Real fields
    ===========

    This module provides classes to define float (32-bit) and double
    (64-bit) fields.


    Floats and doubles
    ------------------

    A float value can be easily created with the :class:`Float` class:

    >>> value = Float("f", 1.967834)
    >>> print value
    (f = 1.96783399582)

    Some times, it is also useful to see the hexadecimal value that
    forms this float number.

    >>> print value.str_hex_value()
    0x3FFBE1FC

    The same might be applied for doubles:

    >>> value = Double("f", 0.0087552)
    >>> print value
    (f = 0.0087552)

    Helper classes
    --------------

    Default helper classes use network byte order (big-endian):

    +-----+---------------+
    |Size |Class          |
    +=====+===============+
    |32   |:class:`Float` |
    +-----+---------------+
    |64   |:class:`Double`|
    +-----+---------------+

    Endianness helper classes:

    +-----+-----------------+-----------------+
    |Size |Little-Endian    |Big-Endian       |
    +=====+=================+=================+
    |32   |:class:`FloatLE` |:class:`FloatBE` |
    +-----+-----------------+-----------------+
    |64   |:class:`DoubleLE`|:class:`DoubleBE`|
    +-----+-----------------+-----------------+

'''

from BitPacket.Value import Value

__STRUCT_FLOAT_LE_FMT__ = "<f"
__STRUCT_FLOAT_BE_FMT__ = ">f"

__STRUCT_DOUBLE_LE_FMT__ = "<d"
__STRUCT_DOUBLE_BE_FMT__ = ">d"


########################################################################

class FloatLE(Value):

    def __init__(self, name, value = 0.0):
        Value.__init__(self, name, __STRUCT_FLOAT_LE_FMT__, value)

class FloatBE(Value):

    def __init__(self, name, value = 0.0):
        Value.__init__(self, name, __STRUCT_FLOAT_BE_FMT__, value)

Float = FloatBE

########################################################################

class DoubleLE(Value):

    def __init__(self, name, value = 0.0):
        Value.__init__(self, name, __STRUCT_DOUBLE_LE_FMT__, value)

class DoubleBE(Value):

    def __init__(self, name, value = 0.0):
        Value.__init__(self, name, __STRUCT_DOUBLE_BE_FMT__, value)

Double = DoubleBE
