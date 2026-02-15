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
Test Phase94 module.
"""

import unittest

# Ensure the project root is in PYTHONPATH

from src.infrastructure.swarm.orchestration.connectivity.multi_cloud_bridge_orchestrator import (
    MultiCloudBridgeOrchestrator,
)


class TestMultiCloudBridge(unittest.TestCase):
    def setUp(self):
        self.orchestrator = MultiCloudBridgeOrchestrator(None)

    def test_registration_and_sync(self) -> None:
        self.orchestrator.register_cloud_node("AWS-01", "AWS", "us-east-1")
        self.orchestrator.register_cloud_node("AZ-01", "Azure", "eastus")

        topology = self.orchestrator.get_bridge_topology()
        self.assertEqual(topology["total_nodes"], 2)

        sync = self.orchestrator.sync_state_cross_cloud({"data": 123}, "AWS")
        self.assertEqual(sync["nodes_synced"], 1)  # Synced to Azure

        self.assertIn("Azure", sync["targets"])

    def test_routing(self) -> None:
        self.orchestrator.register_cloud_node("GCP-01", "GCP", "us-central1")
        success = self.orchestrator.route_message("Hello GCP", "GCP")

        self.assertTrue(success)

        fail = self.orchestrator.route_message("Hello AWS", "AWS")
        self.assertFalse(fail)


if __name__ == "__main__":
    unittest.main()
