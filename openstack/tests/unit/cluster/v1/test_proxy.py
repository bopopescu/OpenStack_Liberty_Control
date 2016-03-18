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

from openstack.cluster.v1 import _proxy
from openstack.cluster.v1 import action
from openstack.cluster.v1 import build_info
from openstack.cluster.v1 import cluster
from openstack.cluster.v1 import cluster_policy
from openstack.cluster.v1 import event
from openstack.cluster.v1 import node
from openstack.cluster.v1 import policy
from openstack.cluster.v1 import policy_type
from openstack.cluster.v1 import profile
from openstack.cluster.v1 import profile_type
from openstack.tests.unit import test_proxy_base


class TestClusterProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestClusterProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_build_info_get(self):
        self.verify_get(self.proxy.get_build_info, build_info.BuildInfo,
                        ignore_value=True)

    def test_profile_types(self):
        self.verify_list(self.proxy.profile_types,
                         profile_type.ProfileType,
                         paginated=False)

    def test_profile_type_get(self):
        self.verify_get(self.proxy.get_profile_type,
                        profile_type.ProfileType)

    def test_policy_types(self):
        self.verify_list(self.proxy.policy_types, policy_type.PolicyType,
                         paginated=False)

    def test_policy_type_get(self):
        self.verify_get(self.proxy.get_policy_type, policy_type.PolicyType)

    def test_profile_create(self):
        self.verify_create(self.proxy.create_profile, profile.Profile)

    def test_profile_delete(self):
        self.verify_delete(self.proxy.delete_profile, profile.Profile, False)

    def test_profile_delete_ignore(self):
        self.verify_delete(self.proxy.delete_profile, profile.Profile, True)

    def test_profile_find(self):
        self.verify_find(self.proxy.find_profile, profile.Profile)

    def test_profile_get(self):
        self.verify_get(self.proxy.get_profile, profile.Profile)

    def test_profiles(self):
        self.verify_list(self.proxy.profiles, profile.Profile,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_profile_update(self):
        self.verify_update(self.proxy.update_profile, profile.Profile)

    def test_cluster_create(self):
        self.verify_create(self.proxy.create_cluster, cluster.Cluster)

    def test_cluster_delete(self):
        self.verify_delete(self.proxy.delete_cluster, cluster.Cluster, False)

    def test_cluster_delete_ignore(self):
        self.verify_delete(self.proxy.delete_cluster, cluster.Cluster, True)

    def test_cluster_find(self):
        self.verify_find(self.proxy.find_cluster, cluster.Cluster)

    def test_cluster_get(self):
        self.verify_get(self.proxy.get_cluster, cluster.Cluster)

    def test_clusters(self):
        self.verify_list(self.proxy.clusters, cluster.Cluster,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_cluster_update(self):
        self.verify_update(self.proxy.update_cluster, cluster.Cluster)

    def test_node_create(self):
        self.verify_create(self.proxy.create_node, node.Node)

    def test_node_delete(self):
        self.verify_delete(self.proxy.delete_node, node.Node, False)

    def test_node_delete_ignore(self):
        self.verify_delete(self.proxy.delete_node, node.Node, True)

    def test_node_find(self):
        self.verify_find(self.proxy.find_node, node.Node)

    def test_node_get(self):
        self.verify_get(self.proxy.get_node, node.Node)

    def test_nodes(self):
        self.verify_list(self.proxy.nodes, node.Node,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_node_update(self):
        self.verify_update(self.proxy.update_node, node.Node)

    def test_policy_create(self):
        self.verify_create(self.proxy.create_policy, policy.Policy)

    def test_policy_delete(self):
        self.verify_delete(self.proxy.delete_policy, policy.Policy, False)

    def test_policy_delete_ignore(self):
        self.verify_delete(self.proxy.delete_policy, policy.Policy, True)

    def test_policy_find(self):
        self.verify_find(self.proxy.find_policy, policy.Policy)

    def test_policy_get(self):
        self.verify_get(self.proxy.get_policy, policy.Policy)

    def test_policies(self):
        self.verify_list(self.proxy.policies, policy.Policy,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_policy_update(self):
        self.verify_update(self.proxy.update_policy, policy.Policy)

    def test_cluster_policies(self):
        self.verify_list(self.proxy.cluster_policies,
                         cluster_policy.ClusterPolicy,
                         paginated=False, method_args=["FAKE_CLUSTER"],
                         expected_kwargs={"path_args": {
                             "cluster_id": "FAKE_CLUSTER"}})

    def test_get_cluster_policies(self):
        fake_policy = policy.Policy.from_id("FAKE_POLICY")
        fake_cluster = cluster.Cluster.from_id('FAKE_CLUSTER')

        # Policy object as input
        self._verify2('openstack.proxy.BaseProxy._get',
                      self.proxy.get_cluster_policy,
                      method_args=[fake_policy, "FAKE_CLUSTER"],
                      expected_args=[cluster_policy.ClusterPolicy,
                                     'FAKE_POLICY'],
                      expected_kwargs={"path_args": {
                          "cluster_id": "FAKE_CLUSTER"}})

        # Policy ID as input
        self._verify2('openstack.proxy.BaseProxy._get',
                      self.proxy.get_cluster_policy,
                      method_args=["FAKE_POLICY", "FAKE_CLUSTER"],
                      expected_args=[cluster_policy.ClusterPolicy,
                                     "FAKE_POLICY"],
                      expected_kwargs={"path_args": {
                          "cluster_id": "FAKE_CLUSTER"}})

        # Cluster object as input
        self._verify2('openstack.proxy.BaseProxy._get',
                      self.proxy.get_cluster_policy,
                      method_args=["FAKE_POLICY", fake_cluster],
                      expected_args=[cluster_policy.ClusterPolicy,
                                     "FAKE_POLICY"],
                      expected_kwargs={"path_args": {
                          "cluster_id": "FAKE_CLUSTER"}})

    def test_action_get(self):
        self.verify_get(self.proxy.get_action, action.Action)

    def test_actions(self):
        self.verify_list(self.proxy.actions, action.Action,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_event_get(self):
        self.verify_get(self.proxy.get_event, event.Event)

    def test_events(self):
        self.verify_list(self.proxy.events, event.Event,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})