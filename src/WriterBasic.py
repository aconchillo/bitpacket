#!/usr/bin/env python
#
# @file    WriterBasic.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Wed Aug 05, 2009 17:37
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

    Basic text
    ==========

'''

from Writer import Writer


class WriterBasic(Writer):

    def start_block(self, field):
        s = Writer.start_block(self, field)
        s += '(%s =' % field.name()
        return s

    def end_block(self, field):
        Writer.end_block(self, field)
        return ')'

    def write(self, field):
        s = self.indentation()
        s += '(%s = %s)' % (field.name(), field.str_value())
        return s
