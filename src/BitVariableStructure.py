#!/usr/bin/env python
#
# @file    BitVariableStructure.py
# @brief   Variable structure depending on a counter field
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 19:26
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

    Variable structures depending on a counter field.

    Sometimes we need to create packets that have a number of repeated
    structures in it. Normally, these kind of packets have a field
    indicating the number of repeated structures and the structures
    after it.

    +-------+-------+-----------+-------+-----------+
    | count |  id   |  address  |  id   |  address  |
    +-------+-------+-----------+-------+-----------+
     <- 1 -> <- 1 -> <--- 4 ---> <- 1 -> <--- 4 --->
             <--------------- count --------------->

    We can achieve this by using the BitVariableStructure class which
    is a subclass of BitStructure. This class already contains a
    counter field of a given size and at the beginning the structure
    does not contain any more fields, thus the counter is set to
    zero. The fields which will form the variable structure need to be
    added as in BitStructure and the counter will be automatically
    increased.

    In order to create a BitVariableStructure it is necessary to
    define the base type of the fields (all of the same type) that
    this variable structure will contain.

    >>> class MyStructure(BitStructure):
    ...    def __init__(self, id = 0, address = 0):
    ...        BitStructure.__init__(self, 'mystructure')
    ...        self.append(BitField('id', 8, id))
    ...        self.append(BitField('address', 32, address))

    Following the first depicted packet, we have created a MyStructure
    class that contains two fields. Now, we are ready to define a new
    variable structure that will contain a variable number of
    MyStructure fields.

    >>> packet = BitVariableStructure('mypacket', 8, MyStructure)

    Finally, we can try to add a MyStrcuture instance and see how the
    final packet looks like.

    >>> packet.append(MyStructure(0x54, 0x10203040))
    >>> print packet
    (mypacket =
       (counter = 0x01)
       (fields =
          (mystructure0 =
             (id = 0x54)
             (address = 0x10203040))))

    Note that the variable structure has a new field 'fields' which
    contains all the structures being added to this variable
    structure. We can also see that the packet has a counter field of
    value 1 (only one field has been added) and that our MyStructure
    instance has a new name 'mystructure0'. This is because the
    BitStructure class does not allow to have fields with the same
    name, thus when the field has been added the name has
    automatically changed.

    We can also build more complex packets, such as the one below,
    where we have two variable structures one inside of the other.

    +-------+-------+-------+-----------+------
    | cnt1  |  id   | cnt2  |  address  | ...
    +-------+-------+-------+-----------+------
     <- 1 -> <- 1 -> <- 1 -> <--- 4 --->
                             <----- cnt2 ----->
             <-------------- cnt1 ------------>

    This can easly be done with the following piece of code:

    >>> class Address(BitField):
    ...    def __init__(self, address = 0):
    ...        BitField.__init__(self, 'address', 32, address)

    >>> class AddressList(BitVariableStructure):
    ...    def __init__(self):
    ...        BitVariableStructure.__init__(self, 'addresses', 8, Address)

    >>> class IdAddresses(BitStructure):
    ...    def __init__(self, id = 0):
    ...        BitStructure.__init__(self, 'ids')
    ...        self.__list = AddressList()
    ...        self.append(BitField('id', 8, id))
    ...        self.append(self.__list)
    ...
    ...    def add(self, address):
    ...        self.__list.append(Address(address))

    >>> ids = IdAddresses(0x34)
    >>> ids.add(0x10203040)
    >>> ids.add(0x50607080)

    >>> vs = BitVariableStructure('packet', 8, IdAddresses)
    >>> vs.append(ids)
    >>> print vs
    (packet =
       (counter = 0x01)
       (fields =
          (ids0 =
             (id = 0x34)
             (addresses =
                (counter = 0x02)
                (fields =
                   (address0 = 0x10203040)
                   (address1 = 0x50607080))))))


    UNPACKING VARIABLE STRUCTURES

    In order to unpack a variable structure, the BitVariableStructure
    class needs to know, as we already said, the base type of the
    multiple structures (all of the same type) that will
    contain. Then, we only need to set new data to the structure and
    everything will be built automatically.

    >>> vs = BitVariableStructure('packet', 8, base_type = IdAddresses)
    >>> print vs
    (packet =
       (counter = 0x00)
       (fields =))

    The BitVariableStructure 'packet' is empty, so, now we can unpack
    the following array of bytes:

    >>> data = array.array('B', [0x01, 0x34, 0x02, 0x10, 0x20, 0x30, 0x40,
    ...                          0x50, 0x60, 0x70, 0x80])

    into our previously defined variable structure:

    >>> vs.set_array(data)
    >>> print vs
    (packet =
       (counter = 0x01)
       (fields =
          (ids0 =
             (id = 0x34)
             (addresses =
                (counter = 0x02)
                (fields =
                   (address0 = 0x10203040)
                   (address1 = 0x50607080))))))

     As we can see, the BitVariableStructure class dynamically creates
     fields of the given base type in order to reconstruct the whole
     structure.

'''

import array
import copy

from BitField import BitField
from BitStructure import BitStructure
from BitFieldBase import _bin_to_int
from BitFieldBase import _encode_array

class BitVariableStructure(BitStructure):
    '''
    This class represents a variable structure of bit fields to be
    used to build packets. It inhertis from BitStructure, thus both
    are BitFieldBase themselves and all of them can be used
    together. That is, we can add any BitFieldBase subclass into a
    BitStructure or BitVariableStructure.
    '''

    def __init__(self, name, counter_size, base_type):
        '''
        Initializes the bit variable structure field with the given
        'name' as well as with the desired bit size ('counter_size')
        for the self-contained counter field. The 'base_field' might
        be an instance of the structure's type to be added. Note that
        it is only allowed to add fields of the same type and size of
        the base field.
        '''
        BitStructure.__init__(self, name)

        self.__base_type = base_type
        self.__counter = BitField('counter', counter_size)
        self.__fields = BitStructure('fields')

        BitStructure.append(self, self.__counter)
        BitStructure.append(self, self.__fields)

    def counter(self):
        '''
        Returns the number of sub-fields contained in this variable
        structure.
        '''
        return self.__counter.value()

    def subfields(self):
        '''
        Returns the list of sub-fields of this variable structure. The
        number of sub-fields is determined by the counter field.
        '''
        return self.__fields.fields()

    def append(self, field):
        '''
        Appends a new 'field' (of any derived BitFieldBase type) to
        this variable structure. The 'field' being added must be of
        the same type as the base field, otherwise a TypeError
        exception will be raised.
        '''
        if not isinstance(field, self.__base_type):
            raise TypeError, "Given field type differs from base type"

        counter = self.counter()
        field.set_name('%s%d' % (field.name(), counter))
        self.__fields.append(field)
        self.__counter.set_value(counter + 1)

    def set_binary(self, bits):
        # We might be re-using the instance, so we need to reset it.
        self.reset()

        # Get counter from data and append fields.
        counter = _bin_to_int(bits[0:self.__counter.size()])
        for i in range(counter):
            new_field = self.__base_type()
            self.append(new_field)

        # Fields have been only added, we need to set the value now.
        self.__fields.set_binary(bits[self.__counter.size():])

    def is_variable(self):
        return True

    def reset(self):
        '''
        Remove all added sub-fields form this variable structure and
        set counter to 0.
        '''
        self.__counter.set_value(0)
        self.__fields.reset()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
