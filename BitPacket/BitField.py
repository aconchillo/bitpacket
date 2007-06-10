#!/usr/bin/env python
#
# @file    BitField.py
# @brief   A simple bit field representation
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sat Mar 31, 2007 20:15
#
# Copyright (C) 2007 Aleix Conchillo Flaque
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

''' '''

__version__ = '0.1.0'
__date__    = 'Sat Mar 31, 2007 20:19'
__author__  = 'Aleix Conchillo Flaque <aleix@member.fsf.org>'
__copyright__ = 'Copyright (C) 2007 Aleix Conchillo Flaque'
__license__ = 'GPL'
__url__     = 'http://hacks-galore.org/aleix/BitPacket'

__doc__ = '''

    A simple bit field representation.

    INTRODUCTION

    This class represents a bit field to be used together with
    BitStructure and BitVariableStructure classes in order to build
    bit field structures.

    Note that some of the code found in this documentation might not
    be self-contained, it may depend on code explained in previous
    sections.


    SINGLE BIT FIELDS

    A packet might be formed by mutiple fields that could be single
    bit fields, integer fields, structure fields or variable structure
    fields.

    An example of a packet could be:

    +-------+-----------+---------+------------------+
    |  id   |  address  | nbytes  |       data       |
    +-------+-----------+---------+------------------+
     <- 1 -> <--- 4 ---> <-- 2 --> <---- nbytes ---->

    That is, a packet with four fields:

        - Indetifier: 1 byte
        - Memory address: 4 bytes
        - Number of data bytes: 2 bytes
        - Data: number of data bytes

    The first field could be constructed by the following piece of
    code:

    >>> bf = BitField('id', Common.BYTE_SIZE, 0x54)
    >>> bf.value() == 0x54
    True

    that would create a BitField instance of a field named 'id' of 1
    byte size and value 0x54.


    UNPACKING SINGLE BIT FIELDS

    In order to unpack a single field from a data buffer, one would
    create a BitField without any initialisation and assign the data
    buffer when ready:

    >>> data = array.array('B', [0x35])
    >>> bf = BitField('id', Common.BYTE_SIZE)
    >>> bf.set_array(data)
    >>> bf.array()
    array('B', [53])
    >>> print bf
    (id = 0x35)

'''

import math
import array
import Common

class BitField:
    '''
    This class represents a bit field to be used together with
    BitStructure and BitVariableStructure classes in order to build
    packets.
    '''

    def __init__(self, name, size, default = 0):
        '''
        Initializes the field with the given 'name' and 'size' (in
        bits). By default the field's value will be initialized to 0
        or to 'default' if specified.
        '''
        self._name = name
        self.__check_value_size(default, size)
        self.__size = size
        self.__value = default

    def name(self):
        '''
        Returns the name of the field.
        '''
        return self._name

    def value(self):
        '''
        Returns the integer value of the field.
        '''
        return self.__value

    def set_value(self, value, size = None):
        '''
        Sets a new integer 'value' to the field. An optional new bit
        'size' can also be specified.
        '''
        if size != None:
            self.__size = size
        self.__check_value_size(value, self.__size)
        self.__value = value

    def array(self):
        '''
        Returns a byte array (big-endian) representing this field.
        '''
        return _bignum_to_array(self.value(), self.byte_size())

    def set_array(self, data):
        '''
        Sets a byte array (big-endian) to the field. The array should
        be of type 'B' (unsigned char). This method will modify the
        field's size automatically depending on the array size.
        '''
        self.set_value(_array_to_bignum(data),
                       len(data) * Common.BYTE_SIZE)

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        return self.__size

    def byte_size(self):
        '''
        Returns the size of the field in bytes.
        '''
        byte_size = self.__size / 8
        if (self.__size % 8) > 0:
            byte_size += 1
        return byte_size

    def __str__(self, indent = 0):
        '''
        Prints the name and value of the field with an optional
        indentation.
        '''
        s = ""
        for i in range(indent):
            s += " "
        s += "(%s = 0x%X)" % (self._name, self.value())
        return s

    def __check_value_size(self, value, size):
        '''
        Checks if the given 'value' can be represented with the given
        'size', raises a ValueError exception if not.
        '''
        value_size = _value_bit_size(value)
        if (value != 0) and (size != 0) and (size <= value_size):
            raise ValueError,  '"%s" value 0x%0X needs at least %d bits (%d given)' \
                % (self._name, value, value_size, size)

def _value_bit_size(value):
    '''
    Returns the number of needed bits to represent the given 'value'.
    '''
    if value == 0:
        return 1
    else:
        return math.log(value, 2)

def _array_to_bignum(byte_array):
    '''
    Transforms an array of bytes (in big-endian) into an integer
    value.
    '''
    if byte_array.typecode != 'B':
        raise TypeError, 'Array type should be unsigned char'
    lst = byte_array.tolist()
    i = len(lst) - 1
    bignum = 0
    for byte in lst:
        bignum += byte * 2**(8*i)
        i -= 1
    return bignum

def _bignum_to_array(bignum, size):
    '''
    Transforms an integer value into an array of bytes (in
    big-endian).
    '''
    byte_mask = 0xFF
    data = array.array('B')
    for i in range(size):
        data.append( (bignum>>i*8) & byte_mask)
    data.reverse()
    return data


if __name__ == '__main__':
    import doctest
    doctest.testmod()
