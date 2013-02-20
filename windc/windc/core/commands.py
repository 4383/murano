# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
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

TEMPLATE_DEPLOYMENT_COMMAND = "Template"
CHEF_COMMAND = "Chef"
CHEF_OP_CREATE_ENV = "Env"
CHEF_OP_CREATE_ROLE = "Role"
CHEF_OP_ASSIGN_ROLE = "AssignRole"
CHEF_OP_CREATE_NODE = "CRNode"

class Command:
	type = "Empty"
	context = None

	def __init__(self):
		self.type = "Empty"
		self.context = None
		self.data = None

	def __init__(self, type, context):
		self.type = type
		self.context = context

	def __init__(self, type, context, data):
		self.type = type
		self.context = context
		self.data = data


