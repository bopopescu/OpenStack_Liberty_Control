# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

import six

from cryptography import utils
from cryptography.x509.oid import ObjectIdentifier


class NameAttribute(object):
    def __init__(self, oid, value):
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError(
                "oid argument must be an ObjectIdentifier instance."
            )

        if not isinstance(value, six.text_type):
            raise TypeError(
                "value argument must be a text type."
            )

        self._oid = oid
        self._value = value

    oid = utils.read_only_property("_oid")
    value = utils.read_only_property("_value")

    def __eq__(self, other):
        if not isinstance(other, NameAttribute):
            return NotImplemented

        return (
            self.oid == other.oid and
            self.value == other.value
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<NameAttribute(oid={0.oid}, value={0.value!r})>".format(self)


class Name(object):
    def __init__(self, attributes):
        self._attributes = attributes

    def get_attributes_for_oid(self, oid):
        return [i for i in self if i.oid == oid]

    def __eq__(self, other):
        if not isinstance(other, Name):
            return NotImplemented

        return self._attributes == other._attributes

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return iter(self._attributes)

    def __len__(self):
        return len(self._attributes)

    def __repr__(self):
        return "<Name({0!r})>".format(self._attributes)
