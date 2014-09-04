#!/usr/bin/env python
#
# @file    Boolean.py
# @brief   A bit field for representing a boolean type
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Nov 17, 2010 13:02
#
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Aleix Conchillo Flaque
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

    Booleans
    ========

    A bit field for representing a boolean type.

    **API reference**: :class:`Boolean`

    A :class:`Boolean` is a :class:`BitField` with a single bit. So only
    True or False can be set.

    >>> b = Boolean("Option", True)
    >>> print b
    (Option = True)

    There a couple of helper function to enable or disable the field
    value:

    >>> b.disable()
    >>> print b
    (Option = False)

    >>> b.enable()
    >>> print b
    (Option = True)

'''

from BitPacket.BitField import *

__BOOLEAN_STR__ = ["False", "True"]


class Boolean(BitField):

    '''
    This class represents a boolean field. It is a convenient class to
    represent True and False values.
    '''

    def __init__(self, name, value = False):
        '''
        Initialize the field with the given *name*. The default value is
        False.
        '''
        BitField.__init__(self, name, 1, value)

    def enable(self):
        '''
        Set the value to True.
        '''
        self.set_value(True)

    def disable(self):
        '''
        Set the value to False.
        '''
        self.set_value(False)

    def str_value(self):
        '''
        Returns a text string with True or False.
        '''
        return __BOOLEAN_STR__[self.value()]

    def str_eng_value(self):
        '''
        Returns a text string with True or False.
        '''
        return __BOOLEAN_STR__[self.eng_value()]
