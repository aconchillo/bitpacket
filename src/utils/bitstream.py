#!/usr/bin/env python
#
# @file    bitstream.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 18:07
#
# Copyright (C) 2009 Aleix Conchillo Flaque
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

from binary import encode_bin, decode_bin

class BitStreamReader(object):

    def __init__(self, substream):
        self.__substream = substream
        self.__total_size = 0
        self.__buffer = ""

    def close(self):
        if self.__total_size % 8 != 0:
            raise ValueError("Total size of read data must be a multiple "
                             "of 8 (%d given)" % self.__total_size)

    def tell(self):
        return self.__substream.tell()

    def seek(self, pos, whence = 0):
        self.__buffer = ""
        self.__total_size = 0
        self.__substream.seek(pos, whence)

    def read(self, count):
        assert count >= 0
        l = len(self.__buffer)
        if count == 0:
            data = ""
        elif count <= l:
            data = self.__buffer[:count]
            self.__buffer = self.__buffer[count:]
        else:
            data = self.__buffer
            count -= l
            bytes = count // 8
            if count & 7: 
                bytes += 1
            buf = encode_bin(self.__substream.read(bytes))
            data += buf[:count]
            self.__buffer = buf[count:]
        self.__total_size += len(data)
        return data


class BitStreamWriter(object):

    def __init__(self, substream):
        self.__substream = substream
        self.__buffer = []
        self.__pos = 0

    def close(self):
        self.flush()

    def flush(self):
        bytes = decode_bin("".join(self.__buffer))
        self.__substream.write(bytes)
        self.__buffer = []
        self.__pos = 0

    def tell(self):
        return self.__substream.tell() + self.__pos // 8

    def seek(self, pos, whence = 0):
        self.flush()
        self.__substream.seek(pos, whence)

    def write(self, data):
        if not data:
            return
        if type(data) is not str:
            raise TypeError("Data must be a string, not %r" % type(data))
        self.__buffer.append(data)
