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

    Packets can be seen as field containers. That is, a packet is formed
    by a sequence of fields. The :class:`Container` class provides this
    vision. A :mod:`Container` is also a :mod:`Field` itself. Therefore,
    a :mod:`Container` might also accomodate other Containers.

    Consider the first three bytes of the IP header:

    +---------+---------+---------+---------------+
    | version |   hlen  |   tos   |    length     |
    +=========+=========+=========+===============+
    | 4 bits  |  4 bits | 1 byte  |    2 bytes    |
    +---------+---------+---------+---------------+

    We can see the IP header as a :mod:`Container` with a
    sub-:mod:`Container` holding two bit fields (*version* and *hlen*)
    and two additional fields (*tos* and *length*).

    The :class:`Container` class is just an abstract class that allows
    adding fields. That is, it provides the base methods to build
    Containers.

'''

from BitPacket.Field import Field

__FIELD_SEPARATOR__ = "."

class Container(Field):
    '''
    This is an abstrat class to create containers. A container is just a
    field that might contain a sequence of fields (that can be
    containers as well), thus forming a bigger field.
    '''

    def __init__(self, name):
        '''
        Initializes the container with the given *name*. By default, it
        does not contain any fields.
        '''
        Field.__init__(self, name)
        self.__fields = []
        self.__fields_name = {}

    def append(self, field):
        '''
        Appends a new *field* into the container. A *NameError*
        exception will be raised if a field with the same name is
        already in the container.
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
        Returns the field identified by *name*. *name* accepts a dot (.)
        separator to indicate sub-fields of a container (multiple
        separators are allowed). If the field does not exist a
        *KeyError* exception is raised.
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
        Returns the (ordered) list of fields of this container.
        '''
        return self.__fields

    def keys(self):
        '''
        Returns the list of fields' names recursively (i.e. if fields
        are also containers). In case one or more of the fields are
        containers, its fields will be suffixed with a dot separator. As
        an example, "a.b.c" is the key for a field *c* inside a *b*
        container which is also inside a root *a* container.
        '''
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
        Returns the size of the field in bytes. That is, the sum of all
        byte sizes of the fields in this container.
        '''
        size = 0
        for f in self.fields():
            size += f.size()
        return size

    def __len__(self):
        '''
        Returns the number of fields in this container.
        '''
        return len(self.__fields)

    def __getitem__(self, name):
        '''
        Returns the value of the field identified by *name*. This is the
        same as calling container.field(name).value(). If the field does
        not exists a *KeyError* exception is raised.
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
        Sets the given *value* to the field identified by *name*. This
        is the same as calling
        container.field(name).set_value(value). If the field does not
        exists a *KeyError* exception is raised.
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
