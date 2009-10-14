#!/usr/bin/env python
#
# @file    BitFieldReal.py
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


__STRUCT_FLOAT_FMT__ = 'f'
__STRUCT_DOUBLE_FMT__ = 'd'


class BitFieldReal(BitFieldStruct):

    def __init__(self, name, format, default = None):
        BitFieldStruct.__init__(self, name, format, default)

    def str_value(self):
        '''
        Returns a human-readable representation for a float value.
        '''
        return '%g' % self.value()

    def str_eng_value(self):
        '''
        Returns a human-readable representation for a float value.
        '''
        return '%g' % self.eng_value()


class BitFieldFloat(BitFieldReal):

    def __init__(self, name, default = None):
        BitFieldReal.__init__(self, name, __STRUCT_FLOAT_FMT__, default)

class BitFieldDouble(BitFieldReal):

    def __init__(self, name, default = None):
        BitFieldReal.__init__(self, name, __STRUCT_DOUBLE_FMT__, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
