#!/usr/bin/env python
#
# @file    Data.py
# @brief   An structure for raw data.
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Wed Jan 20, 2010 11:30
#
# Copyright (C) 2010, 2011, 2012 Aleix Conchillo Flaque
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

    Data
    ====

    An structure that holds a :mod:`String` and its length.

    **API reference**: :class:`Data`

    A :mod:`Data` field lets you store a string of words and keeps its
    length in another field. By default, the size of a word is 1
    byte. :mod:`Data` is a :mod:`Structure` with two fields in this
    order: length and data (internally named *Dara*). The length is a
    numeric field and specifies how many words the *Data* field
    contains.

    In the next example we create a :mod:`Data` field with six
    characters and a length field of 1 byte (thus, a maximum of 255
    characters can be hold):

    >>> data = Data("data", UInt8("Length"));
    >>> data.set_value("abcdef")
    >>> print data
    (data =
      (Length = 6)
      (Data = 0x616263646566))

    We can easily get back the six characters by creating the string
    again:

    >>> "".join(data["Data"])
    'abcdef'


    Word sizes
    ----------

    The length field tells us how many words the *Data* field
    contains. Above, we just saw an example with the default word size
    of 1. But a 12 character string and a word size of 4, we give us 3
    words.

    >>> data = Data("data", UInt8("Length"), 4);
    >>> data.set_value("abcdefghigkl")
    >>> print data
    (data =
      (Length = 3)
      (Data = 0x616263646566676869676B6C))

    Note that data length needs to be a multiple of the word size.

    It is also possible to obtain the word size from the value of
    another field.

    +--------+--------+----------------+
    |  WSize | Length |     Data       |
    +========+========+================+
    | 1 byte | 1 byte | Length * WSize |
    +--------+--------+----------------+

    >>> packet = Structure("packet")
    >>> packet.append(UInt8("WSize"))
    >>> data = Data("data", UInt8("Length"), lambda ctx: ctx["WSize"]);
    >>> packet.append(data)

    >>> buffer = array.array("B", [2, 3, 40, 55, 22, 45, 34, 89])
    >>> packet.set_array(buffer)
    >>> print packet
    (packet =
      (WSize = 2)
      (data =
        (Length = 3)
        (Data = 0x2837162D2259)))

'''

from BitPacket.utils.callable import param_call

from BitPacket.Container import FIELD_SEPARATOR
from BitPacket.Structure import Structure
from BitPacket.String import String

class Data(Structure):
    '''
    This class lets you store strings of words and also provides a field
    to hold its length. It is a :mod:`Structure` with two fields: length
    and data (internally created with name *Data*). The length is a
    numeric field and specifies how many words the *Data* field
    contains. The *Data* field is a :class:`String`.
    '''

    def __init__(self, name, lengthfield, wordsize = 1):
        '''
        Initialize the field with the given *name* and a
        *lengthfield*. Optionally, the initial string can be given in
        *data* and a different word size (defaults to 1) can be set with
        *wordsize*. *wordsize* can also be a function that takes the
        root packet as a single argument. This way, it is possible to
        provide a word size that depends on the value of another field.
        '''
        Structure.__init__(self, name)
        self.__wordsize = wordsize

        wsizefunc = lambda ctx: \
            lengthfield.value() * param_call(wordsize, ctx)

        self.__length = lengthfield
        self.__data = String("Data", wsizefunc)

        Structure.append(self, self.__length)
        Structure.append(self, self.__data)

    def value(self):
        '''
        Returns the value of the *Data* field as a string.
        '''
        return self.__data.value()

    def set_value(self, value):
        '''
        Sets a new string to the *Data* field. The given string length
        must be mutliple of the word size and must fit in the length
        field (i.e. 300 characters are too long if the length field is
        :class:`UInt8`, as only 255 characters fit), otherwise a
        *ValueError* exception will be raised.
        '''
        length = len(value)
        wordsize = param_call(self.__wordsize, self.root())
        if (length % wordsize) == 0:
            try:
                self.__length.set_value(length / wordsize)
            except:
                raise ValueError("Data length must be lower than length "
                                 "field maximum size (%d given)" % length)

            self.__data.set_value(value)
        else:
            raise ValueError("Data length must be a multiple of %d (%d given)" \
                                 % (wordsize, length))

# import array
# from BitPacket.Integer import *

# p = Data("data", UInt8("len"), lambda ctx: 2)
# p.set_array(array.array('B', [3, 1, 2, 3, 4 , 5 , 6]))
# p.set_value(array.array('B', [1, 2, 3, 4, 5]).tostring())
# print p

# p = String("data", "", lambda ctx: ctx["length"])
# print p

# def wsize(ctx):
#     return ctx["WSize"]

# packet = Structure("packet")
# packet.append(UInt8("WSize"))
# data = Data("data", UInt8("Length"), wsize);
# packet.append(data)

# buffer = array.array("B", [2, 3, 40, 55, 22, 45, 34, 87])
# packet.set_array(buffer)
# print packet
