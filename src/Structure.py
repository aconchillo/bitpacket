#!/usr/bin/env python
#
# @file    Structure.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 11:57
#
# Copyright (C) 2009 Aleix Conchillo Flaque
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

__doc__ = '''

    FIELD CONTAINERS

    A packet field might be formed by bit fields. The BitStructure
    class must be used, in conjunction with BitField, to create
    byte-aligned fields formed, internally, by bit fields.

    Consider the first byte of the IP header:

    +---------+----------+
    | version |   hlen   |
    +---------+----------+
     <-- 4 --> <-- 4 -->

    This packet could be constructed by:

    >>> bs = BitStructure('IP1st')

    The line above creates an empty packet named 'IP1st'. So, now we
    need to add fields to it. As BitStructure is a Container subclass
    the append() method can be used:

    >>> bs.append(BitField('version', 4, 14))
    >>> bs.append(BitField('hlen', 4, 12))
    >>> print bs
    (IP1st =
       (version = 14)
       (hlen = 12))


    ACCESSING CONTAINER FIELDS

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

from Container import Container

class Structure(Container):

    def __init__(self, name):
        Container.__init__(self, name)

    def _encode(self, stream, context):
        for f in self.fields():
            f._encode(stream, context)

    def _decode(self, stream, context):
        for f in self.fields():
            f._decode(stream, context)
