#!/usr/bin/env python
#
# @file    Field.py
# @brief   Base abstract class for all BitPacket fields
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 12:28
#
# Copyright (C) 2009, 2010 Aleix Conchillo Flaque
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

    An object-oriented representation of bit field structures.

    **API reference**: :class:`Field`

    The Field class is the abstract root class for all other BitPacket
    classes. Initially, a field only has a name and no value. Field
    subclasses must provide field details, such as the size of the
    field, the implementation of how the field value will look like,
    that is, how the field should be built, and other field related
    details.

    Naming fields
    =============

    The most simple field accessor is its name. A field name is built
    upon creation but can be changed at run-time (special care should
    be taken, though). It is recommended to follow python variable
    naming when assigning a name to a field. This is because with the
    :class:`Container` subclass (and its subclasses) fields can be
    accessed as class members.

    Note: changing the field name at run-time is not recommended
    unless you know what you are doing.


    Building and parsing fields
    ===========================

    The main objective of BitPacket is to provide an easy way to
    represent packets. In BitPacket, packets can be built from and to
    strings, arrays and streams.

    A field subclass, then, needs to provide the following methods:

    >>> def value(self)

    This method returns the actual value of the field, whatever that
    is, a number, a string, etc.

    >>> def set_value(self, value)

    This method sets a new value for the current field. The value
    might be a number, a string, etc. depending on the field contents.

    >>> def size(self)

    This method must return the field's size. Note that some fields
    are bit-oriented, so the method might return values for different
    units (basically for bytes and bits).

    >>> def str_value(self)

    This method must return the string representation for the given
    field.

    >>> def str_hex_value(self)

    This method must return the hexadecimal string representation for
    the given field. The hexadecimal values of the string must be
    obtained from the actual values in memory. For example, for a
    float value, the hexadecimal representation could be the bytes
    forming the IEEE-754 representation.

    >>> def str_eng_value(self)

    This method must return the string representation of the result
    obtained after applying the field's calibration curve. Therefore,
    it is necessary to first call the calibration curve of the field
    and then return the result (after applying any extra desired
    formatting).

    >>> def _encode(self, stream, context)
    >>> def _decode(self, stream, context)

    Calibration curves
    ==================

'''

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from WriterTextBasic import WriterTextBasic

class Field(object):

    def __init__(self, name):
        '''
        Initialize this abstract class with the given 'name' and field
        'type'.
        '''
        self.__name = name
        self.__calibration = None
        self.__writer = WriterTextBasic()

        # Identity calibration
        self.set_calibration_curve(lambda x: x)

    def name(self):
        '''
        Returns the name of the field.
        '''
        return self.__name

    def set_name(self, name):
        self.__name = name

    def value(self):
        '''
        Returns the value (integer, float...) of the field.
        '''
        raise NotImplementedError

    def set_value(self, value):
        '''
        Sets a new 'value' (integer, float...) to the field.
        '''
        raise NotImplementedError

    def array(self, array):
        return array.fromstring(self.string())

    def set_array(self, array):
        self.set_string(array.tostring())

    def string(self):
        '''
        Returns a string of bytes representing this field. Note that
        if the field is not byte aligned, the last byte starts from
        the MSB.
        '''
        stream = StringIO()
        self.stream(stream)
        return stream.getvalue()

    def set_string(self, string):
        '''
        Sets a string of bytes to the field.
        '''
        self.set_stream(StringIO(string))

    def stream(self, stream):
        self._encode(stream, self)

    def set_stream(self, stream):
        self._decode(stream, self)

    def calibration_curve(self):
        return self.__calibration

    def set_calibration_curve(self, curve):
        '''
        Sets the calibration curve to be applied to this field value
        in order to obtain the enginnering value. Some fields might
        represent tempreatures, angles, etc. that need to be converted
        from its digital form to its analog form. The calibration
        curve provides the functionality to perform this conversion.
        '''
        self.__calibration = curve

    def hex_value(self):
        '''
        Returns the hexadecimal integer representation of this
        field. That is, the bytes forming this field in its integer
        representation.
        '''
        return self.value()

    def eng_value(self):
        '''
        Returns the engineering value of this field. The engineering
        value is the result of applying a calibration curve to the
        value of this field. Some fields might represent tempreatures,
        angles, etc. that need to be converted from its digital form
        to its analog form. This function will return the value after
        the conversion is done, that is, after applying the
        calibration curve.
        '''
        return self.__calibration(self.value())

    def writer(self):
        '''
        Returns the writer to be used by this field in order to print
        the field information.

        By default, the WriterBasic is used.
        '''
        return self.__writer

    def set_writer(self, writer):
        '''
        Sets the new 'writer' to be used by this field in order to
        print the field information.
        '''
        self.__writer = writer

    def write(self, stream):
        '''
        Returns a human-readable representation of the information of
        this bit field. This function uses the writer set via
        'set_writer' to obtain the final string.

        Note that the result might not contain all the information. It
        all depends on the BitFieldWriter implementation.
        '''
        assert self.writer() != None, "No default writer set for this field"

        return self.writer().write(self, stream)

    def size(self):
        '''
        Returns the size of the field.
        '''
        raise NotImplementedError

    def str_value(self):
        '''
        Returns a human-readable representation of the value of this
        field. Note that the type of the field can be a float,
        integer, etc. So, the representation might be different for
        each type.
        '''
        raise NotImplementedError

    def str_hex_value(self):
        '''
        Returns a human-readable representation of the hexadecimal
        value of this field. Note that the type of the field can be a
        float, integer, etc. This is the real representation (in
        memory) of the value.
        '''
        raise NotImplementedError

    def str_eng_value(self):
        '''
        Returns a human-readable representation of the engineering
        value. This function will first calculate the engineering
        value (by applying the calibration curve) and will return the
        string representation of it.
        '''
        raise NotImplementedError

    def _encode(self, stream, context):
        raise NotImplementedError

    def _decode(self, stream, context):
        raise NotImplementedError

    def __str__(self):
        '''
        Returns a human-readable representation of the information of
        this bit field. This function uses the writer set via
        'set_writer' to obtain the final string.

        It has the same effect than calling the 'write' method.
        '''
        stream = StringIO()
        self.write(stream)
        return stream.getvalue()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
