#!/usr/bin/env python
#
# @file    BitStructure.py
# @brief   A container implementation for bit fields
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Sun Aug 02, 2009 19:25
#
# Copyright (C) 2009, 2010, 2011, 2012 Aleix Conchillo Flaque
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

    A container implementation for bit fields.

    **API reference**: :class:`BitStructure`

    The BitStructure class must be used, in conjunction with
    :mod:`BitField`, to create byte-aligned fields formed, internally,
    by bit fields.

    It is really important to understand that BitPacket is byte
    oriented, therefore, a BitStructure must be byte-aligned.

    Consider the first byte of an IP header packet:

    +---------+----------+
    | version |   hlen   |
    +=========+==========+
    | 4 bits  |  4 bits  |
    +---------+----------+

    This packet can be constructed as:

    >>> ip = BitStructure("IP")

    The line above creates an empty structure named 'IP'. Now, we need
    to add fields to it. As BitStructure is a :mod:`Container` subclass
    the :func:`Container.append` function can be used:

    >>> ip.append(BitField("version", 4, 0x0E))
    >>> ip.append(BitField("hlen", 4, 0x0C))
    >>> print ip
    (IP =
      (version = 0x0E)
      (hlen = 0x0C))

    Note that the size of a BitStructure is returned in bytes. Remember
    that the purpose of a BitStructure is to create a byte-aligned value
    that is built internally with bits:

    >>> ip.size()
    1


    Accessing fields
    ----------------

    BitStructure fields can be obtained as in a dictionary, and as in
    any :mod:`Container` subclass. Following the last example:

    >>> ip["version"]
    14
    >>> ip["hlen"]
    12


    Packing bit structures
    ----------------------

    As with any BitPacket field, packing a BitStructure is really
    simple. Considering the IP header exampe above we can easily create
    an array of bytes with the contents of the structure:

    >>> ip_data = array.array("B")
    >>> ip.array(ip_data)
    >>> print ip_data
    array('B', [236])

    Or also create a string of bytes from it:

    >>> ip.bytes()
    '\\xec'


    Unpacking bit structures
    ------------------------

    To be able to unpack an integer value or a string of bytes into a
    BitStructure, we only need to create the desired structure and
    assign data to it.

    >>> bs = BitStructure("mypacket")
    >>> bs.append(BitField("id", 8))
    >>> bs.append(BitField("address", 32))
    >>> print bs
    (mypacket =
      (id = 0x00)
      (address = 0x00000000))

    So, now we can unpack the following array of bytes:

    >>> data = array.array("B", [0x38, 0x87, 0x34, 0x21, 0x40])

    into our previously defined structure:

    >>> bs.set_array(data)
    >>> print bs
    (mypacket =
      (id = 0x38)
      (address = 0x87342140))

    Also, new data can also be unpacked (old data will be lost):

    >>> data = array.array("B", [0x45, 0x67, 0x24, 0x98, 0xFB])
    >>> bs.set_array(data)
    >>> print bs
    (mypacket =
      (id = 0x45)
      (address = 0x672498FB))

'''

from BitPacket.utils.binary import byte_end
from BitPacket.utils.bitstream import BitStreamReader, BitStreamWriter

from BitPacket.Container import Container

class BitStructure(Container):
    '''
    This class represents an structure formed by bit fields. The
    resulting structure must be byte-aligned and is to be used with
    other BitPacket types.
    '''

    def __init__(self, name):
        '''
        Initialize the bit structure field with the given *name*. By
        default an structure field does not contain any fields.
        '''
        Container.__init__(self, name)

    def _encode(self, stream, context):
        bitstream = BitStreamWriter(stream)
        for f in self.fields():
            f._encode(bitstream, context)
        bitstream.flush()

    def _decode(self, stream, context):
        bitstream = BitStreamReader(stream)
        for f in self.fields():
            f._decode(bitstream, context)

    def size(self):
        '''
        Returns the size of the field in bytes. This function will add
        all the bit field sizes in order to calculate the byte size of
        the container.
        '''
        return byte_end(Container.size(self))
