#!/usr/bin/env python
#
# @file    stream.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 12:31
#
# Copyright (C) 2007-2009 Aleix Conchillo Flaque
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

def read_stream(stream, length):
    if length < 0:
        raise ValueError("data length to read must be >= 0")
    data = stream.read(length)
    if len(data) != length:
        raise ValueError("data length mismatch (%d expected, %d read)" \
                             % (length, len(data)))
    return data

def write_stream(stream, length, data):
    if length < 0:
        raise ValueError("data length to write must be >= 0")
    if len(data) != length:
        raise ValueError("data length mismatch (%d expected, %d found)" \
                             % (length, len(data)))
    stream.write(data)
