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

    String of characters
    ====================

    Fields to store a string of characters.

     **API reference**: :class:`String`

    A :mod:`String` field lets you store a string of characters of any
    size. The length of the string needs to be specified at creation
    time.

    The simplest case is a string with a fixed length. In the next
    example we create a string field with sixteen characters:

    >>> data = String("data", 16)
    >>> data.set_value("this is a string")
    >>> print data
    (data = 0x74686973206973206120737472696E67)

    As usual, we can easily get back the original string:

    >>> "".join(data.value())
    'this is a string'

    Note that, above, "print data" returns a human-readable string with
    hexadecimal values and "data.value()" returns the actual string.

    For convenience, there is a :mod:`Text` field that inherits from
    :mod:`String` and always returns the actual string.

    >>> text = Text("text", 16)
    >>> text.set_value("this is a string")
    >>> print text
    (text = this is a string)

    So, :mod:`Text` is supposedly to be used with only text while
    :mod:`String` is to be used with any character.


    Unpacking strings
    =================

    Instead of a fixed length, we can specify a length function that
    will tell us what length the string should have. In the following
    structure we create a :mod:`Structure` with a numeric "length" field
    and a string of unknown size.

    +--------+---------+
    | length |  string |
    +========+=========+
    | 1 byte |  length |
    +--------+---------+

    *BitPacket* already provides a helper the :mod:`Data` field which
    contains a length field and a string.

    >>> packet = Structure("string")
    >>> l = UInt8("length")
    >>> s = String("data", lambda ctx: ctx["length"])
    >>> packet.append(l)
    >>> packet.append(s)

    If we print the initial contents of the structure we can see that
    the length is 0 and that we still have an empty string.

    >>> print packet
    (string =
      (length = 0)
      (data = ))

    We can try to assign a value to our string directly and see what
    happens:

    >>> try:
    ...   s.set_value("this is a string")
    ... except ValueError as err:
    ...   print "Error: %s" % err
    Error: Data length must be 0 (16 given)

    An exception is raised indicating that string length should be
    0. This is because the "length" field has not been assigned a value
    yet.

    Finally, we can provide to the structure all the necessary
    information, for example, in an array:

    >>> data = array.array("B", [0x10, 0x74, 0x68, 0x69, 0x73, 0x20,
    ...                          0x69, 0x73, 0x20, 0x61, 0x20, 0x73,
    ...                          0x74, 0x72, 0x69, 0x6E, 0x67])
    >>> packet.set_array(data)
    >>> print packet
    (string =
      (length = 16)
      (data = 0x74686973206973206120737472696E67))

'''

from BitPacket.utils.stream import read_stream, write_stream
from BitPacket.utils.callable import param_call

from BitPacket.Field import Field

class String(Field):
    '''
    A :mod:`String` field lets you store a string of characters of any
    size. Usually, to unpack a string we need to extract the length of
    the string from another field, in which case we need to specify a
    function that will know where to get the length from. However, it is
    also possible to specify a fixed length string.
    '''

    def __init__(self, name, length):
        '''
        Initialize the string field with a *name* and a
        *length*. *length* can be a fixed number or a single arument
        function that returns the length of the string. The single
        argument is a reference to the top-level root :mod:`Container`
        field where the string belongs to. A possible function could
        be::

            lambda ctx: ctx["Length"]

        where we get the length of the string from a *Length* field.
        '''
        Field.__init__(self, name)
        self.__data = ""
        self.__length = length

    def _encode(self, stream):
        write_stream(stream, param_call(self.__length, self.root()), self.__data)

    def _decode(self, stream):
        self.__data = read_stream(stream, param_call(self.__length, self.root()))

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
        length = param_call(self.__length, self.root())
        if len(data) == length:
            self.__data = data
        else:
            raise ValueError("Data length must be %d (%d given)" \
                                 % (length, len(data)))

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


class Text(String):
    '''
    :mod:`Text` is basically a :mod:`String` but conceived to be used
    with only text strings. It does not perform any check on the
    data. It simply returns the internal string (which should be text)
    instead of generating a text string with the hexadecimal values of
    the string.
    '''

    def __init__(self, name, length):
        String.__init__(self, name, length)

    def str_value(self):
        '''
        Returns the text string.
        '''
        return self.value()

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
