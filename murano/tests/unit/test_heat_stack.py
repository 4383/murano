# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from heatclient.v1 import stacks
import mock
from oslo_config import cfg

from murano.engine.system import heat_stack
from murano.tests.unit import base

CLS_NAME = 'murano.engine.system.heat_stack.HeatStack'
CONF = cfg.CONF


class TestHeatStack(base.MuranoTestCase):
    def setUp(self):
        super(TestHeatStack, self).setUp()
        self.heat_client_mock = mock.Mock()
        self.heat_client_mock.stacks = mock.MagicMock(spec=stacks.StackManager)
        CONF.set_override('stack_tags', ['test-murano'], 'heat',
                          enforce_type=True)
        self.mock_tag = ','.join(CONF.heat.stack_tags)
        heat_stack.HeatStack._get_token_client = mock.Mock(
            return_value=self.heat_client_mock)
        heat_stack.HeatStack._get_client = mock.Mock(
            return_value=self.heat_client_mock)

    @mock.patch(CLS_NAME + '._wait_state')
    @mock.patch(CLS_NAME + '._get_status')
    def test_push_adds_version(self, status_get, wait_st):
        """Assert that if heat_template_version is omitted, it's added."""

        status_get.return_value = 'NOT_FOUND'
        wait_st.return_value = {}
        hs = heat_stack.HeatStack('test-stack', 'Generated by TestHeatStack')
        hs._template = {'resources': {'test': 1}}
        hs._files = {}
        hs._hot_environment = ''
        hs._parameters = {}
        hs._applied = False
        hs.push()

        hs = heat_stack.HeatStack(
            'test-stack', 'Generated by TestHeatStack')
        hs._template = {'resources': {'test': 1}}
        hs._files = {}
        hs._parameters = {}
        hs._applied = False
        hs.push()

        expected_template = {
            'heat_template_version': '2013-05-23',
            'description': 'Generated by TestHeatStack',
            'resources': {'test': 1}
        }
        self.heat_client_mock.stacks.create.assert_called_with(
            stack_name='test-stack',
            disable_rollback=True,
            parameters={},
            template=expected_template,
            files={},
            environment='',
            tags=self.mock_tag
        )
        self.assertTrue(hs._applied)

    @mock.patch(CLS_NAME + '._wait_state')
    @mock.patch(CLS_NAME + '._get_status')
    def test_description_is_optional(self, status_get, wait_st):
        """Assert that if heat_template_version is omitted, it's added."""

        status_get.return_value = 'NOT_FOUND'
        wait_st.return_value = {}
        hs = heat_stack.HeatStack('test-stack', None)
        hs._template = {'resources': {'test': 1}}
        hs._files = {}
        hs._hot_environment = ''
        hs._parameters = {}
        hs._applied = False
        hs.push()

        expected_template = {
            'heat_template_version': '2013-05-23',
            'resources': {'test': 1}
        }
        self.heat_client_mock.stacks.create.assert_called_with(
            stack_name='test-stack',
            disable_rollback=True,
            parameters={},
            template=expected_template,
            files={},
            environment='',
            tags=self.mock_tag
        )
        self.assertTrue(hs._applied)

    @mock.patch(CLS_NAME + '._wait_state')
    @mock.patch(CLS_NAME + '._get_status')
    def test_heat_files_are_sent(self, status_get, wait_st):
        """Assert that if heat_template_version is omitted, it's added."""

        status_get.return_value = 'NOT_FOUND'
        wait_st.return_value = {}
        hs = heat_stack.HeatStack('test-stack', None)
        hs._description = None
        hs._template = {'resources': {'test': 1}}
        hs._files = {"heatFile": "file"}
        hs._hot_environment = ''
        hs._parameters = {}
        hs._applied = False
        hs.push()

        expected_template = {
            'heat_template_version': '2013-05-23',
            'resources': {'test': 1}
        }
        self.heat_client_mock.stacks.create.assert_called_with(
            stack_name='test-stack',
            disable_rollback=True,
            parameters={},
            template=expected_template,
            files={"heatFile": "file"},
            environment='',
            tags=self.mock_tag
        )
        self.assertTrue(hs._applied)

    @mock.patch(CLS_NAME + '._wait_state')
    @mock.patch(CLS_NAME + '._get_status')
    def test_heat_environments_are_sent(self, status_get, wait_st):
        """Assert that if heat_template_version is omitted, it's added."""

        status_get.return_value = 'NOT_FOUND'
        wait_st.return_value = {}
        hs = heat_stack.HeatStack('test-stack', None)
        hs._description = None
        hs._template = {'resources': {'test': 1}}
        hs._files = {"heatFile": "file"}
        hs._hot_environment = 'environments'
        hs._parameters = {}
        hs._applied = False
        hs.push()

        expected_template = {
            'heat_template_version': '2013-05-23',
            'resources': {'test': 1}
        }
        self.heat_client_mock.stacks.create.assert_called_with(
            stack_name='test-stack',
            disable_rollback=True,
            parameters={},
            template=expected_template,
            files={"heatFile": "file"},
            environment='environments',
            tags=self.mock_tag
        )
        self.assertTrue(hs._applied)

    @mock.patch(CLS_NAME + '._wait_state')
    @mock.patch(CLS_NAME + '._get_status')
    def test_heat_async_push(self, status_get, wait_st):
        """Assert that if heat_template_version is omitted, it's added."""

        status_get.return_value = 'NOT_FOUND'
        wait_st.return_value = {}
        hs = heat_stack.HeatStack('test-stack', None)
        hs._description = None
        hs._template = {'resources': {'test': 1}}
        hs._files = {"heatFile": "file"}
        hs._hot_environment = 'environments'
        hs._parameters = {}
        hs._applied = False
        hs.push(async=True)

        expected_template = {
            'heat_template_version': '2013-05-23',
            'resources': {'test': 1}
        }
        self.heat_client_mock.stacks.create.assert_not_called()
        hs.output()
        self.heat_client_mock.stacks.create.assert_called_with(
            stack_name='test-stack',
            disable_rollback=True,
            parameters={},
            template=expected_template,
            files={"heatFile": "file"},
            environment='environments',
            tags=self.mock_tag
        )
        self.assertTrue(hs._applied)

    @mock.patch(CLS_NAME + '.current')
    def test_update_wrong_template_version(self, current):
        """Template version other than expected should cause error."""

        hs = heat_stack.HeatStack(
            'test-stack', 'Generated by TestHeatStack')
        hs._template = {'resources': {'test': 1}}

        invalid_template = {
            'heat_template_version': 'something else'
        }

        current.return_value = {}

        e = self.assertRaises(heat_stack.HeatStackError,
                              hs.update_template,
                              invalid_template)
        err_msg = "Currently only heat_template_version 2013-05-23 "\
                  "is supported."
        self.assertEqual(err_msg, str(e))

        # Check it's ok without a version
        hs.update_template({})
        expected = {'resources': {'test': 1}}
        self.assertEqual(expected, hs._template)

        # .. or with a good version
        hs.update_template({'heat_template_version': '2013-05-23'})
        expected['heat_template_version'] = '2013-05-23'
        self.assertEqual(expected, hs._template)

    @mock.patch(CLS_NAME + '._wait_state')
    @mock.patch(CLS_NAME + '._get_status')
    def test_heat_stack_tags_are_sent(self, status_get, wait_st):
        """Assert heat_stack tags are sent

        Assert that heat_stack `tags` parameter get push & with
        value from config parameter `stack_tags`.
        """

        status_get.return_value = 'NOT_FOUND'
        wait_st.return_value = {}
        CONF.set_override('stack_tags', ['test-murano', 'murano-tag'], 'heat',
                          enforce_type=True)
        hs = heat_stack.HeatStack('test-stack', None)
        hs._description = None
        hs._template = {'resources': {'test': 1}}
        hs._files = {}
        hs._hot_environment = ''
        hs._parameters = {}
        hs._applied = False
        hs._tags = ','.join(CONF.heat.stack_tags)
        hs.push()

        expected_template = {
            'heat_template_version': '2013-05-23',
            'resources': {'test': 1}
        }
        self.heat_client_mock.stacks.create.assert_called_with(
            stack_name='test-stack',
            disable_rollback=True,
            parameters={},
            template=expected_template,
            files={},
            environment='',
            tags=','.join(CONF.heat.stack_tags)
        )
        self.assertTrue(hs._applied)
