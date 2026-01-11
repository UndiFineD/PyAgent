import unittest
import time
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.orchestration.SelfHealingOrchestrator import SelfHealingOrchestrator

class TestSelfHealing(unittest.TestCase):
    def setUp(self):
        # Mock fleet manager
        self.orchestrator = SelfHealingOrchestrator(None)

    def test_heartbeat_and_recovery(self) -> None:
        # Register a healthy agent
        self.orchestrator.register_heartbeat("AgentX", {"key": "value"})
        self.assertIn("AgentX", self.orchestrator.health_registry)
        
        # Simulate time passing (backdating the heartbeat)
        self.orchestrator.health_registry["AgentX"] = time.time() - 15
        
        # Check health - should trigger recovery
        self.orchestrator.check_fleet_health()
        
        status = self.orchestrator.get_recovery_status()
        self.assertEqual(status['total_recoveries'], 1)
        self.assertEqual(status['recent_actions'][0]['agent'], "AgentX")
        self.assertTrue(status['recent_actions'][0]['state_restored'])

    def test_no_recovery_for_healthy_agent(self) -> None:
        self.orchestrator.register_heartbeat("AgentY")
        self.orchestrator.check_fleet_health()
        
        status = self.orchestrator.get_recovery_status()
        self.assertEqual(status['total_recoveries'], 0)

if __name__ == "__main__":
    unittest.main()
