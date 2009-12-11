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

from utils.binary import byte_end, encode_bin, decode_bin
from utils.stream import read_stream, write_stream

from Container import Container

from FieldType import FieldTypeBit
from FieldType import FieldTypeByte


class BitStructure(Container):
    '''
    This class represents an structure of bit fields to be used to
    build packets.
    '''

    def __init__(self, name):
        '''
        Initializes the bit structure field with the given 'name'. By
        default an structure field does not contain any fields.
        '''
        Container.__init__(self, name, FieldTypeByte, FieldTypeBit)

    def _encode(self, stream, context):
        binary = ""
        for f in self.fields():
            binary += f.binary()
        try:
            write_stream(stream, self.size(), decode_bin(binary))
        except (AssertionError, ValueError), err:
            raise ValueError('"%s" size error: %s' % (self.name(), err))

    def _decode(self, stream, context):
        try:
            binary = encode_bin(read_stream(stream, self.size()))
        except ValueError, err:
            raise ValueError('"%s" size error: %s ' % (self.name(), err))
        start = 0
        for f in self.fields():
            f.set_binary(binary[start:])
            start += f.size()

    def size(self):
        '''
        Returns the size of the field in bytes. That is, the sum of
        all sizes of the fields in this bit structure.
        '''
        return byte_end(self.bit_size())

    def bit_size(self):
        '''
        Returns the size of the field in bits. That is, the sum of
        all sizes of the fields in this bit structure.
        '''
        return Container.size(self)
