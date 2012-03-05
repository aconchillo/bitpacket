#!/usr/bin/env python
#
# @file    String.py
# @brief   A field to represent a stream of bytes
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Jan 20, 2010 09:18
#
# Copyright (C) 2009, 2010, 2012 Aleix Conchillo Flaque
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

    String field
    ============

    A field to store a string of characters.

    **API reference**: :class:`String`

    A :mod:`String` field lets you store a string of characters of any
    size. In the next example we create a string field with six
    characters:

    >>> data = String("data", "this is a string");
    >>> print data
    (data = 0x74686973206973206120737472696E67)

    We can easily get back the six characters by creating the string
    again:

    >>> "".join(data.value())
    'this is a string'


    Unpacking strings
    -----------------

    A :mod:`String` is actually also a meta field. Remember that meta
    fields are used when we don't know the size of the field in
    advance. When packing a string, that's immediate, as we already know
    the size of string, thus we can pack the packet without
    problems. But consider an incoming packet, normally we would expect
    the size of the string to be specified in another field, as the
    :mod:`String` field itslef does not encode any information about the
    size. And this is were meta field come in handy.

    An example will ilustrate this better. Imagine we need to decode
    this packet:

    >>> data = array.array("B", [0x0B, 0x68, 0x65, 0x6C, 0x6C, 0x6F,
    ...                          0x20, 0x77, 0x6F, 0x72, 0x6C, 0x64])

    And we know that the packet format looks like this:

    +--------+---------+
    | length |  string |
    +========+=========+
    | 1 byte |  length |
    +--------+---------+

    As this is a two field packet we will create a :mod:`Structure`:

    >>> packet = Structure("test")

    The first field is the length of the string (next field) in bytes:

    >>> packet.append(UInt8("length"))

    The second field is the string itself:

    >>> packet.append(String("string", "", lambda ctx: ctx["length"]))

    We need to indicate somehow that the length of the string is
    specified by the *length* field. This is where we use the third
    constructor parameter *lengthfunc*. *lengthfunc* takes the context
    as an argument (the context is always the root :mod:`Container` that
    holds all the fields in the packet being unpacked). So, internally,
    *BitPacket* will know how many bytes it needs to read for the string
    field.

    Finally, we set the data to be unpacked and verify its content:

    >>> packet.set_array(data)
    >>> print packet
    (test =
      (length = 11)
      (string = 0x68656C6C6F20776F726C64))
    >>> "".join(packet["string"])
    'hello world'

    *BitPacket* already provides a helper the :mod:`Data` field which
    contains a length field and a string.

'''

from BitPacket.utils.stream import read_stream, write_stream

from BitPacket.Field import Field

class String(Field):
    '''
    A :mod:`String` field lets you store a string of characters of any
    size. Usually, to unpack a string we need to extract the length of
    the string from another field, therefore :mod:`String` becomes a
    meta field.
    '''

    def __init__(self, name, data = "", lengthfunc = lambda ctx: len(data)):
        '''
        Initialize the string field with a *name* and and initial
        *data*, if provided. This is enough if we are just
        packing. However, we need to provide how to obtian the string
        length if we want to be able to unpack it. Thus, we need to give
        a function that will received a context as a single argument and
        that returns the length of the string, in the *lengthfunc*
        field. The context is a reference to the root :mod:`Container`
        field that the field belongs to, so it is possible to access all
        other fields. A possible function could be::

            lambda ctx: ctx["Length"]

        where we get the length of the string from a *Length* field.
        '''
        Field.__init__(self, name)
        self.__data = data
        self.__lengthfunc = lengthfunc

    def _encode(self, stream, context):
        write_stream(stream, self.__lengthfunc(context), self.__data)

    def _decode(self, stream, contex):
        self.__data = read_stream(stream, self.__lengthfunc(contex))

    def size(self):
        '''
        Returns the size in bytes of the string.
        '''
        return len(self.__data)

    def value(self):
        '''
        Returns the string of characters.
        '''
        return self.__data

    def set_value(self, data):
        '''
        Sets a new string of characters to the field.
        '''
        self.__data = data

    def str_value(self):
        '''
        Returns a text string with the hexadecimal value of each
        character of the string. A prefix of 0x is added. So, for "hello",
        "0x68656C6C6F" would be returned.
        '''
        string = ""
        value = self.value()
        if len(value) > 0:
            string = "0x" + "".join(["%02X" % ord(c) for c in value])
        return string

    def str_hex_value(self):
        '''
        This is equivalent of calling *str_value ()*.
        '''
        return self.str_value()

    def str_eng_value(self):
        '''
        This is equivalent of calling *str_value ()*.
        '''
        return self.str_value()
