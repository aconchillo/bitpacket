#!/usr/bin/env python
#
# @file    callable.py
# @brief   Helper functions to check callable parameters
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Fri Mar 09, 2012 00:53
#
# Copyright (C) 2012 Aleix Conchillo Flaque
#
# This file is part of BitPacket and has been copied from the
# construct project and updated (http://construct.wikispaces.com).
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

def param_call(param, ctx):
    if callable(param):
        return param(ctx)
    else:
        return param
