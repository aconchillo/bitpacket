#!/usr/bin/env python
#
# @file    WriterXML.py
# @brief   A writer implementation to XML
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

    XML
    ===

'''

from Writer import Writer


class WriterXML(Writer):

    def start_block(self, field, stream):
        self.indent(stream)
        Writer.start_block(self, field, stream)
        s = '<structure name="%s" class="%s" size="%d">' \
            % (field.name(), field.__class__.__name__, field.size())
        stream.write(s)
        stream.write(self.config().newline)

    def end_block(self, field, stream):
        Writer.end_block(self, field, stream)
        self.indent(stream)
        stream.write("</structure>")
        if self.indentation() > 0:
            stream.write(self.config().newline)

    def write(self, field, stream):
        self.indent(stream)
        s = '<field name="%s" class="%s" size="%d">' \
            % (field.name(), field.__class__.__name__, field.size())
        stream.write(s)
        stream.write(self.config().newline)

        Writer.start_block(self, field, stream)
        self.indent(stream)
        stream.write("<hex_value>%s</hex_value>" % field.str_hex_value())
        stream.write(self.config().newline)

        self.indent(stream)
        stream.write("<value>%s</value>" % field.str_value())
        stream.write(self.config().newline)

        self.indent(stream)
        stream.write("<eng_value>%s</eng_value>" % field.str_eng_value())
        stream.write(self.config().newline)
        Writer.end_block(self, field, stream)

        self.indent(stream)
        stream.write("</field>")
        if self.indentation() > 0:
            stream.write(self.config().newline)
