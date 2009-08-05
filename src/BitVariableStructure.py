#!/usr/bin/env python
#
# @file    BitVariableStructure.py
# @brief   Variable structure depending on a counter field
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 19:26
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


    Variable structures depending on a counter field.

    Sometimes we need to create packets that have a number of repeated
    structures in it. Normally, these kind of packets have a field
    indicating the number of repeated structures and the structures
    after it.

    +-------+-------+-----------+-------+-----------+
    | count |  id   |  address  |  id   |  address  |
    +-------+-------+-----------+-------+-----------+
     <- 1 -> <- 1 -> <--- 4 ---> <- 1 -> <--- 4 --->

    We can achieve this by using the BitVariableStructure class which
    is a subclass of BitStructure. This class already contains a
    counter field of a given size and at the beginning the structure
    does not contain any more fields, thus the counter is set to
    zero. The fields which will form the variable structure need to be
    added as in BitStructure and the counter will be automatically
    increased.

    >>> bs = BitStructure('mystructure')
    >>> bs.append(BitField('id', BitPacket.BYTE_SIZE, 0x54))
    >>> bs.append(BitField('address',
    ...                    BitPacket.INTEGER_SIZE,
    ...                    0x10203040))
    >>> packet = BitVariableStructure('mypacket',
    ...                               BitPacket.BYTE_SIZE,
    ...                               bs)
    >>> packet.append(bs)
    >>> print packet
    (mypacket =
       (counter = 0x1)
       (fields =
          (mystructure0 =
             (id = 0x54)
             (address = 0x10203040))))

    Note that the variable structure has a new field 'fields' which
    will contain all the structures being added to this variable
    structure. We can also see that the packet has a counter field of
    value 1 and our created structure 'mystructure' and that the
    structure has a new name 'mystructure0'. This is because the
    BitStructure class does not allow to have fields with the same
    name, thus when the 'mystructure' field has been added the name
    has automatically changed.

    Finally, we can also build more complex packets, such as the one
    below, where we have two variable structures one inside of the
    other.

    +-------+-------+-------+-----------+------
    | cnt1  |  id   | cnt2  |  address  | ...
    +-------+-------+-------+-----------+------
     <- 1 -> <- 1 -> <- 1 -> <--- 4 --->
                             <----- cnt2 ----->
             <-------------- cnt1 ------------>

    This can easly be done with the following piece of code:

    >>> base_adds = BitField('address', BitPacket.INTEGER_SIZE)
    >>> adds = BitVariableStructure('addresses',
    ...                             BitPacket.BYTE_SIZE,
    ...                             base_adds)
    >>> adds.append(BitField('address',
    ...                      BitPacket.INTEGER_SIZE,
    ...                      0x10203040))
    >>> adds.append(BitField('address',
    ...                      BitPacket.INTEGER_SIZE,
    ...                      0x50607080))
    >>> ids = BitStructure('ids')
    >>> ids.append(BitField('id', BitPacket.BYTE_SIZE, 0x34))
    >>> ids.append(adds)
    >>> vs = BitVariableStructure('packet',
    ...                           BitPacket.BYTE_SIZE,
    ...                           ids)
    >>> vs.append(ids)
    >>> print vs
    (packet =
       (counter = 0x1)
       (fields =
          (ids0 =
             (id = 0x34)
             (addresses =
                (counter = 0x2)
                (fields =
                   (address0 = 0x10203040)
                   (address1 = 0x50607080))))))

    We have created a variable structure with two addresses 'adds' and
    we have added it to the fixed structure 'ids'. Our packet has been
    created as a BitVariableStructure named 'packet' and the 'ids'
    fixed structure has been added to it.


    ACCESSING VARIABLE STRUCTRES MEMBERS

    In order to access members of variable structures we can follow
    two methods: access by name or access by index.

    Both methods require to know how many members the variable
    structure contains. This is given by the counter() method. So, to
    access the members by name you need to remember that names are
    dynamically changed when added to a variable structure, thus
    appending and 'id' field will become 'id0' (if no member has been
    previously added), and appending 'id' again will become
    'id1'. With this, we can easily iterate through variable structure
    members from the structure created in the previous section:

    >>> for i in range(vs.counter()):
    ...     ids = vs.counter_field('ids%d' %i)
    ...     adds = ids.field('addresses')
    ...     for j in range(adds.counter()):
    ...        print adds.counter_field('address%d' % j)
    ...
    (address0 = 0x10203040)
    (address1 = 0x50607080)


    UNPACKING VARIABLE STRUCTURES

    In order to unpack a variable structure, the BitVariableStructure
    class needs to know the type of the multiple structures (all of
    the same type) that might contain. This is done by assigning an
    instance of the desired type into the 'base_field' parameter of
    the BitVariableStructure constructor. So, taking the last example
    defined in the 'VARIABLE STRUCTURES' section, we could do the
    following:

    >>> addr = BitField('address', BitPacket.INTEGER_SIZE)
    >>> adds = BitVariableStructure('addresses',
    ...                             BitPacket.BYTE_SIZE,
    ...                             base_field = addr)
    >>> ids = BitStructure('ids')
    >>> ids.append(BitField('id', BitPacket.BYTE_SIZE))
    >>> ids.append(adds)
    >>> vs = BitVariableStructure('packet',
    ...                           BitPacket.BYTE_SIZE,
    ...                           base_field = ids)
    >>> print vs
    (packet =
       (counter = 0x0)
       (fields =))

    The BitVariableStructure 'packet' is empty, so, now we can unpack
    the following array of bytes:

    >>> data = array.array('B', [0x01, 0x34, 0x02, 0x10, 0x20, 0x30, 0x40,
    ...                          0x50, 0x60, 0x70, 0x80])

    into our previously defined variable structure:

    >>> vs.set_array(data)
    >>> print vs
    (packet =
       (counter = 0x1)
       (fields =
          (ids0 =
             (id = 0x34)
             (addresses =
                (counter = 0x2)
                (fields =
                   (address0 = 0x10203040)
                   (address1 = 0x50607080))))))

     As we can see, the BitVariableStructure class dynamically creates
     copies of the 'base_field' parameter in order to reconstruct the
     whole structure.

