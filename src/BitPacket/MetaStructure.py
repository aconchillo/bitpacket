#!/usr/bin/env python
#
# @file    MetaStructure.py
# @brief   A meta structure with an unknow number of fields
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Fri Dec 11, 2009 17:07
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

    A meta structure with an unknow number of fields.

    **API reference**: :class:`MetaStructure`

    Sometimes we need to create packets that have a number of repeated
    fields in it. Normally, these kind of packets have a counter field
    indicating the number of repeated fields after it.

    Basic meta structures
    ---------------------

    A *MetaStructure* is a subclass of *Structure*. It does not contain
    any fields by default, as they will be created at
    run-time. Therefore, the intended use of this class is to facilitate
    the unpacking of defined data but whose size is not known at
    creation time (i.e. the number of received data may vary).

    +--------+--------+---------+
    | count  |   id   | address |
    +========+========+=========+
    | 1 byte | 1 byte | 4 bytes |
    +--------+--------+---------+
    |        |  *count* times   |
    +--------+------------------+

    In order to create a *MetaStructure* it is necessary to define the
    base type of the fields (all of the same type) that this structure
    will contain. Following the depicted packet above, we will create a
    *MyStructure* class that contains two fields, *id* and *address*.

    >>> class MyStructure(Structure):
    ...    def __init__(self, name = "mystructure", id = 0, address = 0):
    ...        Structure.__init__(self, name)
    ...        self.append(UInt8("id", id))
    ...        self.append(UInt32("address", address))

    Now, we can define an *Structure* that contains a counter field that
    will be used to know how many *MyStructure* structures follow it.

    >>> packet = Structure("mypacket")
    >>> packet.append(UInt8("counter"))
    >>> packet.append(MetaStructure("mystructure",
    ...                             lambda ctx: ctx["counter"],
    ...                             lambda ctx: MyStructure()))

    So, here is the big deal! Note that, as a second argument to the
    *MetaStructure* constructor, we have provided an anonymous function
    (does not need to be anonymous) that returns the number of following
    *MyStructure*. The function takes a single argument which will
    always be the root of our BitPacket, so this means we have direct
    access to the *counter* field and that we can know its value (it
    will already be processed because it comes first). The third
    argument is also a function (also receiveing the context) that will
    tell how to create the fields. Got it?  If not, read this paragraph
    again.

    Let's try to unpack some data to this structure and see what
    happens:

    >>> data = array.array("B", [0x01, 0x54, 0x10, 0x20, 0x30, 0x40])
    >>> packet.set_array(data)
    >>> print packet
    (mypacket =
      (counter = 1)
      (mystructure =
        (0 =
          (id = 84)
          (address = 270544960))))

    Now, the meta structure contains one field of type *MyStructure*. It
    is worth to note that the fields added to a meta structure are
    automatically named in a zero-based scheme. That is, to access the
    first *address* field value we could:

    >>> packet["mystructure.0.address"]
    270544960


    Complex meta structures
    -----------------------

    We can also build more complex packets, such as the one below, where
    we have two meta structures one inside of the other.

    +--------+--------+--------+----------------+
    | count1 |   id   | count2 |     address    |
    +========+========+========+================+
    | 1 byte | 1 byte | 1 byte |     4 bytes    |
    +--------+--------+--------+----------------+
    |                          | *count2* times |
    +--------+--------+--------+----------------+
    |        |         *count1* times           |
    +--------+----------------------------------+

    We will first create a structure for the list of addresses. It will
    contain the *count2* counter and a *MetaStructure* whose number of
    elements is provided by *count2* and that will be filled with 32-bit
    unsigned integers.

    >>> class AddressList(Structure):
    ...     def __init__(self):
    ...         Structure.__init__(self, "address")
    ...         self.append(UInt8("id"))
    ...         self.append(UInt8("count2"))
    ...         self.append(MetaStructure("address",
    ...                                   lambda ctx: self["count2"],
    ...                                   lambda ctx: UInt32("value")))

    Now, we can build our packet as an structure with the *count1*
    counter and a *MetaStructure* whose number of elements is provided
    by *count1* and that will be filled by address lists (that,
    remember, already has another meta structure).

    >>> s = Structure("mypacket")
    >>> s.append(UInt8("count1"))
    >>> s.append(MetaStructure("mystructure",
    ...                        lambda ctx: ctx["count1"],
    ...                        lambda ctx: AddressList()))

    So, let's try to set some data to this packet. As we have seen
    before with the simple case, data should be propagated and meta
    structures will be used to build the desired fields.

    >>> s.set_array(array.array("B", [0x02, # count1
    ...                               0x01, # id (1)
    ...                               0x01, # count2 (1)
    ...                               0x01, 0x02, 0x03, 0x04,
    ...                               0x02, # id (2)
    ...                               0x02, # count2 (2)
    ...                               0x05, 0x06, 0x07, 0x08,
    ...                               0x09, 0x0A, 0x0B, 0x0C]))
    >>> print s
    (mypacket =
      (count1 = 2)
      (mystructure =
        (0 =
          (id = 1)
          (count2 = 1)
          (address =
            (0 = 16909060)))
        (1 =
          (id = 2)
          (count2 = 2)
          (address =
            (0 = 84281096)
            (1 = 151653132)))))

    It worked! As we see, our packet consists on a *mystructure* that
    contains two *AddressList* fields. The first one with a single
    address and the second with two.

    The conclusion is that building complex data structures is possible
    and really simple with the use of meta fields such as
    *MetaStructure*.

'''

from BitPacket.Structure import Structure

class MetaStructure(Structure):
    '''
    Meta structures are used when the number of fields in a packet is
    only known at runtime. Normally, the number of fields to create is
    contained in a numeric field that indicates it.

    This class makes this task easy by letting the user to provide the
    way this numeric field should be obtained and how to create the
    fields.
    '''

    def __init__(self, name, lengthfunc, fieldfunc):
        '''
        Initialize the meta structure with the given *name* and two
        functions, *lengthfunc* and *fieldfunc*. Both functions are
        unary, receiving the current BitPacket context as their
        argument. The former needs to return the number of fields that
        should be created. The later returns a newly created field.
        '''
        Structure.__init__(self, name)
        self.__fieldfunc = fieldfunc
        self.__lengthfunc = lengthfunc

    def _decode(self, stream, context):
        # Get the counter dynamically.
        length = self.__lengthfunc(context)

        # Append fields.
        for i in range(length):
            new_field = self.__fieldfunc(context)
            new_field._set_name("%d" % i)
            self.append(new_field)

        # Once the subfields have been added, parse the stream.
        Structure._decode(self, stream, context)
