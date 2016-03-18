# Copyright 2014 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Common parameter types for validating request Body.

"""
import copy
import re
import unicodedata

import six


def _is_printable(char):
    """determine if a unicode code point is printable.

    This checks if the character is either "other" (mostly control
    codes), or a non-horizontal space. All characters that don't match
    those criteria are considered printable; that is: letters;
    combining marks; numbers; punctuation; symbols; (horizontal) space
    separators.
    """
    category = unicodedata.category(char)
    return (not category.startswith("C") and
            (not category.startswith("Z") or category == "Zs"))


def _get_all_chars():
    for i in range(0xFFFF):
        yield six.unichr(i)


# build a regex that matches all printable characters. This allows
# spaces in the middle of the name. Also note that the regexp below
# deliberately allows the empty string. This is so only the constraint
# which enforces a minimum length for the name is triggered when an
# empty string is tested. Otherwise it is not deterministic which
# constraint fails and this causes issues for some unittests when
# PYTHONHASHSEED is set randomly.
def _get_printable(exclude=None):
    if exclude is None:
        exclude = []
    return ''.join(c for c in _get_all_chars()
                       if _is_printable(c) and c not in exclude)


_printable_ws = ''.join(c for c in _get_all_chars()
                        if unicodedata.category(c) == "Zs")


def _get_printable_no_ws(exclude=None):
    if exclude is None:
        exclude = []
    return ''.join(c for c in _get_all_chars()
                   if _is_printable(c) and
                       unicodedata.category(c) != "Zs" and
                       c not in exclude)

valid_name_regex_base = '^(?![%s])[%s]*(?<![%s])$'


valid_name_regex = valid_name_regex_base % (
    re.escape(_printable_ws), re.escape(_get_printable()),
    re.escape(_printable_ws))


# This regex allows leading/trailing whitespace
valid_name_leading_trailing_spaces_regex_base = (
    "^[%(ws)s]*[%(no_ws)s]+[%(ws)s]*$|"
    "^[%(ws)s]*[%(no_ws)s][%(no_ws)s%(ws)s]+[%(no_ws)s][%(ws)s]*$")


valid_cell_name_regex = valid_name_regex_base % (
    re.escape(_printable_ws),
    re.escape(_get_printable(exclude=['!', '.', '@'])),
    re.escape(_printable_ws))


# cell's name disallow '!',  '.' and '@'.
valid_cell_name_leading_trailing_spaces_regex = (
    valid_name_leading_trailing_spaces_regex_base % {
        'ws': re.escape(_printable_ws),
        'no_ws': re.escape(_get_printable_no_ws(exclude=['!', '.', '@']))})


valid_name_leading_trailing_spaces_regex = (
    valid_name_leading_trailing_spaces_regex_base % {
        'ws': re.escape(_printable_ws),
        'no_ws': re.escape(_get_printable_no_ws())})


valid_name_regex_obj = re.compile(valid_name_regex, re.UNICODE)


boolean = {
    'type': ['boolean', 'string'],
    'enum': [True, 'True', 'TRUE', 'true', '1', 'ON', 'On', 'on',
             'YES', 'Yes', 'yes',
             False, 'False', 'FALSE', 'false', '0', 'OFF', 'Off', 'off',
             'NO', 'No', 'no'],
}


none = {
    'enum': ['None', None, {}]
}


positive_integer = {
    'type': ['integer', 'string'],
    'pattern': '^[0-9]*$', 'minimum': 1
}


non_negative_integer = {
    'type': ['integer', 'string'],
    'pattern': '^[0-9]*$', 'minimum': 0
}


hostname = {
    'type': 'string', 'minLength': 1, 'maxLength': 255,
    # NOTE: 'host' is defined in "services" table, and that
    # means a hostname. The hostname grammar in RFC952 does
    # not allow for underscores in hostnames. However, this
    # schema allows them, because it sometimes occurs in
    # real systems.
    'pattern': '^[a-zA-Z0-9-._]*$',
}


hostname_or_ip_address = {
    # NOTE: Allow to specify hostname, ipv4 and ipv6.
    'type': 'string', 'maxLength': 255,
    'pattern': '^[a-zA-Z0-9-_.:]*$'
}


name = {
    # NOTE: Nova v2.1 API contains some 'name' parameters such
    # as keypair, server, flavor, aggregate and so on. They are
    # stored in the DB and Nova specific parameters.
    # This definition is used for all their parameters.
    'type': 'string', 'minLength': 1, 'maxLength': 255,
    'pattern': valid_name_regex,
}


cell_name = {
    'type': 'string', 'minLength': 1, 'maxLength': 255,
    'pattern': valid_cell_name_regex,
}


cell_name_leading_trailing_spaces = {
    'type': 'string', 'minLength': 1, 'maxLength': 255,
    'pattern': valid_cell_name_leading_trailing_spaces_regex,
}


name_with_leading_trailing_spaces = {
    'type': 'string', 'minLength': 1, 'maxLength': 255,
    'pattern': valid_name_leading_trailing_spaces_regex,
}


tcp_udp_port = {
    'type': ['integer', 'string'], 'pattern': '^[0-9]*$',
    'minimum': 0, 'maximum': 65535,
    'minLength': 1
}


project_id = {
    'type': 'string', 'minLength': 1, 'maxLength': 255,
    'pattern': '^[a-zA-Z0-9-]*$'
}


server_id = {
    'type': 'string', 'format': 'uuid'
}


image_id = {
    'type': 'string', 'format': 'uuid'
}


volume_id = {
    'type': 'string', 'format': 'uuid'
}


network_id = {
    'type': 'string', 'format': 'uuid'
}


network_port_id = {
    'type': 'string', 'format': 'uuid'
}


admin_password = {
    # NOTE: admin_password is the admin password of a server
    # instance, and it is not stored into nova's data base.
    # In addition, users set sometimes long/strange string
    # as password. It is unnecessary to limit string length
    # and string pattern.
    'type': 'string',
}


image_ref = {
    'type': 'string',
}


flavor_ref = {
    'type': ['string', 'integer'], 'minLength': 1
}


metadata = {
    'type': 'object',
    'patternProperties': {
        '^[a-zA-Z0-9-_:. ]{1,255}$': {
            'type': 'string', 'maxLength': 255
        }
    },
    'additionalProperties': False
}


metadata_with_null = copy.deepcopy(metadata)
metadata_with_null['patternProperties']['^[a-zA-Z0-9-_:. ]{1,255}$']['type'] =\
    ['string', 'null']


mac_address = {
    'type': 'string',
    'pattern': '^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$'
}


ip_address = {
    'type': 'string',
    'oneOf': [
        {'format': 'ipv4'},
        {'format': 'ipv6'}
    ]
}


ipv4 = {
    'type': 'string', 'format': 'ipv4'
}


ipv6 = {
    'type': 'string', 'format': 'ipv6'
}


cidr = {
    'type': 'string', 'format': 'cidr'
}
