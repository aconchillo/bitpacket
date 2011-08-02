#!/usr/bin/env python
#
# @file    WriterConfig.py
# @brief   Base configuration parameters for writers
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Fri Jan 22, 2010 10:34
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

    **API reference**: :class:`WriterConfig`

'''

class WriterConfig(object):

    def __init__(self, **kwargs):
        self.set_config(**kwargs)

    def set_config(self, **kwargs):
        for key in list(kwargs.keys()):
            if key in self.__dict__:
                if type(kwargs[key]) == type(self.__dict__[key]):
                    self.__dict__[key] = kwargs[key]
                else:
                    raise TypeError('Invalid type for "%s" configuration (%s != %s)' \
                                        % (key,
                                           type(kwargs[key]),
                                           type(self.__dict__[key])))
            else:
                raise KeyError('Invalid configuration parameter "%s"' % key)

    def __str__(self):
        return str(self.__dict__)
