#!/usr/bin/env python
#
# @file    BitFieldReal.py
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

    Float and double bit fields.

    This module provides classes to define float (32-bit) and double
    (64-bit) bit fields.

    In order to encode and decode real values, the Python's 'struct'
    module is used. So, the conversion from binary data to real values
    depends on that module.


    32-BIT and 64-BIT REAL VALUES

    A float value can be easily created with the BitFieldFloat class:

    >>> value = BFFloat('f', 1.967834)
    >>> print value
    (f = 1.96783)

    Some times, it is also useful to see the hexadecimal value that
    forms this float number.

    >>> print value.str_hex_value()
    0x3FFBE1FC

    The same might be applied for doubles:

    >>> value = BFDouble('f', 0.0087552)
    >>> print value
    (f = 0.0087552)

'''

import struct

from BitFieldStruct import BitFieldStruct

from BitFieldBase import _hex_string


__STRUCT_FLOAT_FMT__ = 'f'
__STRUCT_DOUBLE_FMT__ = 'd'


class BitFieldReal(BitFieldStruct):

    def __init__(self, name, format, default = 0.0):
        BitFieldStruct.__init__(self, name, 1, format)
        self.set_value(default)

    def str_value(self):
        '''
        Returns a human-readable representation for the float value.

        The value is rounded and converted to decimal notation in the
        style [-]ddd.ddd or [-]d.ddde[+-]dd depeding on the exponent.

        See 'printf' documentation for 'g' format.
        '''
        return '%g' % self.value()

    def str_eng_value(self):
        '''
        Returns a human-readable representation for the engineering
        value.

        The engineering values is, by default, represented as a real
        value.

        The value is rounded and converted to decimal notation in the
        style [-]ddd.ddd or [-]d.ddde[+-]dd depeding on the exponent.

        See 'printf' documentation for 'g' format.
        '''
        return '%g' % self.eng_value()


class BFFloat(BitFieldReal):

    def __init__(self, name, default = 0.0):
        BitFieldReal.__init__(self, name, __STRUCT_FLOAT_FMT__, default)

class BFDouble(BitFieldReal):

    def __init__(self, name, default = 0.0):
        BitFieldReal.__init__(self, name, __STRUCT_DOUBLE_FMT__, default)




class BitFieldRealList(BitFieldStruct):

    def __init__(self, name, size, BFRealType, default = None):
        # Create an instance of the base real type.
        self.__object = BFRealType(name)

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
        return ['%g' % value for value in self.value()]

    def str_hex_value(self):
        byte_size = self.__object.byte_size()
        return [_hex_string(value, byte_size) for value in self.hex_value()]

    def str_eng_value(self):
        return ['%g' % value for value in self.eng_value()]

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


class BFFloatList(BitFieldRealList):

    def __init__(self, name, size, default = None):
        BitFieldRealList.__init__(self, name, size, BFFloat, default)

class BFDoubleList(BitFieldRealList):

    def __init__(self, name, size, default = None):
        BitFieldRealList.__init__(self, name, size, BFDouble, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
