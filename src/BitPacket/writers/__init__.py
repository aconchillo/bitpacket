#
# @file    __init__.py
# @brief   An set of writers to reprsent bit structures.
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Tue Aug 2, 2011 10:46
#
# Copyright (C) 2010, 2011 Aleix Conchillo Flaque
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

from BitPacket.writers.Writer import Writer
from BitPacket.writers.WriterConfig import WriterConfig
from BitPacket.writers.WriterTextBasic import WriterTextBasic
from BitPacket.writers.WriterTextStream import WriterTextStream
from BitPacket.writers.WriterTextStreamConfig import WriterTextStreamConfig
from BitPacket.writers.WriterTextTable import WriterTextTable
from BitPacket.writers.WriterTextTableConfig import WriterTextTableConfig
from BitPacket.writers.WriterTextXML import WriterTextXML

__HAVE_GTK = True
try:
    from BitPacket.writers.WriterGtkTreeModel import WriterGtkTreeModel
    from BitPacket.writers.WriterGtkTreeView import WriterGtkTreeView
except ImportError as e:
    __HAVE_GTK = False

__all__ =   [ "Writer",
              "WriterConfig",
              "WriterTextStream",
              "WriterTextStreamConfig",
              "WriterTextBasic",
              "WriterTextTable",
              "WriterTextTableConfig",
              "WriterTextXML" ]

if __HAVE_GTK:
    __all__.extend([ "WriterGtkTreeModel",
                     "WriterGtkTreeView" ])
