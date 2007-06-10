#!/usr/bin/env python
#
# @file    __init__.py
# @brief   Dummy file to make BitPacket a package
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Jun 10, 2007 21:31
#
# Copyright (C) 2007 Aleix Conchillo Flaque
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

__version__ = '0.1.0'

__all__ = [
    'BitField',
    'BitStructure'
    ]

from BitPacket.BitField import BitField
from BitPacket.BitStructure import BitStructure
from BitPacket.BitStructure import BitVariableStructure
