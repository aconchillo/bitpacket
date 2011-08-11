#!/usr/bin/env python
#
# @file    WriterTable.py
# @brief   A writer implementation to text tables
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Aug 05, 2009 17:37
#
# Copyright (C) 2009, 2010, 2011 Aleix Conchillo Flaque
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

from BitPacket.utils.compatibility import *
from BitPacket.utils.string import wrap_string

from BitPacket.writers.WriterTextStream import WriterTextStream
from BitPacket.writers.WriterTextTableConfig import WriterTextTableConfig

class WriterTextTable(WriterTextStream):

    def __init__(self, stream, config = WriterTextTableConfig()):
        WriterTextStream.__init__(self, stream, config)

    def write(self, field, userdata = None):
        self.__field(field, userdata)

    def __header(self, userdata):
        table_size_size = self.config().table_size_size
        table_name_size = self.config().table_name_size
        table_class_size = self.config().table_class_size
        table_value_size = self.config().table_value_size

        s = str("| %-*s | %-*s | %-*s | %*s | %*s | %*s |") \
            % (table_name_size,
               wrap_string("Name", table_name_size),
               table_class_size,
               wrap_string("Class", table_class_size),
               table_size_size, "Size",
               table_value_size, "Hex",
               table_value_size, "Raw",
               table_value_size, "Eng")
        self.stream().write(s)
        self.stream().write(self.config().newline)

        s = str("+-%s-+-%s-+-%s-+-%s-+-%s-+-%s-+") \
            % ("-" * table_name_size,
               "-" * table_class_size,
               "-" * table_size_size,
               "-" * table_value_size,
               "-" * table_value_size,
               "-" * table_value_size)
        self.stream().write(s)
        self.stream().write(self.config().newline)

    def __field(self, field, userdata):
        if self.level() == 0:
            self.__header(userdata)
        else:
            self.stream().write(self.config().newline)

        # First we write the field
        self.__field_line(field, userdata)

        # Then, its children, if any.
        subfields = field.fields()
        if len(subfields) > 0:
            self.start_block(field, userdata)
            for f in subfields:
                self.write(f, userdata)
            self.end_block(field, userdata)

    def __field_line(self, field, userdata):
        table_name_size = self.config().table_name_size
        table_class_size = self.config().table_class_size
        table_size_size = self.config().table_size_size
        table_value_size = self.config().table_value_size
        name_size = table_name_size - self.indentation()

        try:
            str_hex = field.str_hex_value()
            str_raw = field.str_value()
            str_eng = field.str_eng_value()
        except:
            str_hex = ""
            str_raw = ""
            str_eng = ""

        self.stream().write(str("| "))
        self.indent()
        s = str("%-*s | %-*s | %*d | %*s | %*s | %*s |") \
            % (name_size,
               wrap_string(field.name(), name_size),
               table_class_size,
               wrap_string(field.__class__.__name__,
                           table_class_size),
               table_size_size, field.size(),
               table_value_size,
               wrap_string(str_hex, table_value_size),
               table_value_size,
               wrap_string(str_raw, table_value_size),
               table_value_size,
               wrap_string(str_eng, table_value_size))
        self.stream().write(s)


