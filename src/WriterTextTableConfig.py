#!/usr/bin/env python
#
# @file    WriterTableConfig.py
# @brief   Configuration parameters for table writers
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Feb 02, 2010 15:40
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

    **API reference**: :class:`WriterTextTableConfig`

'''

from WriterTextStreamConfig import WriterTextStreamConfig

__TABLE_NAME_SIZE__ = 25
__TABLE_CLASS_SIZE__ = 15
__TABLE_SIZE_SIZE__ = 4
__TABLE_VALUE_SIZE__ = 20

class WriterTextTableConfig(WriterTextStreamConfig):

    def __init__(self, config = {}):
        self.table_name_size = __TABLE_NAME_SIZE__
        self.table_class_size = __TABLE_CLASS_SIZE__
        self.table_size_size = __TABLE_SIZE_SIZE__
        self.table_value_size = __TABLE_VALUE_SIZE__
        WriterTextStreamConfig.__init__(self, config)
