#!/usr/bin/env python
#
# @file    WriterXML.py
# @brief   A writer implementation to XML
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

    **API reference**: :class:`WriterTextXML`

'''

from utils.compatibility import *
     
from writers.WriterTextStream import WriterTextStream


class WriterTextXML(WriterTextStream):

    def start_block(self, field, userdata = None):
        WriterTextStream.start_block(self, field, userdata)
        try:
            s = str('<container name="%s" class="%s" size="%d" value="%s">') \
                % (field.name(), field.__class__.__name__, field.size(),
                   field.str_hex_value())
        except:
            s = str('<container name="%s" class="%s" size="%d">') \
                % (field.name(), field.__class__.__name__, field.size())
        self.stream().write(s)
        self.stream().write(self.config().newline)

    def end_block(self, field, userdata = None):
        WriterTextStream.end_block(self, field, userdata)
        self.indent()
        self.stream().write(str("</container>"))
        if self.level() > 0:
            self.stream().write(self.config().newline)

    def write(self, field, userdata = None):
        self.indent()

        subfields = field.fields()
        if len(subfields) > 0:
            self.start_block(field, userdata)
            for f in subfields:
                self.write(f, userdata)
            self.end_block(field, userdata)
        else:
            self.__field_line(field, userdata)

    def __field_line(self, field, userdata):
        s = str('<field name="%s" class="%s" size="%d">') \
            % (field.name(), field.__class__.__name__, field.size())
        self.stream().write(s)
        self.stream().write(self.config().newline)

        WriterTextStream.start_block(self, field, userdata)
        self.indent()
        self.stream().write(str("<hex_value>%s</hex_value>") % field.str_hex_value())
        self.stream().write(self.config().newline)

        self.indent()
        self.stream().write(str("<value>%s</value>") % field.str_value())
        self.stream().write(self.config().newline)

        self.indent()
        self.stream().write(str("<eng_value>%s</eng_value>") % field.str_eng_value())
        self.stream().write(self.config().newline)
        WriterTextStream.end_block(self, field, userdata)

        self.indent()
        self.stream().write(str("</field>"))
        if self.level() > 0:
            self.stream().write(self.config().newline)
