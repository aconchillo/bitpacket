#!/usr/bin/env python
#
# @file    Value.py
# @brief   An abstract class for numeric values (integer or real)
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Tue Oct 13, 2009 12:02
#
# Copyright (C) 2009, 2010, 2011, 2012 Aleix Conchillo Flaque
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

    An abstract class for numeric values (integer or real).

    **API reference**: :class:`Value`

    This is the base class for numeric fields. Internally, it uses
    Python's struct module to define the numeric value size and the byte
    order (little-endian or big-endian).

    The following code creates an 32-bit unsigned integer with a
    little-endian byte ordering.

    >>> v32 = Value("value", "<I", 67436735)
    >>> print v32
    (value = 67436735)

    Fortunately, BitPacket already defines most of numeric values that
    are commonly used.

'''

import struct

from BitPacket.utils.compatibility import *

from BitPacket.utils.string import hex_string
from BitPacket.utils.stream import read_stream, write_stream

from BitPacket.Field import Field

# Character     Byte order               Size and alignment
# @             native                   native
# =             native                   standard
# <             little-endian            standard
# >             big-endian               standard
# !             network (= big-endian)   standard

class Value(Field):
    '''
    This is the base class for numeric fields. Internally, it uses
    Python's struct module to define the numeric value size and the byte
    order (little-endian or big-endian).
    '''

    def __init__(self, name, format, value):
        '''
        Initialize the field with the given *name* and *value*. The
        *format* is a string conforming the Python's struct module
        format strings.
        '''
        Field.__init__(self, name)

        # This will store the string of bytes
        self.__bytes = ""

        # Calculate byte size from struct type
        self.__format = format
        self.__size = struct.calcsize(self.__format)

        # Finally set default value
        self.set_value(value)

    def _encode(self, stream, context):
        write_stream(stream, self.size(), self.__bytes)

    def _decode(self, stream, context):
        self.__bytes = read_stream(stream, self.size())

    def value(self):
        '''
        Returns the numeric value of this field.
        '''
        value = struct.unpack(self.__format, self.__bytes)
        return value[0]

    def set_value(self, value):
        '''
        Sets the new numeric *value* to this field. The value must fit
        in this field, otherwise an exception is raised.
        '''
        bytes = struct.pack(self.__format, value)
        self.set_bytes(bytes)

    def hex_value(self):
        '''
        Returns the hexadecimal integer representation of this
        field. That is, the bytes forming this field in its integer
        representation. This will vary depending on the field's
        endiannes and size, so :class:`UInt16LE` will return a different
        hexadecimal value than :class:`UInt16BE` for the same number.
        '''
        value = 0
        for c in self.__bytes:
            value = (value << 8) + u_ord(c)
        return value

    def size(self):
        '''
        Returns the size in bytes of this field.
        '''
        return self.__size

    def str_value(self):
        '''
        Returns a human-readable representation of the numeric value of
        this field.
        '''
        return str(self.value())

    def str_hex_value(self):
        '''
        Returns a human-readable representation of the hexadecimal
        representation of this field. This internally uses
        *hex_value()*.
        '''
        return hex_string(self.hex_value(), self.size())

    def str_eng_value(self):
        '''
        Returns a human-readable representation of the engineering
        value. This function will first calculate the engineering
        value (by applying the calibration curve) and will return the
        string representation of it.
        '''
        return str(self.eng_value())
