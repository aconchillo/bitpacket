#!/usr/bin/env python
#
# @file    BitStructure.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 19:25
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

    FIXED STRUCTURES

    A packet is built by many fields which could form an
    structure. This structure can be represented using the
    BitStructure class.

    An example of a simple packet could be:

    +-------+-----------+
    |  id   |  address  |
    +-------+-----------+
     <- 1 -> <--- 4 --->

    That is, a packet (structure) with two fields:

        - Indetifier: 1 byte
        - Memory address: 4 bytes

    This packet could be constructed by:

    >>> bs = BitStructure('mystructure')

    The line above creates an empty packet named 'mystructure'. So,
    now we need to add fields to it. This can be done by calling the
    append() method:

    >>> bs.append(BitField('id', BitPacket.BYTE_SIZE, 0x54))
    >>> bs.append(BitField('address',
    ...                    BitPacket.INTEGER_SIZE,
    ...                    0x10203040))
    >>> print bs
    (mystructure =
       (id = 0x54)
       (address = 0x10203040))

    As you can see, this has added two fields of different sizes into
    our packet.


    ACCESSING FIXED STRUCTRES MEMBERS

    Structure fields can be obtained as in a dictionary, that is, by
    its name. Following the last example:

    >>> print '0x%X' % bs['id']
    0x54
    >>> print '0x%X' % bs['address']
    0x10203040


    UNPACKING STRUCTURES

    To be able to unpack an integer value or an array of bytes into a
    BitStructure, we only need to create the desired packet without
    initializing any field and assign the integer value or array of
    bytes to it.

    >>> bs = BitStructure('mypacket')
    >>> bs.append(BitField('id', BitPacket.BYTE_SIZE))
    >>> bs.append(BitField('address', BitPacket.INTEGER_SIZE))
    >>> print bs
    (mypacket =
       (id = 0x0)
       (address = 0x0))

    So, now we can unpack the following array of bytes:

    >>> data = array.array('B', [0x38, 0x87, 0x34, 0x21, 0x40])

    into our previously defined structure:

    >>> bs.set_array(data)
    >>> print bs
    (mypacket =
       (id = 0x38)
       (address = 0x87342140))


    STRUCTURES AS CLASSES

    An interesting, and obvious, use, is to subclass BitStructure to
    create your own reusable structures. Then, we could create the
    structure defined in the previous section as a new class:

    >>> class MyStructure(BitStructure):
    ...    def __init__(self, id = 0, address = 0):
    ...        BitStructure.__init__(self, 'mystructure')
    ...        self.append(BitField('id', BitPacket.BYTE_SIZE, id))
    ...        self.append(BitField('address',
    ...                             BitPacket.INTEGER_SIZE,
    ...                             address))
    ...
    ...    def id(self):
    ...        return self['id']
    ...
    ...    def address(self):
    ...        return self['address']
    ...
    >>> ms = MyStructure(0x33, 0x50607080)
    >>> print ms
    (mystructure =
       (id = 0x33)
       (address = 0x50607080))

    We can now use the accessors of our class to print its content:

    >>> print '0x%X' % ms.id()
    0x33
    >>> print '0x%X' % ms.address()
    0x50607080

'''

import array

import BitPacket

from BitFieldBase import BitFieldBase
from BitFieldBase import _encode_array
from BitField import BitField

class BitStructure(BitFieldBase):
    '''
    This class represents an structure of bit fields to be used to
    build packets. BitStructure and BitVariableStructure are BitField
    themselves and all of them can be used together. That is, we can
    add any BitField subclass into a BitStructure or
    BitVariableStructure.
    '''

    def __init__(self, name):
        '''
        Initializes the bit structure field with the given 'name'. By
        default an structure field does not contain any members.
        '''
        BitFieldBase.__init__(self, name)
        self._reset()

    def append(self, field):
        '''
        Appends a new 'field' (of any derived BitField type) into the
        structure.
        '''
        if field.name() in self.__fields_name:
            raise NameError, 'field "%s" already exists in structure "%s"' \
                % (field.name(), self.name())
        else:
            self.__fields_name[field.name()] = field
        self.__fields.append(field)

    def array(self):
        '''
        Returns a byte array (big-endian) representing this field.
        '''
        if (self.size() & 7) != 0:
            raise ValueError, '"%s" size must be a multiple of 8' % self.name()

        arr = array.array('B')
        for i in range(0, len(self.__fields)):
            arr += self.__fields[i].array()
        return arr

    def set_array(self, data):
        '''
        Sets a byte array (big-endian) to the field. The array should
        be of type 'B' (unsigned char).
        '''
        if (self.size() & 7) != 0:
            raise ValueError, '"%s" size must be a multiple of 8' % self.name()

        bits = _encode_array(data)
        self.set_binary(bits)

    def binary(self):
        '''
        Returns a binary string representing this field. The binary
        string is a sequence of 0's and 1's.
        '''
        bits = []
        for i in range(0, len(self.__fields)):
            bits += self.__fields[i].binary()
        return bits

    def set_binary(self, bits):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's.
        '''
        size = len(bits)
        start = 0
        for field in self.__fields:
            field_size = field.size()
            if field.is_variable():
                end = size
            else:
                end = start + field_size
            # We could have a field with greater size than given one,
            # so we need to check this.
            if end > size:
                end = size
            field.set_binary(bits[start:end])
            start = end

    def size(self):
        '''
        Returns the size of the field in bits. That is, the sum of all
        item' sizes in the structure.
        '''
        size = 0
        for field in self.__fields:
            size += field.size()
        return size

    def field(self, name):
        '''
        Returns the structure field identified by 'name'.
        '''
        return self.__fields_name[name]

    def _reset(self):
        '''
        Remove all added fields from this structure.
        '''
        self.__fields = []
        self.__fields_name = {}

    def __len__(self):
        '''
        Returns the number of items in the structure.
        '''
        return len(self.__fields)

    def __getitem__(self, name):
        '''
        Returns the structure field identified by 'name'.
        '''
        return self.field(name).value()

    def __setitem__(self, name, value):
        '''
        Sets the given integer 'value' as the value of to the
        structure field identified by 'name'.
        '''
        self.field(name).set_value(value)

    def __str__(self, indent = 0):
        '''
        Returns a human-readable representation of the structure.
        '''
        s = ''
        for i in range(indent):
            s += ' '
        s += '(%s =' % self.name()
        for field in self.__fields:
            s += '\n'
            s += field.__str__(indent + 3)
        s += ')'
        return s


if __name__ == '__main__':
    import doctest
    doctest.testmod()
