#!/usr/bin/env python
#
# @file    WriterGtkTreeModel.py
# @brief   An abstract class for field writers
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Tue Dec 14, 2010 16:24
#
# Copyright (C) 2010 Aleix Conchillo Flaque
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

    **API reference**: :class:`WriterGtkTreeModel`

'''

import gtk
import gobject

class WriterGtkTreeModel(gtk.GenericTreeModel):

    # Available columns
    (NAME_COLUMN,
     CLASS_COLUMN,
     SIZE_COLUMN,
     RAW_VALUE_COLUMN,
     HEX_VALUE_COLUMN,
     ENG_VALUE_COLUMN,
     NUM_COLUMNS) = range(7)

    COLUMN_TYPES = (gobject.TYPE_STRING,
                    gobject.TYPE_STRING,
                    gobject.TYPE_INT,
                    gobject.TYPE_STRING,
                    gobject.TYPE_STRING,
                    gobject.TYPE_STRING)

    COLUMN_NAMES = ["Name", "Class", "Size", "Raw", "Hexadecimal", "Engineering"]

    def __init__(self, field):
        gtk.GenericTreeModel.__init__(self)
        self.__root = field

    def on_get_flags(self):
        return gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.COLUMN_TYPES)

    def on_get_column_type(self, n):
        return self.COLUMN_TYPES[n]

    def on_get_iter(self, path):
        node = self.__root
        for i in path[1:]:
            node = node.fields()[i]
        return node

    def on_get_path(self, rowref):
        path = []
        node = rowref
        while node:
            path.append(node.index())
            node = node.parent()
        return tuple(reversed(path))

    def on_get_value(self, rowref, column):
        try:
            str_hex = rowref.str_hex_value()
            str_raw = rowref.str_value()
            str_eng = rowref.str_eng_value()
        except:
            str_hex = ""
            str_raw = ""
            str_eng = ""

        values = {self.NAME_COLUMN : rowref.name(),
                  self.CLASS_COLUMN : rowref.__class__.__name__,
                  self.SIZE_COLUMN : rowref.size(),
                  self.HEX_VALUE_COLUMN : str_hex,
                  self.RAW_VALUE_COLUMN : str_raw,
                  self.ENG_VALUE_COLUMN : str_eng}

        return values[column]

    def on_iter_next(self, rowref):
        if rowref and rowref.parent():
            try:
                next = rowref.index() + 1
                return rowref.parent().fields()[next]
            except IndexError:
                return None
        return None

    def on_iter_children(self, parent):
        if parent:
            if len(parent.fields()) > 0:
                return parent.fields()[0]
        return self.__root

    def on_iter_has_child(self, rowref):
        if rowref:
            return len(rowref.fields()) > 0
        return False

    def on_iter_n_children(self, rowref):
        if rowref:
            return len(rowref.fields())
        return 1

    def on_iter_nth_child(self, parent, n):
        if parent:
            try:
                return parent.fields()[n]
            except IndexError:
                return None
        return self.__root

    def on_iter_parent(self, child):
        if child:
            return child.parent()
        return None
