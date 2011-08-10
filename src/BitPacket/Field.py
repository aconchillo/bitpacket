#!/usr/bin/env python
#
# @file    Field.py
# @brief   Base abstract class for all BitPacket fields
# @author  Aleix Conchillo Flaque <aconchillo@gmail.com>
# @date    Sun Aug 02, 2009 12:28
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
    accessed directly as class members.

    Note: changing the field name at run-time is not recommended
    unless you know what you are doing.


    Building and parsing fields
    ===========================

    The main purpose of BitPacket is to provide an easy way to represent
    packets. In BitPacket, packets can be built from and to an string of
    bytes, arrays and streams.

    A field subclass, then, needs to provide the following methods::

        def value():_

    This method returns the actual value of the field, whatever that
    is, a number, a string, etc.::

        def set_value(value):_

    This method sets a new value to the current field. The value might
    be a number, a string, etc. depending on the field contents::

        def size():_

    This method must return the field's size. Note that some fields
    are bit-oriented, so the method might return values for different
    units (basically for bytes or bits)::

        def str_value():_

    This method must return the text string representation for the
    given field::

        def str_hex_value():_

    This method must return the hexadecimal text string representation
    for the given field. The hexadecimal values of the string must be
    obtained from the actual values in memory. For example, for a
    float value, the hexadecimal representation could be the bytes
    forming the IEEE-754 representation::

        def str_eng_value():_

    This method must return the text string representation of the result
    obtained after applying the field's calibration curve. Therefore, it
    is necessary to call the calibration curve of the field first and
    then return the result (after applying any extra desired
    formatting)::

        def _encode(stream, context):_

    This method will write the field's value into the given stream (byte
    or bit oriented). The context is the root of the packet that the
    field is part of::

        def _decode(stream, context):_

    This method will convert the given stream (byte or bit oriented)
    into the internal field representation. The context is the root of
    the packet that the field is part of.

    Calibration curves
    ==================

    Sometimes a field might need to be expressed in another way, or a
    calculation might be necessary to determine the final value of the
    field. Consider, for example, a numeric field that represents a
    temperature with a 16-bit precision and covers a range from 0 to 50
    celsius degrees. The calibration curve comes in handy by letting the
    user to specify this conversion function::

        def set_calibration_curve(self, curve):_

    This method lets the user to provide a function to compute the
    calibration curve. The function must be unary taking the field's
    value and computing (using a the desired conversion function) a
    result.

    For the temperature example, the calibration function could be
    something like::

        def temp_conv(x):
            return (x / 65535.0) * 50.0

'''

from io import BytesIO, StringIO

from BitPacket.writers.WriterTextBasic import WriterTextBasic

class Field(object):
    '''
    Abstract root class for all other BitPacket classes. Initially, a
    field only has a name and no value. Field subclasses must provide
    field details, such as the size of the field, the implementation of
    how the field value will look like, that is, how the field should be
    built, and other field related details.
    '''

    def __init__(self, name):
        '''
        Initialize the field with the given *name*. And identity
        (returning the field's value) calibration curve is set by
        default.
        '''
        self.__name = name
        self.__parent = None
        self.__calibration = None

        # Identity calibration
        self.set_calibration_curve(lambda x: x)

    def name(self):
        '''
        Returns the name of the field.
        '''
        return self.__name

    def parent(self):
        '''
        Returns the parent of this field, or None if the field is not
        part of any other field.
        '''
        return self.__parent

    def fields(self):
        '''
        Returns a list of the children of this field. An empty list is
        returned if the field does not have any child.
        '''
        return []

    def value(self):
        '''
        Returns the value of the field.
        '''
        raise NotImplementedError

    def set_value(self, value):
        '''
        Sets a new *value* to the field.
        '''
        raise NotImplementedError

    def array(self, array):
        '''
        Returns the given *array* appended with the field byte
        representation to it.
        '''
        return array.fromstring(self.bytes())

    def set_array(self, array):
        '''
        Sets the given *array* bytes to the field. This function does
        the same as calling *set_bytes* with the bytes of the array.
        '''
        self.set_bytes(array.tostring())

    def bytes(self):
        '''
        Returns a string of bytes representing this field.
        '''
        stream = BytesIO()
        self.stream(stream)
        return stream.getvalue()

    def set_bytes(self, bytes):
        '''
        Sets a string of bytes to the field.
        '''
        self.set_stream(BytesIO(bytes))

    def stream(self, stream):
        '''
        Fill the given byte stream with the contents of this field.
        '''
        self._encode(stream, self)

    def set_stream(self, stream):
        '''
        Sets this field with the contents of the given stream. Note that
        only the bytes necessary for this field will be obtained from
        the stream. This means that the stream cursor will only advance
        as many bytes as the size of this field.
        '''
        self._decode(stream, self)

    def calibration_curve(self):
        '''
        Returns the calibration curve function.
        '''
        return self.__calibration

    def set_calibration_curve(self, curve):
        '''
        Sets the calibration curve to be applied to this field in order
        to obtain a desired conversion. Some fields might represent
        temperatures, angles, etc. that need to be converted from its
        digital form to its analog form. The calibration curve provides
        the functionality to perform this conversion.
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
        value is the result of applying a calibration curve to the value
        of this field. Some fields might represent temperatures, angles,
        etc. that need to be converted from its digital form to its
        analog form. This function will return the value after the
        conversion is done, that is, after applying the calibration
        curve.
        '''
        return self.__calibration(self.value())

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
        '''
        Write the field's value into the given stream (byte or bit
        oriented). The context is the root of the packet that the field
        is part of.
        '''
        raise NotImplementedError

    def _decode(self, stream, context):
        '''
        Converts the given stream (byte or bit oriented) into the
        internal field representation. The context is the root of the
        packet that the field is part of.
        '''
        raise NotImplementedError

    def _set_name(self, name):
        '''
        Sets a new name to the field. This function is intended to be
        used only by the library internals, so use it with care as the
        field must have already been referenced by its original name.
        '''
        self.__name = name

    def _set_parent(self, parent):
        '''
        Sets the parent of this field. This function is intended to be
        used only by the library internals, so use it with care.
        '''
        self.__parent = parent

    def __str__(self):
        '''
        Returns a human-readable representation of the information of
        this bit field. It uses :class:`WriterTextBasic` to obtain the
        resulting string.
        '''
        writer = WriterTextBasic(StringIO())
        writer.write(self)
        return writer.stream().getvalue()
