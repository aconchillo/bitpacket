#!/usr/bin/env python
#
# @file    Field.py
# @brief   An object-oriented representation of bit field structures
# @author  Aleix Conchillo Flaque <aleix@member.fsf.org>
# @date    Sun Aug 02, 2009 12:28
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

    An object-oriented representation of bit field structures.

    These classes represent simple bit fields, and fixed and variable
    structures of bit fields which might be used to construct
    packets. BitField, BitStructure and BitVariableStructure implement
    the BitFieldBase abstract class, so all of them can be used
    together. This means that, for example, we can add any
    BitFieldBase sub-class into a BitStructure or
    BitVariableStructure.

'''

import array

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from FieldType import FieldTypeByte

from WriterBasic import WriterBasic

class Field:

    def __init__(self, name, type = FieldTypeByte):
        '''
        Initialize this abstract class with the given 'name' and field
        'type'.
        '''
        self.__name = name
        self.__type = type
        self.__calibration = None
        self.__writer = WriterBasic()

        # Identity calibration
        self.set_calibration_curve(lambda x: x)

    def name(self):
        '''
        Returns the name of the field.
        '''
        return self.__name

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

    def write(self):
        '''
        Returns a human-readable representation of the information of
        this bit field. This function uses the writer set via
        'set_writer' to obtain the final string.

        Note that the result might not contain all the information. It
        all depends on the BitFieldWriter implementation.
        '''
        assert self.writer() != None, "No default writer set for this field"

        return self.writer().write(self)

    def _encode(self, stream, context):
        raise NotImplementedError

    def _decode(self, stream, context):
        raise NotImplementedError

    def size(self):
        '''
        Returns the size of the field.
        '''
        raise NotImplementedError

    def type(self):
        return self.__type

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
        values of this field. Note that the type of the field can be a
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

    def __str__(self):
        '''
        Returns a human-readable representation of the information of
        this bit field. This function uses the writer set via
        'set_writer' to obtain the final string.

        It has the same effect than calling the 'write' method.
        '''
        return self.write()
