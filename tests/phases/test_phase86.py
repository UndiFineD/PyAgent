import unittest
import time

# Ensure the project root is in PYTHONPATH

from src.infrastructure.orchestration.healing.SelfHealingOrchestrator import (
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
