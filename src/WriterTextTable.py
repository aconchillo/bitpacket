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

    **API reference**: :class:`WriterTextTable`

'''

from utils.string import wrap_string

from WriterStream import WriterStream
from WriterTextTableConfig import WriterTextTableConfig

class WriterTextTable(WriterStream):

    def __init__(self, config = WriterTextTableConfig()):
        WriterStream.__init__(self, config)

    def start_block(self, field, stream):
        table_name_size = self.config().table_name_size
        table_class_size = self.config().table_class_size
        table_size_size = self.config().table_size_size
        table_value_size = self.config().table_value_size

        name_size = table_name_size - self.indentation()
        if self.level() == 0:
            self.__header(stream)
        else:
            stream.write(self.config().newline)

        stream.write("| ")
        self.indent(stream)
        WriterStream.start_block(self, field, stream)
        s = "%-*s | %-*s | %*d | %*s | %*s | %*s |" \
            % (name_size,
               wrap_string(field.name(), name_size),
               table_class_size,
               wrap_string(field.__class__.__name__, table_class_size),
               table_size_size, field.size(),
               table_value_size, "",
               table_value_size, "",
               table_value_size, "")
        stream.write(s)

    def write(self, field, stream):
        table_name_size = self.config().table_name_size
        table_class_size = self.config().table_class_size
        table_size_size = self.config().table_size_size
        table_value_size = self.config().table_value_size

        name_size = table_name_size - self.indentation()
        if self.level() > 0:
            stream.write(self.config().newline)
        stream.write("| ")
        self.indent(stream)
        s = "%-*s | %-*s | %*d | %*s | %*s | %*s |" \
            % (name_size,
               wrap_string(field.name(), name_size),
               table_class_size,
               wrap_string(field.__class__.__name__, table_class_size),
               table_size_size, field.size(),
               table_value_size,
               wrap_string(field.str_hex_value(), table_value_size),
               table_value_size,
               wrap_string(field.str_value(), table_value_size),
               table_value_size,
               wrap_string(field.str_eng_value(), table_value_size))
        stream.write(s)

    def __header(self, stream):
        table_size_size = self.config().table_size_size
        table_name_size = self.config().table_name_size
        table_class_size = self.config().table_class_size
        table_value_size = self.config().table_value_size

        s = "| %-*s | %-*s | %-*s | %*s | %*s | %*s |" \
            % (table_name_size,
               wrap_string("Name", table_name_size),
               table_class_size,
               wrap_string("Class", table_class_size),
               table_size_size, "Size",
               table_value_size, "Hex",
               table_value_size, "Raw",
               table_value_size, "Eng")
        stream.write(s)
        stream.write(self.config().newline)

        s = "+-%s-+-%s-+-%s-+-%s-+-%s-+-%s-+" \
            % ("-" * table_name_size,
               "-" * table_class_size,
               "-" * table_size_size,
               "-" * table_value_size,
               "-" * table_value_size,
               "-" * table_value_size)
        stream.write(s)
        stream.write(self.config().newline)


