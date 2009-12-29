#!/usr/bin/env python
#
# @file    Real.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Oct 13, 2009 12:03
#
# Copyright (C) 2009 Aleix Conchillo Flaque
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
    (64-bit) bit fields.

    In order to encode and decode real values, the Python's 'struct'
    module is used. So, the conversion from binary data to real values
    depends on that module.


    Floats and doubles
    ------------------

    A float value can be easily created with the BitFieldFloat class:

    >>> value = Float('f', 1.967834)
    >>> print value
    (f = 1.96783399582)

    Some times, it is also useful to see the hexadecimal value that
    forms this float number.

    >>> print value.str_hex_value()
    0x3FFBE1FC

    The same might be applied for doubles:

    >>> value = Double('f', 0.0087552)
    >>> print value
    (f = 0.0087552)

'''

from Value import Value


__STRUCT_FLOAT_FMT__ = 'f'
__STRUCT_DOUBLE_FMT__ = 'd'


class Float(Value):

    def __init__(self, name, default = 0.0):
        Value.__init__(self, name, __STRUCT_FLOAT_FMT__, default)

class Double(Value):

    def __init__(self, name, default = 0.0):
        Value.__init__(self, name, __STRUCT_DOUBLE_FMT__, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
