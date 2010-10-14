#!/usr/bin/env python
#
# @file    compatibility.py
# @brief   Py3k and Python 2.6 compatibility
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Thu Oct 14, 2010 12:57
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

import sys

try:
    str = unicode
except NameError:
    pass

def u_ord(c):
    if sys.hexversion >= 0x03000000:
        return c
    else:
        return ord(c)
