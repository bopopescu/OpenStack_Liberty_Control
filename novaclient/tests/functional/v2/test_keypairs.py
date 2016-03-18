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

import tempest_lib.cli.base

from novaclient.tests.functional import base
from novaclient.tests.functional.v2 import fake_crypto
from novaclient.tests.functional.v2.legacy import test_keypairs


class TestKeypairsNovaClientV22(test_keypairs.TestKeypairsNovaClient):
    """Keypairs functional tests for v2.2 nova-api microversion."""

    COMPUTE_API_VERSION = "2.2"

    def test_create_keypair(self):
        keypair = super(TestKeypairsNovaClientV22, self).test_create_keypair()
        self.assertIn('ssh', keypair)

    def test_create_keypair_x509(self):
        key_name = self._create_keypair(key_type='x509')
        keypair = self._show_keypair(key_name)
        self.assertIn(key_name, keypair)
        self.assertIn('x509', keypair)

    def test_import_keypair(self):
        pub_key, fingerprint = fake_crypto.get_ssh_pub_key_and_fingerprint()
        pub_key_file = self._create_public_key_file(pub_key)
        keypair = self._test_import_keypair(fingerprint, pub_key=pub_key_file)
        self.assertIn('ssh', keypair)

    def test_import_keypair_x509(self):
        certif, fingerprint = fake_crypto.get_x509_cert_and_fingerprint()
        pub_key_file = self._create_public_key_file(certif)
        keypair = self._test_import_keypair(fingerprint, key_type='x509',
                                            pub_key=pub_key_file)
        self.assertIn('x509', keypair)


class TestKeypairsNovaClientV210(base.ClientTestBase):
    """Keypairs functional tests for v2.10 nova-api microversion.
    """

    COMPUTE_API_VERSION = "2.10"

    def setUp(self):
        super(TestKeypairsNovaClientV210, self).setUp()
        user_name = self.name_generate("v2.10")
        password = "password"
        user = self.cli_clients.keystone(
            "user-create --name %(name)s --pass %(pass)s --tenant %(tenant)s" %
            {"name": user_name, "pass": password,
             "tenant": self.cli_clients.tenant_name})
        self.user_id = self._get_value_from_the_table(user, "id")
        self.addCleanup(self.cli_clients.keystone,
                        "user-delete %s" % self.user_id)
        self.cli_clients_2 = tempest_lib.cli.base.CLIClient(
            username=user_name,
            password=password,
            tenant_name=self.cli_clients.tenant_name,
            uri=self.cli_clients.uri,
            cli_dir=self.cli_clients.cli_dir)

    def another_nova(self, action, flags='', params='', fail_ok=False,
                     endpoint_type='publicURL', merge_stderr=False):
        flags += " --os-compute-api-version %s " % self.COMPUTE_API_VERSION
        return self.cli_clients_2.nova(action, flags, params, fail_ok,
                                       endpoint_type, merge_stderr)

    def test_create_and_list_keypair(self):
        name = self.name_generate("v2_10")
        self.nova("keypair-add %s --user %s" % (name, self.user_id))
        self.addCleanup(self.another_nova, "keypair-delete %s" % name)
        output = self.nova("keypair-list")
        self.assertRaises(ValueError, self._get_value_from_the_table,
                          output, name)
        output_1 = self.another_nova("keypair-list")
        output_2 = self.nova("keypair-list --user %s" % self.user_id)
        self.assertEqual(output_1, output_2)
        # it should be table with one key-pair
        self.assertEqual(name, self._get_column_value_from_single_row_table(
            output_1, "Name"))

        output_1 = self.another_nova("keypair-show %s " % name)
        output_2 = self.nova("keypair-show --user %s %s" % (self.user_id,
                                                            name))
        self.assertEqual(output_1, output_2)
        self.assertEqual(self.user_id,
                         self._get_value_from_the_table(output_1, "user_id"))

    def test_create_and_delete(self):
        name = self.name_generate("v2_10")

        def cleanup():
            # We should check keypair existence and remove it from correct user
            # if keypair is presented
            o = self.another_nova("keypair-list")
            if name in o:
                self.another_nova("keypair-delete %s" % name)

        self.nova("keypair-add %s --user %s" % (name, self.user_id))
        self.addCleanup(cleanup)
        output = self.another_nova("keypair-list")
        self.assertEqual(name, self._get_column_value_from_single_row_table(
            output, "Name"))

        self.nova("keypair-delete %s --user %s " % (name, self.user_id))
        output = self.another_nova("keypair-list")
        self.assertRaises(
            ValueError,
            self._get_column_value_from_single_row_table, output, "Name")
