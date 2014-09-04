#!/usr/bin/env python
#
# @file    Flag.py
# @brief   A bit field for representing a flag
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

    Flags
    =====

    A bit field for representing a flag.

    **API reference**: :class:`Flag`

    A :class:`Flag` is a :class:`BitField` with a single bit. As in the
    :class:`Boolean` type, it can have only two values Active and
    Inactive. Basically, it is just a helper class to print Active or
    Inactive instead of True or False. The same behavior could be
    achieved by using the :class:`Boolean` type.

    >>> f = Flag("Flag", Flag.Active)
    >>> print f
    (Flag = Active)

    There a couple of helper function to activate or deactivate the
    flag:

    >>> f.deactivate()
    >>> print f
    (Flag = Inactive)

    >>> f.activate()
    >>> print f
    (Flag = Active)

'''

from BitPacket.BitField import *

__FLAG_STR__ = ["Inactive", "Active"]


class Flag(BitField):

    '''
    This class represents a boolean field. It is a convenient class to
    represent True and False values.
    '''

    Inactive = 0
    Active = 1

    def __init__(self, name, value = Inactive):
        '''
        Initialize the field with the given *name*. The default value is
        Inactive.
        '''
        BitField.__init__(self, name, 1, value)

    def activate(self):
        '''
        Activate the flag.
        '''
        self.set_value(Flag.Active)

    def deactivate(self):
        '''
        Deactivate the flag.
        '''
        self.set_value(Flag.Inactive)

    def str_value(self):
        '''
        Returns a text string with Active or Inactive.
        '''
        return __FLAG_STR__[self.value()]

    def str_eng_value(self):
        '''
        Returns a text string with Active or Inactive.
        '''
        return __FLAG_STR__[self.eng_value()]
