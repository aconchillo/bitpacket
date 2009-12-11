#!/usr/bin/env python
#
# @file    WriterXML.py
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

from Writer import Writer


class WriterXML(Writer):

    def start_block(self, field):
        s = Writer.start_block(self, field)
        s += '<structure name="%s" class="%s" type="%s" size="%d">' \
            % (field.name(), field.__class__.__name__,
               field.type(), field.size())
        return s

    def end_block(self, field):
        s = '\n'
        s += Writer.end_block(self, field)
        s += '</structure>'
        return s

    def write(self, field):
        s = self.indentation()
        s += '<field name="%s" class="%s" type="%s" size="%d" value="%s"/>' \
            % (field.name(), field.__class__.__name__,
               field.type(), field.size(), field.str_value())
        return s
