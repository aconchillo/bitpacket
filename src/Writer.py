#!/usr/bin/env python
#
# @file    Writer.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Wed Aug 05, 2009 17:37
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

    Writers
    =======

'''

from WriterConfig import WriterConfig

class Writer:
    '''
    This the abstract class for all bit fields sub-classes. All bit
    fields must inherit from this class and implement the
    non-implemented methods in it.
    '''

    def __init__(self, config = WriterConfig()):
        self.__config = config
        self.__indent = 0

    def config(self):
        return self.__config

    def start_block(self, field, stream):
        self.__indent += 1

    def end_block(self, field, stream):
        self.__indent -= 1

    def write(self, field, stream):
        '''
        Returns the name of the field.
        '''
        raise NotImplementedError

    def indent(self, stream):
        return stream.write(" " * self.indentation())

    def indentation(self):
        return self.config().indentation * self.__indent
