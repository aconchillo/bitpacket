#!/usr/bin/env python
#
# @file    BitFieldBase.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 12:28
#
# Copyright (C) 2007, 2008, 2009 Aleix Conchillo Flaque
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

    An object-oriented representation of bit field structures.

    These classes represent simple bit fields, and fixed and variable
    structures of bit fields which might be used to construct
    packets. BitStructure and BitVariableStructure are BitField
    themselves and all of them can be used together. That is, we can
    add any BitField subclass into a BitStructure or
    BitVariableStructure.

    Note that some of the code found in this documentation might not
    be self-contained, it may depend on code explained in previous
    sections.

'''

import array

class BitFieldBase:
    '''
    This the abstract class for all bit fields sub-classes. All bit
    fields must inherit from this class and implement the
    non-implemented methods in it.
    '''

    def __init__(self, name, writer = None):
        '''
        '''
        self._name = name
        self.__writer = writer

    def name(self):
        '''
        Returns the name of the field.
        '''
        return self._name

    def value(self):
        '''
        Returns the integer value of the field.
        '''
        raise NotImplementedError

    def set_value(self, value):
        '''
        Sets a new integer 'value' to the field.
        '''
        raise NotImplementedError

    def array(self):
        '''
        Returns a byte array (big-endian) representing this field.
        '''
        raise NotImplementedError

    def set_array(self, data):
        '''
        Sets a byte array (big-endian) to the field. The array should
        be of type 'B' (unsigned char).
        '''
        raise NotImplementedError

    def binary(self):
        '''
        Returns a binary string representing this field. The binary
        string is a sequence of 0's and 1's.
        '''
        raise NotImplementedError

    def set_binary(self, bits):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's.
        '''
        raise NotImplementedError

    def is_variable(self):
        '''
        Tells whether this filed might have variable size depending on
        its content.
        '''
        return False

    def writer(self):
        return self.__writer

    def set_writer(self, writer):
        self.__writer = writer

    def write(self, indent = 0):
        '''
        Returns a human-readable representation of this bit
        field. This function uses the writer set via 'set_writer' to
        obtain the final string.
        '''
        assert self.writer() != None, "No default writer set for this field"

        return self.writer().write(self, indent)

    def size(self):
        '''
        Returns the size of the field in bits.
        '''
        raise NotImplementedError

    def byte_size(self):
        '''
        Returns the size of the field in bytes.
        '''
        bit_size = self.size()
        byte_size = bit_size / 8
        if (bit_size % 8) > 0:
            byte_size += 1
        return byte_size

    def __str__(self, indent = 0):
        '''
        Returns a human-readable representation of this bit
        field. This function uses the writer set via 'set_writer' to
        obtain the final string. It has the same effect than calling
        'write'.
        '''
        return self.write(indent)



# Private

def _int_to_bin(number, width = 32):
    if number < 0:
        number += 1 << width
    i = width - 1
    bits = ["\x00"] * width
    while number and i >= 0:
        bits[i] = "\x00\x01"[number & 1]
        number >>= 1
        i -= 1
    return "".join(bits)

_bit_values = {"\x00" : 0, "\x01" : 1, "0" : 0, "1" : 1}
def _bin_to_int(bits, signed = False):
    number = 0
    bias = 0
    if signed and _bit_values[bits[0]] == 1:
        bits = bits[1:]
        bias = 1 << len(bits)
    for b in bits:
        number <<= 1
        number |= _bit_values[b]
    return number - bias

_intchar_to_bin = {}
_bin_to_intchar = {}
for _i in range(256):
    _ch = chr(_i)
    _bin = _int_to_bin(_i, 8)
    _intchar_to_bin[_i] = _bin
    _bin_to_intchar[_bin] = _i

def _encode_array(data, width = 0):
    assert data.typecode == 'B', "Array must be of type 'B'"
    if width == 0:
        data_aux = data
    else:
        data_aux = data[0:width]
    return "".join(_intchar_to_bin[ch] for ch in data_aux)

def _decode_array(data):
    i = 0
    j = 0
    l = len(data) // 8
    chars = array.array('B')
    while j < l:
        chars.append(_bin_to_intchar[data[i:i+8]])
        i += 8
        j += 1
    return chars


if __name__ == '__main__':
    import doctest
    doctest.testmod()
