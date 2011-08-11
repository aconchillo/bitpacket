#!/usr/bin/env python
#
# @file    WriterGtkTreeView.py
# @brief   An abstract class for field writers
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Tue Dec 14, 2010 16:25
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

    **API reference**: :class:`WriterGtkTreeView`

'''

import gtk

from BitPacket.writers.Writer import Writer
from BitPacket.writers.WriterGtkTreeModel import WriterGtkTreeModel

class WriterGtkTreeView(Writer):

    def __init__(self):
        Writer.__init__(self)
        self.__view = gtk.TreeView(model = None)
        self.__add_columns(self.__view)
        self.__model = None

    def view(self):
        return self.__view

    def write(self, field, userdata = None):
        self.__model = WriterGtkTreeModel(field)
        self.view().set_model(model = self.__model)

    def __add_columns(self, treeview):
        self.__add_column(treeview, WriterGtkTreeModel.NAME_COLUMN)
        self.__add_column(treeview, WriterGtkTreeModel.CLASS_COLUMN)
        self.__add_column(treeview, WriterGtkTreeModel.SIZE_COLUMN)
        self.__add_column(treeview, WriterGtkTreeModel.RAW_VALUE_COLUMN)
        self.__add_column(treeview, WriterGtkTreeModel.HEX_VALUE_COLUMN)
        self.__add_column(treeview, WriterGtkTreeModel.ENG_VALUE_COLUMN)

    def __add_column(self, treeview, index):
        column = gtk.TreeViewColumn(WriterGtkTreeModel.COLUMN_NAMES[index],
                                    gtk.CellRendererText(),
                                    text = index)
        treeview.append_column(column)


# class WriterGtkTreeDemo(gtk.Window):
#     def __init__(self, field, parent=None):
#         gtk.Window.__init__(self)
#         try:
#             self.set_screen(parent.get_screen())
#         except AttributeError:
#             self.connect('destroy', lambda *w: gtk.main_quit())
#         self.set_title(self.__class__.__name__)
#         self.set_default_size(700, 400)
#         self.set_border_width(8)

#         vbox = gtk.VBox(False, 8)
#         self.add(vbox)

#         sw = gtk.ScrolledWindow()
#         sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
#         sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
#         vbox.pack_start(sw)

#         # create treeview
#         writer = WriterGtkTreeView()
#         treeview = writer.view()
#         treeview.set_rules_hint(True)
#         writer.write(field)

#         sw.add(treeview)

#         # expand all rows after the treeview widget has been realized
#         treeview.connect('realize', lambda tv: tv.expand_all())

#         self.show_all()

##################################################

# import array

# from BitPacket.MetaField import *
# from BitPacket.Structure import Structure
# from BitPacket.Integer import *

# class Test(Structure):

#     def __init__(self):
#         Structure.__init__(self, "tesbabat")
#         self.append(UInt8("value1"))
#         self.append(UInt8("value2"))

# s = Structure("metastruct")
# ss = Structure("substruct")
# s.append(ss)

# f = MetaField("test", lambda ctx: Test())
# ss.append(f)

# s.set_array(array.array("B", [123, 124]))

##################################################

# import array

# from BitPacket.Integer import *
# from BitPacket.MetaData import *
# from BitPacket.MetaStructure import *
# from BitPacket.writers.WriterTextXML import *
# from BitPacket.writers.WriterTextTable import *

# class Test(Structure):

#     def __init__(self):
#         Structure.__init__(self, "test")
#         self.append(UInt8("counter"))
#         self.append(MetaStructure("address",
#                                   lambda ctx: self["counter"],
#                                   lambda ctx: UInt64("value")))

# s = Structure("a")
# s.append(UInt8("counter"))
# s.append(MetaStructure("struct",
#                        lambda ctx: ctx["counter"],
#                        lambda ctx: Test()))

# s.set_array(array.array("B", [2,
#                               1,
#                               1, 2, 3, 4, 1, 2, 3, 4,
#                               2,
#                               5, 6, 7, 8, 9, 10, 11, 12,
#                               13, 14, 15, 16, 17, 18, 19, 20]))

##################################################

# from BitPacket.Mask import *

# s =  Mask8("ValidityFlags", Mask, 0,
#            FLAG_1 = 0x01,
#            FLAG_2 = 0x02,
#            FLAG_3 = 0x04,
#            FLAG_4 = 0x08,
#            FLAG_5 = 0x10,
#            FLAG_6 = 0x20,
#            FLAG_7 = 0x40,
#            FLAG_8 = 0x80)

# s.mask(s.FLAG_1 | s.FLAG_2)

# def main():
#     WriterGtkTreeDemo(s)
#     gtk.main()

# if __name__ == '__main__':
#     main()