'''

import array
import copy

import BitPacket

from BitField import BitField
from BitStructure import BitStructure
from BitFieldBase import _bin_to_int

class BitVariableStructure(BitStructure):
    '''
    This class represents a variable structure of bit fields to be
    used to build packets. It inhertis from BitStructure, thus both
    are BitFieldBase themselves and all of them can be used
    together. That is, we can add any BitFieldBase subclass into a
    BitStructure or BitVariableStructure.
    '''

    def __init__(self, name, counter_size, base_field):
        '''
        Initializes the bit variable structure field with the given
        'name' as well as with the desired bit size ('counter_size')
        for the self-contained counter field. The 'base_field' might
        be an instance of the structure's type to be added. Note that
        it is only allowed to add fields of the same type and size of
        the base field.
        '''
        self.__counter_size = counter_size
        self.__base_field = base_field
        BitStructure.__init__(self, name)

    def counter(self):
        '''
        Returns the number of fields contained in this variable
        structure.
        '''
        return self.__counter.value()

    def counter_field(self, index):
        '''
        Returns the field referenced by 'index', which can be an
        integer value (that is an index) or an string.
        '''
        name = index
        if isinstance(index, int):
            base_name = self.__base_field.name()
            name = '%s%d' % (base_name, index)
        return self.__fields.field(name)

    def append(self, field):
        '''
        Appends a new 'field' (of any derived BitFieldBase type) to
        this variable structure. The 'field' being added must be of
        the same type and size as the base field, otherwise a
        TypeError exception will be raised.
        '''
        if type(field) != type(self.__base_field):
            raise TypeError, "Given field type differs from base type"
        if field.size() != self.__base_field.size():
            raise ValueError, "Given field size differs from base type"
        counter = self.counter()
        base_name = self.__base_field.name()
        field._name = '%s%d' % (base_name, counter)
        self.__fields.append(field)
        self.__counter.set_value(counter + 1)

    def set_binary(self, bits):
        '''
        Sets a binary string to the field. The binary string is a
        sequence of 0's and 1's.
        '''
        # We might be re-using the instance, so we need to start from
        # zero.
        self._reset()

        # We set the counter to 0 as append will already increment it.
        self.__counter.set_value(0)

        # Get counter from data and append fields.
        counter = _bin_to_int(bits[0:self.__counter.size()])
        for i in range(counter):
            new_field = copy.deepcopy(self.__base_field)
            self.append(new_field)

        # Fields have been only added, we need to set the value now.
        self.__fields.set_binary(bits[self.__counter.size():])

    def is_variable(self):
        '''
        Tells whether this filed might have variable size depending on
        its content.
        '''
        return True

    def _reset(self):
        '''
        Remove all added fields form this structure and set counter to
        0.
        '''
        BitStructure._reset(self)
        self.__counter = BitField('counter', self.__counter_size)
        self.__fields = BitStructure('fields')
        BitStructure.append(self, self.__counter)
        BitStructure.append(self, self.__fields)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
