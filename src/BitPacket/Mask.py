#!/usr/bin/env python
#
# @file    Mask.py
# @brief   A field to represent bit masks
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

    Masks
    =====

    A field to represent bit masks.

    **API reference**: :class:`Mask`

    A bit mask is a field where each bit has a different
    meaning. Multiples bits can be set or unset at once, but each one
    will represent a single thing. Bit masks are commonly used to define
    a set of options.

    For example, we can define a 2-bit mask of whether our packet
    includes audio, video or both:

    +-------------+
    | audio/video |
    +=============+
    |   2 bits    |
    +-------------+

    This can be simply constructed by the following code:

    >>> m = Mask("audio/video", 0, AUDIO = 0x01, VIDEO = 0x02)
    >>> m.mask(m.AUDIO | m.VIDEO)
    >>> print m
    (audio/video = 0x03)

    We can also unmask a single option:

    >>> m.unmask(m.AUDIO)
    >>> print m
    (audio/video = 0x02)

    Or unmask all of them with *set_value*:

    >>> m.set_value(0)
    >>> print m
    (audio/video = 0x00)

'''

from BitPacket.BitField import *

from operator import itemgetter

class Mask(BitField):

    '''
    This class represents a bit mask field. Each bit has a unique
    meaning. Bit masks can be set, unset and tested.
    '''

    def __init__(self, name, value, **kwargs):
        '''
        Initialize the field with the given *name* and *value*. The list of
        all masks and their values are be given in *kwargs* with an
        arbitrary number of arguments (FLAG_1 = 0x01, FLAG_2 = 0x02
        ...).

        '''
        BitField.__init__(self, name, len(kwargs.items()), value)

        # List of masks in order (by value).
        self.__masks = []

        # Add bit masks. Note that kwargs is a dictionary, hence not
        # ordered.
        masks = sorted(kwargs.items(), key=itemgetter(1))
        for mask in masks:
            self.__masks.append(mask[0])
            self.__dict__[mask[0]] = mask[1]

    def is_set(self, mask):
        '''
        Tests whether the given bit *mask* is set. That is, all the given
        bits must be set.
        '''
        return (self.value() | mask)

    def mask(self, mask):
        '''
        Mask the given bits in *mask*. The current bits will be kept and
        the new ones will be additionally masked.
        '''
        self.set_value(self.value() | mask)

    def unmask(self, mask):
        '''
        Unmask the given bits in *mask*. The current bits will be kept and
        the new ones will be additionally unmasked.
        '''
        self.set_value(self.value() & ~mask)

    def str_value(self):
        '''
        Returns a human-readable representation of the hexadecimal value
        of this field.
        '''
        return self.str_hex_value()

    def str_eng_value(self):
        '''
        Returns a text string with all the bit mask names that are set. Bit
        masks names are separated by *|*.
        '''
        masks = []
        for mask in self.__masks:
            if self.value() & self.__dict__[mask]:
                masks.append(mask)
        return "|".join(masks)
