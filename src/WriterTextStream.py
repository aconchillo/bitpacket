#!/usr/bin/env python
#
# @file    WriterTextStream.py
# @brief   Base class for text stream-oriented field writers
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
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

    **API reference**: :class:`WriterTextStream`

'''

from utils.compatibility import *

from Writer import Writer
from WriterTextStreamConfig import WriterTextStreamConfig

class WriterTextStream(Writer):

    def __init__(self, stream, config = WriterTextStreamConfig()):
        Writer.__init__(self, config)
        self.__stream = stream

    def stream(self):
        return self.__stream

    def indent(self):
        return self.stream().write(str(" ") * self.indentation())

    def indentation(self):
        return self.config().indentation * self.level()
