#!/usr/bin/env python
#
# @file    BitStructure.py
# @brief   Static and variable structures of bit fields
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Apr 01, 2007 12:53
#
# Copyright (C) 2007 Aleix Conchillo Flaque
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

__version__ = '0.1.0'
__date__    = 'Sun Apr 01, 2007 12:53'
__author__  = 'Aleix Conchillo Flaque <aleix@member.fsf.org>'
__copyright__ = 'Copyright (C) 2007 Aleix Conchillo Flaque'
__license__ = 'GPL'
__url__     = 'http://hacks-galore.org/aleix/BitPacket'

__doc__ = '''

    A representation of structures of bit fields.

    INTRODUCTION

    This class represents an structure of bit fields to be used to
    build packets. BitStructure and BitVariableStructure are BitField
    themselves and all of them can be used together. That is, we can
    add any BitField subclass into a BitStructure or
    BitVariableStructure.

    Note that some of the code found in this documentation might not
    be self-contained, it may depend on code explained in previous
    sections.


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

    >>> bs.append(BitField('id', Common.BYTE_SIZE, 0x54))
    >>> bs.append(BitField('address', Common.INTEGER_SIZE, 0x10203040))
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

    To be able to unpack an integer value or an array of bytes into a
    BitStructure, we only need to create the desired packet without
    initializing any field and assign the integer value or array of
    bytes to it.

    >>> bs = BitStructure('mypacket')
    >>> bs.append(BitField('id', Common.BYTE_SIZE))
    >>> bs.append(BitField('address', Common.INTEGER_SIZE))
    >>> print bs
    (mypacket =
       (id = 0x0)
       (address = 0x0))

    So, now we can unpack the following array of bytes:

    >>> data = array.array('B', [0x38, 0x87, 0x34, 0x21, 0x40])

    into our previously defined structure:

    >>> bs.set_array(data)
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
    ...        self.append(BitField('id', Common.BYTE_SIZE, id))
    ...        self.append(BitField('address', Common.INTEGER_SIZE, address))
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


    VARIABLE STRUCTURES

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
    >>> bs.append(BitField('id', Common.BYTE_SIZE, 0x54))
    >>> bs.append(BitField('address', Common.INTEGER_SIZE, 0x10203040))
    >>> packet = BitVariableStructure('mypacket', Common.BYTE_SIZE)
    >>> packet.append(bs)
    >>> print packet
    (mypacket =
       (counter = 0x1)
       (mystructure0 =
          (id = 0x54)
          (address = 0x10203040)))

    We can see that the packet has a counter field of value 1 and our
    created structure 'mystructure'. Note that the structure has a new
    name 'mystructure0'. This is because the BitStructure class does
    not allow to have fields with the same name, thus when the
    'mystructure' field has been added the name has automatically
    changed.

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

    >>> adds = BitVariableStructure('addresses', Common.BYTE_SIZE)
    >>> adds.append(BitField('address', Common.INTEGER_SIZE, 0x10203040))
    >>> adds.append(BitField('address', Common.INTEGER_SIZE, 0x40506080))
    >>> ids = BitStructure('ids')
    >>> ids.append(BitField('id', Common.BYTE_SIZE, 0x34))
    >>> ids.append(adds)
    >>> vs = BitVariableStructure('packet', Common.BYTE_SIZE)
    >>> vs.append(ids)
    >>> print vs
    (packet =
       (counter = 0x1)
       (ids0 =
          (id = 0x34)
          (addresses =
             (counter = 0x2)
             (address0 = 0x10203040)
             (address1 = 0x40506080))))

    We have created a variable structure with two addresses 'adds' and
    we have added it to the fixed structure 'ids'. Our packet has been
    created as a BitVariableStructure named 'packet' and the 'ids'
    fixed structure has been added to it.


    ACCESSING VARIABLE STRUCTRES MEMBERS

    In order to access members of variable structures we could follow
    two methods: access by name or access by index.

    Both methods require to know how many members the variable
    structure contains. This is given by the counter() method. So, to
    access the members by name you need to remember that names are
    dynamically changed when added to a variable structure, thus
    appending and 'id' field will become 'id0' (if no member has been
    previously added), and appending 'id' again will become
    'id1'. Knowing this, we could easily iterate through variable
    structure members from the structure created in the previous
    section:

    >>> for i in range(vs.counter()):
    ...     ids = vs.field('ids%d' %i)
    ...     adds = ids.field('addresses')
    ...     for j in range(adds.counter()):
    ...        print adds.field('address%d' % j)
    ...
    (address0 = 0x10203040)
    (address1 = 0x40506080)


    UNPACKING VARIABLE STRUCTURES

    In order to unpack a variable structure, the BitVariableStructure
    class needs to know the type of the multiple structures (all of
    the same type) that might contain. This is done by assigning an
    instance of the desired type into the 'base_field' parameter of
    the BitVariableStructure constructor. So, taking the last example
    defined in the 'VARIABLE STRUCTURES' section, we could do the
    following:

    >>> addr = BitField('address', Common.INTEGER_SIZE)
    >>> adds = BitVariableStructure('addresses', Common.BYTE_SIZE,
    ...                             base_field = addr)
    >>> ids = BitStructure('ids')
    >>> ids.append(BitField('id', Common.BYTE_SIZE))
    >>> ids.append(adds)
    >>> vs = BitVariableStructure('packet', Common.BYTE_SIZE,
    ...                           base_field = ids)
    >>> print vs
    (packet =
       (counter = 0x0))

    The BitVariableStructure 'packet' is empty, so, now we can unpack
    the following array of bytes:

    >>> data = array.array('B', [0x01, 0x34, 0x02, 0x10, 0x20, 0x30, 0x40,
    ...                          0x40, 0x50, 0x60, 0x80])

    into our previously defined variable structure:

    >>> vs.set_array(data)
    >>> print vs
    (packet =
       (counter = 0x1)
       (ids0 =
          (id = 0x34)
          (addresses =
             (counter = 0x2)
             (address0 = 0x10203040)
             (address1 = 0x40506080))))

     As we can see, the BitVariableStructure class dynamically creates
     copies of the 'base_field' parameter in order to reconstruct the
     whole structure.

'''

