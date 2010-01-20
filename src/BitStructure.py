#!/usr/bin/env python
#
# @file    BitStructure.py
# @brief   Bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 19:25
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

__doc__ = '''

    Bit-aligned container
    =====================

    **API reference**: :class:`BitStructure`

    The :mod:`BitStructure` class must be used, in conjunction with
    :mod:`BitField`, to create these byte-aligned fields formed,
    internally, by bit fields.

    It is really important to understand that BitPacket is byte
    oriented, therefore, a :mod:`BitStructure` must be byte-aligned.

    Now, consider the first byte of the IP header:

    +---------+----------+
    | version |   hlen   |
    +=========+==========+
    | 4 bits  |  4 bits  |
    +---------+----------+

    This packet could be constructed by:

    >>> bs = BitStructure("IP")

    The line above creates an empty structure named 'IP'. Now, we need
    to add fields to it. As :mod:`BitStructure` is a :mod:`Container`
    subclass the :func:`Container.append` function can be used:

    >>> bs.append(BitField("version", 4, 0x0E))
    >>> bs.append(BitField("hlen", 4, 0x0C))
    >>> print bs
    (IP =
      (version = 0x0E)
      (hlen = 0x0C))


    Accessing fields
    ----------------

    BitStructure fields can be obtained as in a dictionary, as in any
    Container subclass. Following the last example:

    >>> bs["version"]
    14
    >>> bs["hlen"]
    12


    Unpacking bit structures
    ------------------------

    To be able to unpack an integer value or a string of bytes into a
    BitStructure, we only need to create the desired structure without
    initializing any field and assign the integer value or string of
    bytes to it.

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

'''

import array

from utils.binary import byte_end
from utils.bitstream import BitStreamReader, BitStreamWriter
from utils.stream import read_stream, write_stream

from BitField import BitField
from Container import Container

class BitStructure(Container):
    '''
    This class represents an structure of bit fields to be used to
    build byte-aligned fields.
    '''

    def __init__(self, name):
        '''
        Initializes the bit structure field with the given 'name'. By
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
