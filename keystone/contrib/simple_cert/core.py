# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystone.common import extension

EXTENSION_DATA = {
    'name': 'OpenStack Simple Certificate API',
    'namespace': 'http://docs.openstack.org/identity/api/ext/'
                 'OS-SIMPLE-CERT/v1.0',
    'alias': 'OS-SIMPLE-CERT',
    'updated': '2014-01-20T12:00:0-00:00',
    'description': 'OpenStack simple certificate retrieval extension',
    'links': [
        {
            'rel': 'describedby',
            'type': 'text/html',
            'href': 'http://developer.openstack.org/'
                    'api-ref-identity-v2-ext.html',
        }
    ]}
extension.register_admin_extension(EXTENSION_DATA['alias'], EXTENSION_DATA)
extension.register_public_extension(EXTENSION_DATA['alias'], EXTENSION_DATA)