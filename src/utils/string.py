#!/usr/bin/env python
#
# @file    string.py
# @brief   Helper functions for text strings
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Fri Dec 11, 2009 18:07
#
# Copyright (C) 2009, 2010 Aleix Conchillo Flaque
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

def hex_string(number, byte_size):
    hex_size = byte_size * 2
    return "0x%0*X" % (hex_size, number)

def wrap_string(string, length):
    if len(string) > length:
        output = string[0:length - 3]
        output += "..."
    else:
        output = string
    return output
