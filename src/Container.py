#!/usr/bin/env python
#
# @file    Container.py
# @brief   Field containers
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Dec 11, 2009 11:57
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

    FIELD CONTAINERS

    Packets can be seen as field containers. That is, a packet is
    formed by a sequence of fields. The Container class provides this
    vision. A Container is also a Field itself. Therefore, a Container
    might accomodate Containers.

    Consider the first three bytes of the IP header:

    +---------+---------+---------+---------------+
    | version |   hlen  |   tos   |    length     |
    +---------+---------+---------+---------------+
     <-- 4 --> <-- 4 -->
     <------- 1 -------> <-- 1 --> <----- 2 ----->

    These are the field descriptions and their sizes:

      - Version (version): 4 bits
      - Header length (hlen): 4 bits
      - Type Of Service (tos): 1 byte
      - Total length (length): 2 bytes

    We can see the IP header as a Container with a sub-Container
    holding two bit fields (version and hlen) and two more fields (tos
    and length).

    The Container class is just an abstract class that allows adding
    fields of a given FieldType. The FieldType of all the sub-fields
    is defined at construction time.

    Currently, there are three Container implementations: Structure,
    BitStructure and MetaStructure.

'''

from Field import Field

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
            raise NameError, 'field "%s" already exists in "%s"' \
                % (field.name(), self.name())
        else:
            self.__fields_name[field.name()] = field

        self.__fields.append(field)

    def fields(self):
        '''
        Returns the (ordered) list of subfields that form this field.
        '''
        return self.__fields

    def size(self):
        '''
        Returns the size of the field. That is, the sum of all sizes
        of the fields in this container. The size can be in bits or
        bytes depending on the subfields type.
        '''
        size = 0
        for f in self.fields():
            size += f.size()
        return size

    def write(self):
        s = self.writer().start_block(self)
        for field in self.fields():
            # Save field writer
            old_writer = field.writer()
            # Inherit parent writer
            field.set_writer(self.writer())
            s += '\n' + field.write()
            # Restore old field writer
            field.set_writer(old_writer)
        s += self.writer().end_block(self)
        return s

    def reset(self):
        '''
        Remove all existent fields from this container. This function
        will loss all previous information stored in this field.
        '''
        self.__fields = []
        self.__fields_name = {}

    def __len__(self):
        '''
        Returns the number of fields in this container.
        '''
        return len(self.__fields)

    def __getitem__(self, name):
        '''
        Returns the field identified by 'name'.
        '''
        return self.__fields_name[name]

    def __getattr__(self, name):
        '''
        Access the field identified by 'name' as a class attribute.
        '''
        return self[name]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
