#!/usr/bin/env python
#
# @file    binary.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Wed Aug 05, 2009 17:37
#
# Copyright (C) 2009, 2010 Aleix Conchillo Flaque
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

__BYTE_SIZE__ = 8

def byte_aligned(number):
    return (number & 0x07) == 0

def byte_end(bit_size):
    byte_end = bit_size >> 3
    if not byte_aligned(bit_size):
        byte_end += 1
    return byte_end

def int_to_bin(number, width = 32):
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
def bin_to_int(bits, signed = False):
    number = 0
    bias = 0
    if signed and _bit_values[bits[0]] == 1:
        bits = bits[1:]
        bias = 1 << len(bits)
    for b in bits:
        number <<= 1
        number |= _bit_values[b]
    return number - bias

_char_to_bin = {}
_bin_to_char = {}
for _i in range(256):
    _ch = chr(_i)
    _bin = int_to_bin(_i, __BYTE_SIZE__)
    _char_to_bin[_ch] = _bin
    _bin_to_char[_bin] = _ch

def encode_bin(data):
    return "".join(_char_to_bin[ch] for ch in data)

def decode_bin(data):
    data_size = len(data)
    end = byte_end(data_size)
    bit_size = end * __BYTE_SIZE__
    bit_missing = bit_size - data_size
    data += "\x00" * bit_missing
    chars = ""
    i = 0
    while i < bit_size:
        chars += _bin_to_char[data[i:i + __BYTE_SIZE__]]
        i += __BYTE_SIZE__
    return chars
