#!/usr/bin/env python
#
# @file    WriterBasic.py
# @brief   A writer implementation to somewhat like s-expressions
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

    **API reference**: :class:`WriterTextBasic`

'''

from utils.compatibility import *

from WriterTextStream import WriterTextStream

class WriterTextBasic(WriterTextStream):

    def start_block(self, field):
        if self.level() > 0:
            self.stream().write(self.config().newline)
        self.indent()
        WriterTextStream.start_block(self, field)

        try:
            str_hex = field.str_hex_value()
        except:
            str_hex = ""
        self.stream().write(str("(%s = %s") % (field.name(), str_hex))

    def end_block(self, field):
        WriterTextStream.end_block(self, field)
        self.stream().write(str(")"))

    def write(self, field):
        if self.level() > 0:
            self.stream().write(self.config().newline)
        self.indent()
        self.stream().write(str("(%s = %s)") % (field.name(), field.str_value()))
