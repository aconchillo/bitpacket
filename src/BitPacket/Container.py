#!/usr/bin/env python
#
# @file    Container.py
# @brief   Generic abstract field container
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Fri Dec 11, 2009 11:57
#
# Copyright (C) 2009, 2010, 2011 Aleix Conchillo Flaque
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

    **API reference**: :class:`Container`

    Packets can be seen as field containers. That is, a packet is
    formed by a sequence of fields. The :class:`Container` class
    provides this vision. A :mod:`Container` is also a :mod:`Field`
    itself. Therefore, a :mod:`Container` might accomodate other
    Containers.

    Consider the first three bytes of the IP header:

    +---------+---------+---------+---------------+
    | version |   hlen  |   tos   |    length     |
    +=========+=========+=========+===============+
    | 4 bits  |  4 bits | 1 byte  |    2 bytes    |
    +---------+---------+---------+---------------+

    We can see the IP header as a :mod:`Container` with a
    sub-:mod:`Container` holding two bit fields (*version* and *hlen*)
    and two more fields (*tos* and *length*).

    The :class:`Container` class is just an abstract class that allows
    adding fields. That is, it provides the base methods to build
    Containers.

    Currently, there are three :mod:`Container` implementations:
    :mod:`Structure`, :mod:`BitStructure` and :mod:`MetaStructure`.

'''

from BitPacket.Field import Field

__FIELD_SEPARATOR__ = "."

class Container(Field):
    '''
    This is an abstrat class to create containers. A container is just
    a field that might contain a sequence of fields, thus forming a
    bigger field.

    Fields added to a Container must have the same type, that is, it
    is not possible to mix byte with bit fields.
    '''

    def __init__(self, name):
        '''
        Initializes the container with the given 'name' and 'type' and
        'fields_type'. The 'type' is the type of this container, while
        'fields_type' is the allowed type for the fields to be added
        to this container.
        '''
        Field.__init__(self, name)
        self.__fields = []
        self.__fields_name = {}

    def append(self, field):
        '''
        Appends a new 'field' into the container. The new field type
        must match the one given at Container's constructor.
        '''
        # Only one field with the same name is allowed.
        if field.name() in self.__fields_name:
            raise NameError("Field '%s' already exists in '%s'" \
                                % (field.name(), self.name()))
        else:
            self.__fields_name[field.name()] = field

        self.__fields.append(field)
        field._set_parent(self)

    def field(self, name):
        '''
        Returns the field identified by 'name'.
        '''
        names = name.split(__FIELD_SEPARATOR__, 1)
        try:
            field = self.__fields_name[names[0]]
            if len(names) >= 2:
                if isinstance(field, Container):
                    field = field.field(names[1])
                else:
                    raise TypeError("%s is not a Container" % names[0])
        except KeyError:
            raise KeyError("Field '%s' does not exist" % name)
        except TypeError as err:
            raise KeyError("Field '%s' does not exist (%s)" % (name, err))
        return field

    def fields(self):
        '''
        Returns the (ordered) list of subfields that form this field.
        '''
        return self.__fields

    def keys(self):
        keys = []
        for field in self.fields():
            name = field.name()
            if isinstance(field, Container):
                for k in list(field.keys()):
                    keys.append(name + __FIELD_SEPARATOR__ + k)
            else:
                keys.append(name)
        return keys

    def size(self):
        '''
        Returns the size of the field in bytes. That is, the sum of
        all byte sizes of the fields in this container.
        '''
        size = 0
        for f in self.fields():
            size += f.size()
        return size

    def write(self, writer):
        writer.start_block(self)
        for field in self.fields():
            field.write(writer)
        writer.end_block(self)

    def __len__(self):
        '''
        Returns the number of fields in this container.
        '''
        return len(self.__fields)

    def __getitem__(self, name):
        '''
        Returns the value of the field identified by 'name'. This is
        the same as calling container.field(name).value().
        '''
        names = name.split(__FIELD_SEPARATOR__, 1)
        try:
            field = self.__fields_name[names[0]]
            if len(names) < 2:
                return field.value()
            else:
                return field[names[1]]
        except KeyError:
            raise KeyError("Field '%s' does not exist" % name)

    def __setitem__(self, name, value):
        '''
        Sets the given 'value' to the field identified by 'name'. This
        is the same as calling container.field(name).set_value(value).
        '''
        names = name.split(__FIELD_SEPARATOR__, 1)
        try:
            field = self.__fields_name[names[0]]
            if len(names) < 2:
                field.set_value(value)
            else:
                field[names[1]] = value
        except KeyError:
            raise KeyError("Field '%s' does not exist" % name)
