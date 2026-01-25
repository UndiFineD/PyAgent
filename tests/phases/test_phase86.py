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
Test Phase86 module.
"""

import unittest
import time

# Ensure the project root is in PYTHONPATH

from src.infrastructure.swarm.orchestration.healing.self_healing_orchestrator import (
    SelfHealingOrchestrator,
)


class TestSelfHealing(unittest.TestCase):
    def setUp(self):
        # Mock fleet manager with an agents object having try_reload
        from unittest.mock import MagicMock

        self.mock_fleet = MagicMock()
        self.mock_fleet.agents = MagicMock()
        self.mock_fleet.agents.try_reload.return_value = True
        self.orchestrator = SelfHealingOrchestrator(self.mock_fleet)

    def test_heartbeat_and_recovery(self) -> None:
        # Register a healthy agent
        self.orchestrator.register_heartbeat("AgentX", {"key": "value"})
        self.assertIn("AgentX", self.orchestrator.health_registry)

        # Simulate time passing (backdating the heartbeat)
        self.orchestrator.health_registry["AgentX"].last_seen = time.time() - 60

        # Check health - should trigger recovery
        self.orchestrator.check_fleet_health()

        status = self.orchestrator.get_recovery_status()
        self.assertEqual(status["total_recoveries"], 1)

        self.assertEqual(status["recent_actions"][0]["agent"], "AgentX")
        self.assertTrue(status["recent_actions"][0]["state_restored"])

    def test_no_recovery_for_healthy_agent(self) -> None:
        self.orchestrator.register_heartbeat("AgentY")

        self.orchestrator.check_fleet_health()

        status = self.orchestrator.get_recovery_status()
        self.assertEqual(status["total_recoveries"], 0)


if __name__ == "__main__":
    unittest.main()