#!/usr/bin/env python
#
# @file    Array.py
# @brief   An structure for fields of the same type.
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Mon Jan 18, 2010 18:20
#
# Copyright (C) 2010, 2011, 2012 Aleix Conchillo Flaque
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

    Arrays
    ======

    An structure for fields of the same type.

    **API reference**: :class:`Array`

    Sometimes we need to create packets th  at have a number of repeated
    fields in it. Normally, these kind of packets have a counter field
    indicating the number of repeated fields after it.

    An *Array* is a subclass of *Structure*. Initially, it contains a
    length field, which is the one that will indicate how many fields
    the array holds. The type of the length field is specified in the
    *Array* constructor.

    +--------+--------+---------+
    | count  |   id   | address |
    +========+========+=========+
    | 1 byte | 1 byte | 4 bytes |
    +--------+--------+---------+
    |        |  *count* times   |
    +--------+------------------+

    In order to create an *Array* for the depicted packet above, we can
    define the base type of the fields (all of the same type) that this
    array will contain. We will create a *MyStructure* class that
    contains two fields, *id* and *address*.

    >>> class MyStructure(Structure):
    ...    def __init__(self, name = "mystructure", id = 0, address = 0):
    ...        Structure.__init__(self, name)
    ...        self.append(UInt8("id", id))
    ...        self.append(UInt32("address", address))

    Now, we can define an *Array* that contains the default counter
    field of our desired size and a single parameter function that tells
    how to create the array fields.

    >>> packet = Array("mypacket", UInt8("counter"), MyStructure)

    As a second argument to the *Array* constructor, we specify the
    field that specifies how many elements the array contains. As the
    third argument, we have provided the type of the array elements. The
    anonymous function takes an argument which is the root of the packet
    we are building/parsing (this means we have direct access to all
    other packet fields).

    So, let's try to unpack some data and see what happens:

    >>> data = array.array("B", [0x01, 0x54, 0x10, 0x20, 0x30, 0x40])
    >>> packet.set_array(data)
    >>> print packet
    (mypacket =
      (counter = 1)
      (0 =
        (id = 84)
        (address = 270544960)))

    At this point the array contains one field of type *MyStructure* as
    it has unpacked the given array, seen that the *counter* field had
    value 1 and therefore read one *MyStructure* field. It is worth
    noting that the fields added to an *Array* are automatically named
    in a zero-based scheme. That is, to access the first *address* field
    value we could:

    >>> packet["0.address"]
    270544960

    We can also easily add some data to the array. Consider again our
    packet:

    >>> packet = Array("mypacket", UInt8("counter"), MyStructure)

    Adding a *MyStructure* field is as easy as adding a field to any
    other *Structure*:

    >>> packet.append(MyStructure("foo", 54, 98812383))
    >>> print packet
    (mypacket =
      (counter = 1)
      (0 =
        (id = 54)
        (address = 98812383)))


    Complex meta structures
    -----------------------

    We can also build more complex packets, such as the one below, where
    we have one *Array* inside another.

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
    contain the *count2* counter and an *Array* whose number of elements
    is provided by *count2* and that will be filled with 32-bit unsigned
    integers.

    >>> class AddressList(Structure):
    ...     def __init__(self):
    ...         Structure.__init__(self, "addresslist")
    ...         self.append(UInt8("id"))
    ...         self.append(Array("address",
    ...                           UInt8("count2"),
    ...                           lambda ctx: UInt32("value")))

    Now, we can build our packet as an structure with the *count1*
    counter and an *Array* whose number of elements is provided by
    *count1* and that will be filled by address lists (that, remember,
    already has another *Array*).

    >>> s = Array("mypacket",
    ...           UInt8("count1"),
    ...           lambda ctx: AddressList())

    So, let's try to set some data to this packet. As we have seen
    before with the simplest case, data should be propagated and *Array*
    meta properties will be used to build the desired fields.

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
      (0 =
        (id = 1)
        (address =
          (count2 = 1)
          (0 = 16909060)))
      (1 =
        (id = 2)
        (address =
          (count2 = 2)
          (0 = 84281096)
          (1 = 151653132))))

    It worked! As we see, our packet consists on a *mystructure* that
    contains two *AddressList* fields. The first one with a single
    address and the second with two.

'''

from BitPacket.Container import FIELD_SEPARATOR
from BitPacket.Structure import Structure
from BitPacket.MetaField import MetaField

class Array(Structure):

    def __init__(self, name, lengthfield, fieldtype):
        Structure.__init__(self, name)

        self.__length = lengthfield
        self.__fieldtype = fieldtype

        Structure.append(self, self.__length)

    def _decode(self, stream):
        # Clear all fields in the array.
        self.reset()

        # Re-add length field and decode its value.
        Structure.append(self, self.__length)
        self.__length._decode(stream)

        # Append fields and parse them.
        for i in range(self.__length.value()):
            new_field = self.__fieldtype(self.root())
            new_field._set_name("%d" % i)
            new_field._decode(stream)
            Structure.append(self, new_field)

    def append(self, field):
        basefield = self.__fieldtype(self.root())
        basefieldtype = type(basefield)

        # If we have a MetaField check the type of the field that it
        # will hold.
        if isinstance(basefield, MetaField):
            basefieldtype = basefield.type()

        if isinstance(field, basefieldtype):
            value = self.__length.value()
            field._set_name(str(value))
            self.__length.set_value(value + 1)
            Structure.append(self, field)
        else:
            raise TypeError("Invalid field type for array '%s' "
                            "(expected %s, got %s)" \
                                % (self.name(),
                                   basefieldtype, type(field)))

    def __setitem__(self, name, value):
        '''
        Sets the given 'value' to the field identified by 'name'.

        If the names[0] does not exists in the array the function
        will instantiate a new field automatically (only if the index is
        consecutive to the length of the array).
        '''
        names = name.split(FIELD_SEPARATOR, 1)
        length = self.__length.value()

        if int(names[0]) < length:
            # Normal access
            pass
        elif int(names[0]) == length:
            new_field = self.__fieldtype(self.root())
            new_field._set_name("%d" % length)
            Structure.append(self, new_field)
            self.__length.set_value (length + 1)
        else: # int(names[0]) > length
            raise IndexError("Index %s must be <= %s" % (names[0], length))

        Structure.__setitem__(self, name, value)

# from BitPacket.Integer import *
# from BitPacket.MetaField import *

# import array

# class Sub32(UInt32):

#     def __init__(self, value):
#         UInt32.__init__(self, "foo", value)

# a = Array("test", UInt8("len"), lambda ctx: UInt32("test"))
# a.append(UInt32("value", 23))
# a.append(Sub32(34))

# a.set_array(array.array("B", [2, 0, 0, 0, 23, 0, 0, 0, 34]))

# print a

# ma = Array("memory", UInt8,
#            lambda ctx: MetaField("metaaddress",
#                                  lambda ctx: Array("address", UInt8,
#                                                    lambda ctx: MetaField("metavalue", lambda ctx: UInt32("value")))))

# address = Array("address", UInt8, UInt32)
# address.append(UInt32("0", 0x12345678))
# address.append(UInt32("1", 0x9ABCDEFF))
# ma.append(address)
# ma.set_array(array.array("B", [1,
#                                2,
#                                0x12, 0x34, 0x56, 0x78,
#                                0x9A, 0xBC, 0xDE, 0xFF]))
# print ma
