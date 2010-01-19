#!/usr/bin/env python
#
# @file    MetaField.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Fri Jan 15, 2010 10:22
#
# Copyright (C) 2010 Aleix Conchillo Flaque
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

from Field import Field

class MetaField(Field):

    @staticmethod
    def _raise_error(instance):
        raise TypeError("No field created for MetaField '%s'" % instance.name())

    @staticmethod
    def _non_proxyable():
        return ["_field", "_fieldfunc", "_create_field",
                "_encode", "_decode", "write"]

    def __init__(self, name,  fieldfunc):
        Field.__init__(self, name)
        self._fieldfunc = fieldfunc
        self._field = None

    def _encode(self, stream, context):
        if self._field:
            self._field._encode(stream, context)
        else:
            self._raise_error(self)

    def _decode(self, stream, context):
        self._create_field(context)
        self._field._decode(stream, context)

    def write(self, stream):
        if self._field:
            self._field.set_writer(self.writer())
            self._field.write(stream)
        else:
            self._raise_error(self)

    def _create_field(self, context):
        if not self._field:
            # Call name() before proxy is available.
            name = self.name()
            self._field = self._fieldfunc(context)
            self._field.set_name(name)

    def __len__(self):
        if self._field:
            return len(self._field)
        else:
            self._raise_error(self)

    def __getitem__(self, name):
        if self._field:
            return self._field[name]
        else:
            self._raise_error(self)

    def __setitem__(self, name, value):
        if self._field:
            self._field[name] = value
        else:
            self._raise_error(self)

    def __getattribute__(self, name):
        try:
            # We'll get an exception due to _field access in __init__,
            # as _field attribute does not exist yet.
            field = object.__getattribute__(self, "_field")
        except AttributeError:
            field = None

        # Get the list of methods that should not be forwarded.
        non_proxyable = object.__getattribute__(self, "_non_proxyable")()

        # If _field is created and we are accessing a proxyable
        # attribute, then forward it to _field.
        if field and name not in non_proxyable:
            return object.__getattribute__(field, name)
        else:
            return object.__getattribute__(self, name)

# import array

# from Structure import Structure
# from Integer import *

# class Test(Structure):

#     def __init__(self):
#         Structure.__init__(self, "tesbabat")
#         self.append(UInt8("value1"))
#         self.append(UInt8("value2"))

# s = Structure("metastruct")
# ss = Structure("substruct")
# s.append(ss)

# f = MetaField("test", lambda ctx: Test())
# ss.append(f)

# s.set_array(array.array("B", [123, 124]))

# print s

#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
