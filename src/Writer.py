#!/usr/bin/env python
#
# @file    Writer.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Wed Aug 05, 2009 17:37
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


__DEFAULT_INDENTATION__ = 2


class Writer:
    '''
    This the abstract class for all bit fields sub-classes. All bit
    fields must inherit from this class and implement the
    non-implemented methods in it.
    '''

    def __init__(self):
        self.__indent = 0

    def start_block(self, field):
        s = self.indentation()
        self.__indent += 1
        return s

    def end_block(self, field):
        self.__indent -= 1
        return self.indentation()

    def write(self, field):
        '''
        Returns the name of the field.
        '''
        raise NotImplementedError

    def indentation(self):
        s = ''
        for i in range(self.__indent):
            s += ' ' * __DEFAULT_INDENTATION__
        return s
