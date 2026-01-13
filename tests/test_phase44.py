import unittest
import os
import shutil
import json
from src.classes.fleet.FleetManager import FleetManager

class TestPhase44(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Ensure directories exist
        os.makedirs(os.path.join(self.workspace, "models/forge/datasets"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace, "models/forge/adapters"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace, "agent_store"), exist_ok=True)

    def test_autonomous_fine_tuning(self) -> None:
        print("\nTesting Autonomous Fine-Tuning Trigger...")
        evolution_data = {
            "version": "v12",
            "synthetic_examples": [
                {"instruction": "Write a complex SQL query", "output": "SELECT * FROM agents JOIN capabilities..."},
                {"instruction": "Optimize for performance", "output": "Using indexed search..."}
            ]
        }
        res = self.fleet.model_forge.trigger_autonomous_tuning("SQLAgent", evolution_data)
        print(f"Result: {res}")
        self.assertIn("SUCCESS: Fine-tuning job", res)
        self.assertIn("Autonomous Tuning Initialized", res)
        
        # Verify adapter directory created
        self.assertTrue(os.path.exists(os.path.join(self.workspace, "models/forge/adapters/opt_SQLAgent_v12")))

    def test_weight_orchestration(self) -> None:
        print("\nTesting Weight Orchestration...")
        # Activate adapter
        self.fleet.weight_orchestrator.activate_adapter("SQLAgent", "opt_SQLAgent_v12")
        
        # Verify registration
        active = self.fleet.weight_orchestrator.get_active_adapter("SQLAgent")
        self.assertEqual(active, "opt_SQLAgent_v12")
        
        # List all
        regs = self.fleet.weight_orchestrator.list_registrations()
        self.assertIn("SQLAgent", regs)
        
        # Deactivate
        self.fleet.weight_orchestrator.deactivate_adapter("SQLAgent")
        self.assertIsNone(self.fleet.weight_orchestrator.get_active_adapter("SQLAgent"))

if __name__ == "__main__":
    unittest.main()
