#!/usr/bin/env python
#
# @file    Container.py
# @brief   An object-oriented representation of bit field structures
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

from Field import Field

class Container(Field):

    def __init__(self, name, type, fields_type):
        Field.__init__(self, name, type)
        self.__fields = []
        self.__fields_name = {}
        self.__fields_type = fields_type

    def append(self, field):
        '''
        Appends a new 'field' into the structure. The new field type
        must match the one given at Container's creation time.
        '''
        # We do not allow appending fields of different types.
        if field.type().code() != self.__fields_type.code():
            raise TypeError, 'field "%s" is not of type "%s" ("%s" given)' \
                % (field.name(), self.__fields_type, field.type())

        # Only one field with the same name is allowed.
        if field.name() in self.__fields_name:
            raise NameError, 'field "%s" already exists in "%s"' \
                % (field.name(), self.name())
        else:
            self.__fields_name[field.name()] = field

        self.__fields.append(field)

    def field(self, name):
        '''
        Returns the structure field identified by 'name'.
        '''
        return self.__fields_name[name]

    def fields(self):
        '''
        Returns the (ordered) list of fields that form this field.
        '''
        return self.__fields

    def size(self):
        '''
        Returns the size of the field. That is, the sum of all sizes
        of the fields in this container.
        '''
        size = 0
        for f in self.fields():
            size += f.size()
        return size

    def write(self):
        '''
        Returns a human-readable representation of the information of
        this bit field. This function uses the writer set via
        'set_writer' to obtain the final string.
        '''
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
        Remove all existent fields from this structure. This function
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
        Returns the structure field identified by 'name'.
        '''
        return self.field(name)

    def __getattr__(self, name):
        return self[name]
