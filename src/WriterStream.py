#!/usr/bin/env python
#
# @file    WriterStream.py
# @brief   Base class for stream-oriented field writers
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Mar 12, 2010 14:57
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

    **API reference**: :class:`Stream`

'''

from Writer import Writer
from WriterStreamConfig import WriterStreamConfig

class WriterStream(Writer):

    def __init__(self, config = WriterStreamConfig()):
        Writer.__init__(self, config)

    def indent(self, stream):
        return stream.write(" " * self.indentation())

    def indentation(self):
        return self.config().indentation * self.level()
