#!/usr/bin/env python
#
# @file    BitFieldInteger.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Tue Oct 13, 2009 12:03
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


__doc__ = '''

    Signed and unsigned integer bit fields.

    This module provides classes to define signed and unsigned
    integers bit fields, from 8-bit to 64-bit.

    In order to encode and decode integer values, the Python's
    'struct' module is used. So, the conversion from binary data to
    integer values depends on that module.


    SIGNED and UNSIGNED INTEGERS

    Multiple signed and unsigned integer classes are available. It is,
    for example, very easy to create a new 16-bit signed integer bit
    field:

    >>> value = BFInt16('int16', -1345)
    >>> print value
    (int16 = -1345)

    or a 16-bit unsigned one:

    >>> value = BFUInt16('uint16', 0x8000)
    >>> print value
    (uint16 = 32768)

'''

import struct

from BitFieldStruct import BitFieldStruct

from BitFieldBase import _hex_string


__STRUCT_INT8_FMT__ = 'b'
__STRUCT_UINT8_FMT__ = 'B'
__STRUCT_INT16_FMT__ = 'h'
__STRUCT_UINT16_FMT__ = 'H'
__STRUCT_INT32_FMT__ = 'i'
__STRUCT_UINT32_FMT__ = 'I'
__STRUCT_INT64_FMT__ = 'q'
__STRUCT_UINT64_FMT__ = 'Q'


class BitFieldInteger(BitFieldStruct):

    def __init__(self, name, format, default = 0):
        BitFieldStruct.__init__(self, name, 1, format)
        self.set_value(default)

    def str_value(self):
        '''
        Returns a human-readable representation for the integer value.
        '''
        return '%d' % self.value()

    def str_eng_value(self):
        '''
        Returns a human-readable representation for the engineering
        value.

        The engineering values is, by default, represented as an
        integer value.
        '''
        return '%d' % self.eng_value()

class BFInt8(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT8_FMT__, default)

class BFUInt8(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT8_FMT__, default)

class BFInt16(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT16_FMT__, default)

class BFUInt16(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT16_FMT__, default)

class BFInt32(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT32_FMT__, default)

class BFUInt32(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT32_FMT__, default)

class BFInt64(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_INT64_FMT__, default)

class BFUInt64(BitFieldInteger):

    def __init__(self, name, default = 0):
        BitFieldInteger.__init__(self, name, __STRUCT_UINT64_FMT__, default)



class BitFieldIntegerList(BitFieldStruct):

    def __init__(self, name, size, BFIntegerType, default = None):
        # Create an instance of the base integer type.
        self.__object = BFIntegerType(name)

        BitFieldStruct.__init__(self, name, size,
                                self.__object._base_format())

        if default:
            self.set_value(default)

    def set_value(self, values):
        try:
            BitFieldStruct.set_value(self, *values)
        except struct.error, detail:
            raise struct.error, "%s (%d given)" % (detail, len(values))

    def str_value(self):
        return ['%d' % value for value in self.value()]

    def str_hex_value(self):
        byte_size = self.__object.byte_size()
        return [_hex_string(value, byte_size) for value in self.hex_value()]

    def str_eng_value(self):
        return ['%d' % value for value in self.eng_value()]

    def write(self):
        field = self.__object
        field.set_calibration_curve(self.calibration_curve())
        values = self.value()
        s = self.writer().start_block(self)
        for i in range(len(values)):
            field.set_name("%s[%d]" % (self.name(), i))
            field.set_value(values[i])
            # Inherit parent writer
            field.set_writer(self.writer())
            s += '\n' + field.write()
        s += self.writer().end_block(self)
        return s


class BFInt8List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFInt8, default)

class BFUInt8List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFUInt8, default)

class BFInt16List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFInt16, default)

class BFUInt16List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFUInt16, default)

class BFInt32List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFInt32, default)

class BFUInt32List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFUInt32, default)

class BFInt64List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFInt64, default)

class BFUInt64List(BitFieldIntegerList):

    def __init__(self, name, size, default = None):
        BitFieldIntegerList.__init__(self, name, size, BFUInt64, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
