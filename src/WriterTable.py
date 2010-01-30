#!/usr/bin/env python
#
# @file    WriterTable.py
# @brief   A writer implementation to text tables
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

    Text tables
    ===========

'''

from utils.string import wrap_string

from Writer import Writer


__TABLE_NAME_SIZE__ = 25
__TABLE_CLASS_SIZE__ = 15
__TABLE_HEX_SIZE__ = 20
__TABLE_STR_SIZE__ = 20


class WriterTable(Writer):

    def start_block(self, field, stream):
        name_size = __TABLE_NAME_SIZE__ - self.indentation()
        if self.indentation() > 0:
            stream.write(self.config().newline)
        stream.write("| ")
        self.indent(stream)
        Writer.start_block(self, field, stream)
        s = "%-*s | %-*s | %4d | %*s | %*s | %*s |" \
            % (name_size,
               wrap_string(field.name(), name_size),
               __TABLE_CLASS_SIZE__,
               wrap_string(field.__class__.__name__, __TABLE_CLASS_SIZE__),
               field.size(),
               __TABLE_HEX_SIZE__, "",
               __TABLE_STR_SIZE__, "",
               __TABLE_STR_SIZE__, "")
        stream.write(s)

    def write(self, field, stream):
        name_size = __TABLE_NAME_SIZE__ - self.indentation()
        stream.write(self.config().newline)
        stream.write("| ")
        self.indent(stream)
        s = "%-*s | %-*s | %4d | %*s | %*s | %*s |" \
            % (name_size,
               wrap_string(field.name(), name_size),
               __TABLE_CLASS_SIZE__,
               wrap_string(field.__class__.__name__, __TABLE_CLASS_SIZE__),
               field.size(),
               __TABLE_HEX_SIZE__,
               wrap_string(field.str_hex_value(), __TABLE_HEX_SIZE__),
               __TABLE_STR_SIZE__,
               wrap_string(field.str_value(), __TABLE_STR_SIZE__),
               __TABLE_STR_SIZE__,
               wrap_string(field.str_eng_value(), __TABLE_STR_SIZE__))
        stream.write(s)
