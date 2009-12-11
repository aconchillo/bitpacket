#!/usr/bin/env python
#
# @file    BitField.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 12:34
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

    Single bit fields.

    A packet might be formed by multiple fields that could be single
    bit fields, integer fields, structure fields, etc.

    An example of a packet could be:

    +-------+-----------+
    |  id   |  address  |
    +-------+-----------+
     <- 8 -> <--- 32 --->

    That is, a packet with two fields:

        - Identifier: 8 bits
        - Memory address: 32 bits

    The first field could be constructed by the following piece of
    code:

    >>> bf = BitField('id', 8, 0x54)
    >>> bf.value() == 0x54
    True

    that would create a BitField instance of a field named 'id' of 1
    byte size and value 0x54.

'''

from utils.binary import byte_end, bin_to_int, int_to_bin
from utils.string import hex_string

from Field import Field

from FieldType import FieldTypeBit

class BitField(Field):
    '''
    This class represents a single bit field to be used together with
    other BitFieldBase sub-classes, such as BitStructure, in order to
    build bigger fields.
    '''

    def __init__(self, name, size, default = 0):
        '''
        Initializes the field with the given 'name' and 'size' (in
        bits). By default the field's value will be initialized to 0
        or to 'default' if specified.
        '''
        Field.__init__(self, name, FieldTypeBit)
        self.__bits = []
        self.__size = size
        self.set_value(default)

    def value(self):
        '''
        Returns the value of this field. As single bit fields do not
        have a concrete type (signed integers, float...) this will
        return the hexadecimal integer representation of this field.

        This is the same as calling 'hex_value'.
        '''
        return bin_to_int(self.__bits)

    def set_value(self, value):
        '''
        Sets a new integer 'value' to the field.
        '''
        self.__bits = int_to_bin(value, self.size())

    def binary(self):
        '''
        Returns a binary string representing this field. The binary
        string is a sequence of 0's and 1's.
        '''
        return self.__bits

    def set_binary(self, binary):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's.
        '''
        self.__bits = binary[:self.size()]

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.__size

    def str_value(self):
        return str(self.value())

    def str_hex_value(self):
        return hex_string(self.hex_value(), byte_end(self.size()))

    def str_eng_value(self):
        return hex_string(self.eng_value(), byte_end(self.size()))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