import array
import copy

import Common

from BitField import BitField
from BitVector import BitVector

class BitStructure(BitField):
    '''
    This class represents an structure of bit fields to be used to
    build packets. BitStructure and BitVariableStructure are BitField
    themselves and all of them can be used together. That is, we can
    add any BitField subclass into a BitStructure or
    BitVariableStructure.
    '''

    def __init__(self, name):
        '''
        Initializes the bit structure field with the given 'name'. By
        default an structure field does not contain any members.
        '''
        BitField.__init__(self, name, 0)
        self.__fields = []
        self.__fields_name = {}

    def append(self, field):
        '''
        Appends a new 'field' (of any derived BitField type) into the
        structure.
        '''
        if field.name() in self.__fields_name:
            raise NameError, 'field "%s" already exists in structure "%s"' \
                % (field.name(), self._name)
        else:
            self.__fields_name[field.name()] = field
        self.__fields.append(field)

    def value(self):
        '''
        Returns the integer value of the field. This value is the
        integer value representing all the structure items.
        '''
        value = 0
        fields = copy.copy(self.__fields)
        fields.reverse()
        bit_size = 0
        for field in fields:
            value |= field.value() << bit_size
            bit_size += field.size()
        return value

    def set_value(self, value, bit_size = None):
        '''
        Sets a new integer 'value' to the field. The bit size of the
        given value can be specified in the 'bit_size' field. If no
        size is specified it will be calculated automatically to fit
        the value passed.
        '''
        bits = BitVector(intVal = value, size = bit_size)
        if not bit_size:
            bit_size = len(bits)
        start = 0
        for field in self.__fields:
            size = field.size()
            if isinstance(field, BitVariableStructure):
                end = bit_size
            else:
                end = start + size
            # We could have a field with greater size than given one,
            # so we need to check this.
            if end > bit_size:
                end = bit_size
            new_bits = bits[start:end]
            field.set_value(new_bits.intValue(), len(new_bits))
            start = end

    def size(self):
        '''
        Returns the size of the field in bits. That is, the sum of all
        item' sizes in the structure.
        '''
        size = 0
        for field in self.__fields:
            size += field.size()
        return size

    def byte_size(self):
        '''
        Returns the size of the field in bytes. That is, the sum of
        all item' byte sizes in the structure.
        '''
        bit_size = self.size()
        byte_size = bit_size / 8
        if (bit_size % 8) > 0:
            byte_size += 1
        return byte_size

    def field(self, name):
        '''
        Returns the structure field identified by 'name'.
        '''
        return self.__fields_name[name]

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
        Sets the given 'value' as the value of to the structure field
        identified by 'name'.
        '''
        self.field(name).set_value(value)

    def __str__(self, indent = 0):
        '''
        Returns a human-readable representation of the structure.
        '''
        s = ''
        for i in range(indent):
            s += ' '
        s += '(%s =' % self._name
        for field in self.__fields:
            s += '\n'
            s += field.__str__(indent + 3)
        s += ')'
        return s



class BitVariableStructure(BitStructure):
    '''
    This class represents a variable structure of bit fields to be
    used to build packets. BitStructure and BitVariableStructure are
    BitField themselves and all of them can be used together. That is,
    we can add any BitField subclass into a BitStructure or
    BitVariableStructure.
    '''

    def __init__(self, name, counter_size, base_field = None):
        '''
        Initializes the bit variable structure field with the given
        'name' as well as with the desired bit size ('counter_size')
        for the self-contained counter field. The 'base_field'
        parameter is only needed when unpacking, and an instance of
        the structure's type being unpacked must me given.
        '''
        BitStructure.__init__(self, name)
        self.__counter_size = counter_size
        self.__base_field = base_field
        self.__counter = BitField('counter', counter_size)
        self.__fields = []
        BitStructure.append(self, self.__counter)

    def counter(self):
        '''
        Returns the number of structures contained in this variable
        structure.
        '''
        return self.__counter.value()

    def field(self, index):
        '''
        Returns the field referenced by 'index', which can be an
        integer value (that is an index) or an string.
        '''
        if isinstance(index, int):
            return self.__fields[index]
        else:
            return BitStructure.field(self, index)

    def append(self, field):
        '''
        Appends a new 'field' (of any derived BitField type) to this
        variable structure. The 'field' being added should be of the
        same type and size as the previous ones.
        '''
        counter = self.__counter.value()
        field._name += '%d' % counter
        BitStructure.append(self, field)
        self.__fields.append(field)
        self.__counter.set_value(counter + 1)

    def set_value(self, value, bit_size = None):
        '''
        Sets a new integer 'value' to the field. The bit size of the
        given value can be specified in the 'bit_size' field. If no
        size is specified it will be calculated automatically to fit
        the value passed.
        '''
        if not self.__base_field:
            raise ImportError, 'Unable to set value (base field not set)'
        bits = BitVector(intVal = value, size = bit_size)
        if not bit_size:
            bit_size = len(bits)
        counter_bits = bits[0:self.__counter_size]
        start = self.__counter_size
        for i in range(counter_bits.intValue()):
            if isinstance(self.__base_field, BitField) \
                    and not (isinstance(self.__base_field, BitStructure) \
                                 or isinstance(self.__base_field,
                                               BitVariableStructure)):
                end = start + self.__base_field.size()
            else:
                end = bit_size
            value_bits = bits[start:end]
            new_field = copy.deepcopy(self.__base_field)
            new_field.set_value(value_bits.intValue(), len(value_bits))
            end = start + new_field.size()
            self.append(new_field)
            start = end


if __name__ == '__main__':
    import doctest
    doctest.testmod()
