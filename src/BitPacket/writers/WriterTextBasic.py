#!/usr/bin/env python
#
# @file    WriterBasic.py
# @brief   A writer implementation to somewhat like s-expressions
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
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

from BitPacket.utils.compatibility import *

from BitPacket.writers.WriterTextStream import WriterTextStream

class WriterTextBasic(WriterTextStream):

    def start_block(self, field, userdata = None):
        WriterTextStream.start_block(self, field, userdata)
        try:
            str_hex = field.str_hex_value()
        except:
            str_hex = ""
        self.stream().write(str("(%s = %s") % (field.name(), str_hex))

    def end_block(self, field, userdata = None):
        WriterTextStream.end_block(self, field, userdata)
        self.stream().write(str(")"))

    def write(self, field, userdata = None):
        if self.level() > 0:
            self.stream().write(self.config().newline)

        self.indent()

        subfields = field.fields()
        if len(subfields) > 0:
            self.start_block(field, userdata)
            for f in subfields:
                self.write(f, userdata)
            self.end_block(field, userdata)
        else:
            self.stream().write(str("(%s = %s)") % (field.name(),
                                                    field.str_value()))
