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
Test Phase123 Discovery module.
"""

import unittest
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
from pathlib import Path
import time


class TestPhase123Discovery(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.root)

    def test_discovery_orchestrator_initialization(self) -> None:
        # Accessing it should trigger __init__ and start thread
        discovery = self.fleet.orchestrators.discovery
        self.assertIsNotNone(discovery)
        self.assertTrue(hasattr(discovery, "zeroconf"))

    def test_discovery_advertising(self) -> None:
        discovery = self.fleet.orchestrators.discovery
        # Give it a few seconds to start the thread and register
        time.sleep(5)
        self.assertTrue(discovery._is_advertising)

    def tearDown(self):
        if hasattr(self.fleet.orchestrators, "discovery"):
            self.fleet.orchestrators.discovery.shutdown()


if __name__ == "__main__":
    unittest.main()
