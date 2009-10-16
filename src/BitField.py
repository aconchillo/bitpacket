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
    bit fields, integer fields, structure fields or variable structure
    fields.

    An example of a packet could be:

    +-------+-----------+---------+------------------+
    |  id   |  address  | nbytes  |       data       |
    +-------+-----------+---------+------------------+
     <- 1 -> <--- 4 ---> <-- 2 --> <---- nbytes ---->

    That is, a packet with four fields:

        - Identifier: 1 byte
        - Memory address: 4 bytes
        - Number of data bytes: 2 bytes
        - Data: number of data bytes

    The first field could be constructed by the following piece of
    code:

    >>> bf = BitField('id', 8, 0x54)
    >>> bf.value() == 0x54
    True

    that would create a BitField instance of a field named 'id' of 1
    byte size and value 0x54.

    Also, the BitFieldByte class might be useful for creating
    byte-sized fields. So, following the last example:

    >>> bf = BitFieldByte('id', 1, 0x54)
    >>> bf.value() == 0x54
    True


    UNPACKING SINGLE BIT FIELDS

    In order to unpack a single field from a data buffer, one would
    create a BitField without any initialization and assign the data
    buffer when ready:

    >>> data = array.array('B', [0x35])
    >>> bf = BitField('id', 8)
    >>> bf.set_array(data)
    >>> bf.array()
    array('B', [53])
    >>> print bf
    (id = 0x35)
    >>> bf.set_array(bf.array())
    >>> bf.set_value(bf.value())
    >>> print bf
    (id = 0x35)

'''

import array

from BitFieldBase import BitFieldBase
from BitFieldBase import _bin_to_int
from BitFieldBase import _int_to_bin
from BitFieldBase import _encode_array
from BitFieldBase import _decode_array

class BitField(BitFieldBase):
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
        BitFieldBase.__init__(self, name)
        self.__bits = []

        if size == 0:
            raise SizeError, 'Bit size must be at least 1'

        self.__size = size
        self.set_value(default)

    def value(self):
        '''
        Returns the value of this field. As single bit fields do not
        have a concrete type (signed integers, float...) this will
        return the hexadecimal integer representation of this field.

        This is the same as calling 'hex_value'.
        '''
        return self.hex_value()

    def set_value(self, value):
        '''
        Sets a new integer 'value' to the field.
        '''
        self.__bits = _int_to_bin(value, self.size())

    def array(self):
        '''
        Returns a byte array representing this field.
        '''
        if (self.size() & 7) != 0:
            raise ValueError, '"%s" size must be a multiple of 8' % self.name()
        return _decode_array(self.__bits)

    def set_array(self, data):
        '''
        Sets a byte array to the field. The array should be of type
        'B' (unsigned char).
        '''
        if (self.size() & 7) != 0:
            raise ValueError, '"%s" size must be a multiple of 8' % self.name()
        self.__bits = _encode_array(data, self.byte_size())

    def binary(self):
        '''
        Returns a binary string representing this field. The binary
        string is a sequence of 0's and 1's.
        '''
        return self.__bits

    def set_binary(self, bits):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's.
        '''
        self.__bits = bits

    def hex_value(self):
        '''
        Returns the hexadecimal integer representation of this
        field. That is, the bytes forming this field in its integer
        representation.
        '''
        return _bin_to_int(self.__bits)

    def str_value(self):
        '''
        Returns a human-readable representation of the value of this
        field. For single bit fields (base class) this is the
        hexadecimal representation.

        This is the same as calling 'str_hex_value'.
        '''
        return self.str_hex_value()

    def str_hex_value(self):
        '''
        Returns a human-readable representation of the hexadecimal
        values of this field.
        '''
        hex_size = self.byte_size() * 2
        return '0x%0*X' % (hex_size, self.hex_value())

    def str_eng_value(self):
        '''
        Returns a human-readable representation of the engineering
        value. This function will first calculate the engineering
        value (by applying the calibration curve) and will return the
        string representation of it.

        For single bit fields (base class) the hexadecimal
        representation is returned.
        '''
        hex_size = self.byte_size() * 2
        return '0x%0*X' % (hex_size, self.eng_value())

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.__size




# Size (in bits) of a byte
__BYTE_SIZE__ = 8

class BitFieldByte(BitField):
    '''
    This class is a helper BitField sub-class to create fields with
    byte-aligned sizes.
    '''

    def __init__(self, name, size, default = 0):
        '''
        Initializes the field with the given 'name' and 'size' (in
        bytes). By default the field's value will be initialized to 0
        or to 'default' if specified.
        '''
        BitField.__init__(self, name, size * __BYTE_SIZE__, default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
