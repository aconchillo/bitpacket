#!/usr/bin/env python
#
# @file    Structure.py
# @brief   A container implementation for fields of different types
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Fri Dec 11, 2009 11:57
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

    A container implementation for fields of different types.

    **API reference**: :class:`Structure`

    The :class:`Structure` class provides a byte-aligned
    :mod:`Container` implementation. This means that all the fields
    added to a :mod:`Structure` should be byte-aligned. This does not
    mean that a :mod:`BitField` can not be added, but if added, it
    should be added within a :mod:`BitStructure`. This is because bit
    and byte processing is done diffrently, and that's why
    :mod:`BitStructure` was created.

    Consider the first three bytes of the IP header:

    +---------+---------+---------+---------------+
    | version |   hlen  |   tos   |    length     |
    +=========+=========+=========+===============+
    | 4 bits  |  4 bits | 1 byte  |    2 bytes    |
    +---------+---------+---------+---------------+

    For simplicity, we can create only a :mod:`Structure` with the
    last two fields, *tos* and *length*.

    >>> ip = Structure("IP")

    The line above creates an empty packet named 'IP'. Now, we can add
    the two fields to it with an initial value:

    >>> ip.append(UInt8("tos", 3))
    >>> ip.append(UInt16("length", 146))
    >>> print ip
    (IP =
      (tos = 3)
      (length = 146))


    Accessing fields
    ----------------

    Structure fields, as in any other Container, can be obtained like in
    a dictionary, that is, by its name. Following the last example:

    >>> ip["tos"]
    3
    >>> ip["length"]
    146


    Packing structures
    -------------------

    As with any BitPacket field, packing a Structure is really
    simple. Considering the IP header exampe above we can easily create
    an array of bytes with the contents of the structure:

    >>> ip_data = array.array("B")
    >>> ip.array(ip_data)
    >>> print ip_data
    array('B', [3, 0, 146])

    Or also create a string of bytes from it:

    >>> ip.bytes()
    '\\x03\\x00\\x92'


    Unpacking structures
    --------------------

    To be able to unpack an integer value or a string of bytes into a
    Structure, we only need to create the desired packet and assign data
    to it.

    >>> bs = Structure("mypacket")
    >>> bs.append(UInt8("id"))
    >>> bs.append(UInt32("address"))
    >>> print bs
    (mypacket =
      (id = 0)
      (address = 0))

    So, now we can unpack the following array of bytes:

    >>> data = array.array("B", [0x38, 0x87, 0x34, 0x21, 0x40])

    into our previously defined structure:

    >>> bs.set_bytes(data.tostring())
    >>> print bs
    (mypacket =
      (id = 56)
      (address = 2268340544))


    Structures as classes
    ---------------------

    An interesting use of structures is to subclass them to create your
    own reusable ones. As an example, we could create the structure
    defined in the previous section as a new class:

    >>> class MyStructure(Structure):
    ...    def __init__(self, id = 0, address = 0):
    ...        Structure.__init__(self, "mystructure")
    ...        self.append(UInt8("id", id))
    ...        self.append(UInt32("address", address))
    ...
    ...    def id(self):
    ...        return self["id"]
    ...
    ...    def address(self):
    ...        return self["address"]
    ...
    >>> ms = MyStructure(0x33, 0x50607080)
    >>> print ms
    (mystructure =
      (id = 51)
      (address = 1348497536))

    We can now use the accessors of our class to print its content:

    >>> print "0x%X" % ms.id()
    0x33
    >>> print "0x%X" % ms.address()
    0x50607080

'''

from BitPacket.Container import Container

class Structure(Container):

    '''
    This class provides a byte-aligned Container implementation. All the
    fields added to it should be byte-aligned.
    '''

    def __init__(self, name):
        '''
        Initialize the structure with the given *name*. By default, it
        does not contain any fields.
        '''
        Container.__init__(self, name)

    def _encode(self, stream):
        for f in self.fields():
            f._encode(stream)

    def _decode(self, stream):
        for f in self.fields():
            f._decode(stream)
