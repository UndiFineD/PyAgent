#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test Phase90 module.
"""

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.classes.specialized.SwarmDeploymentAgent import SwarmDeploymentAgent

class TestSwarmDeployment(unittest.TestCase):
    def setUp(self):
        self.agent = SwarmDeploymentAgent(os.getcwd())

    def test_provision(self) -> None:
        node = self.agent.provision_node("Compute", "us-west-2")
        self.assertEqual(node['node_type'], "Compute")
        self.assertEqual(node['region'], "us-west-2")
        self.assertIn("DEP-", node['deployment_id'])

    def test_scaling(self) -> None:
        new_nodes = self.agent.scale_swarm(3, "Storage")
        self.assertEqual(len(new_nodes), 3)
        inventory = self.agent.get_deployment_inventory()
        self.assertEqual(inventory['total_nodes'], 3)

if __name__ == "__main__":
    unittest.main()