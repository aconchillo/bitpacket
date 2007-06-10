#!/usr/bin/env python
#
# @file    Common.py
# @brief   Common useful type sizes
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Apr 01, 2007 12:53
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

BIT_SIZE = 1
BYTE_SIZE = BIT_SIZE * 8
WORD_SIZE = BYTE_SIZE * 2

# Chars
CHAR_SIZE = BYTE_SIZE
UNSIGNED_CHAR_SIZE = CHAR_SIZE
SIGNED_CHAR_SIZE = CHAR_SIZE

# Short integer
SHORT_SIZE = WORD_SIZE
UNSIGNED_SHORT_SIZE = SHORT_SIZE
SIGNED_SHORT_SIZE = SHORT_SIZE

# Integer
INTEGER_SIZE = SHORT_SIZE * 2
UNSIGNED_INTEGER_SIZE = INTEGER_SIZE
SIGNED_INTEGER_SIZE = INTEGER_SIZE
