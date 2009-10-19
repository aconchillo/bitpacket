#!/usr/bin/env python
#
# @file    BitStructure.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 19:25
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

    >>> bs.append(BitField('id', 8, 0x54))
    >>> bs.append(BitField('address', 32, 0x10203040))
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

    To be able to unpack an integer value or a string of bytes into a
    BitStructure, we only need to create the desired packet without
    initializing any field and assign the integer value or string of
    bytes to it.

    >>> bs = BitStructure('mypacket')
    >>> bs.append(BitField('id', 8))
    >>> bs.append(BitField('address', 32))
    >>> print bs
    (mypacket =
       (id = 0x00)
       (address = 0x00000000))

    So, now we can unpack the following array of bytes:

    >>> data = array.array('B', [0x38, 0x87, 0x34, 0x21, 0x40])

    into our previously defined structure:

    >>> bs.set_string(data.tostring())
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
    ...        self.append(BitField('id', 8, id))
    ...        self.append(BitField('address', 32, address))
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

from BitFieldBase import BitFieldBase
from BitFieldBase import _decode_string

from BitField import BitField

class BitStructure(BitFieldBase):
    '''
    This class represents an structure of bit fields to be used to
    build packets.
    '''

    def __init__(self, name):
        '''
        Initializes the bit structure field with the given 'name'. By
        default an structure field does not contain any fields.
        '''
        BitFieldBase.__init__(self, name)

        self.__fields = []
        self.__fields_name = {}

    def append(self, field):
        '''
        Appends a new 'field' (of any derived BitFieldBase type) into
        the structure.
        '''
        if field.name() in self.__fields_name:
            raise NameError, 'field "%s" already exists in structure "%s"' \
                % (field.name(), self.name())
        else:
            self.__fields_name[field.name()] = field

        self.__fields.append(field)

    def set_string(self, string, start = 0):
        for field in self.fields():
            field.set_string(string, start)
            start += field.size()

    def binary(self):
        '''
        Returns a binary string representing this structure, that is
        the concatenated binary strings of all fields in the
        structure. The binary string is a sequence of 0's and 1's.
        '''
        bits = []
        for field in self.fields():
            bits += field.binary()
        return bits

    def set_binary(self, bits, start = 0):
        '''
        Sets a binary string to the structure. The binary string is a
        sequence of 0's and 1's.

        This will unpack the given binary string in to the multiple
        fields contained in this structure.
        '''
        string = _decode_string(bits)
        self.set_string(string, start)

    def field(self, name):
        '''
        Returns the structure field identified by 'name'.
        '''
        return self.__fields_name[name]

    def fields(self):
        '''
        Returns the (ordered) list of fields that form this field.
        '''
        return self.__fields

    def write(self):
        '''
        Returns a human-readable representation of the information of
        this bit field. This function uses the writer set via
        'set_writer' to obtain the final string.
        '''
        s = self.writer().start_block(self)
        for field in self.fields():
            # Save field writer
            old_writer = field.writer()
            # Inherit parent writer
            field.set_writer(self.writer())
            s += '\n' + field.write()
            # Restore old field writer
            field.set_writer(old_writer)
        s += self.writer().end_block(self)
        return s

    def size(self):
        '''
        Returns the size of the field in bits. That is, the sum of all
        bit sizes of the fields in this structure.
        '''
        size = 0
        for field in self.__fields:
            size += field.size()
        return size

    def reset(self):
        '''
        Remove all added fields from this structure. This function
        will loss all previous information stored in this field.
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
