#!/usr/bin/env python
#
# @file    WriterXML.py
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

from Writer import Writer


class WriterXML(Writer):

    def start_block(self, field):
        s = Writer.start_block(self, field)
        s += '<structure name="%s" class="%s" size="%d">' \
            % (field.name(), field.__class__.__name__, field.size())
        return s

    def end_block(self, field):
        s = '\n'
        s += Writer.end_block(self, field)
        s += '</structure>'
        return s

    def write(self, field):
        s = self.indentation()
        s += '<field name="%s" class="%s" size="%d">\n' \
            % (field.name(), field.__class__.__name__, field.size())

        Writer.start_block(self, field)
        value_indent = self.indentation()
        s += value_indent + '<value>%s</value>\n' % field.str_value()
        s += Writer.end_block(self, field)

        s += '</field>'
        return s
