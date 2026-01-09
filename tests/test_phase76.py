import unittest
from src.classes.fleet.FleetManager import FleetManager

class TestPhase76(unittest.TestCase):
    def setUp(self):
        self.workspace = "c:/DEV/PyAgent"
        self.fleet = FleetManager(self.workspace)

    def test_swarm_distillation_agent(self):
        print("\nTesting Phase 76: Neural Swarm Compression & Distillation...")
        
        # Knowledge data from agents
        coder_kb = {"specialty": "python_refactoring", "patterns": {"async_io": 0.9, "type_hints": 0.8}, "metrics": {"files_improved": 45}}
        tester_kb = {"specialty": "unit_tests", "patterns": {"pytest_fixtures": 0.95}, "metrics": {"coverage_avg": 0.88}}
        
        # Distill
        res1 = self.fleet.swarm_distillation.distill_agent_knowledge("CoderAgent", coder_kb)
        res2 = self.fleet.swarm_distillation.distill_agent_knowledge("TesterAgent", tester_kb)
        
        print(f"Distilled Coder: {res1}")
        self.assertEqual(res1["agent"], "CoderAgent")
        
        # Get unified context
        unified = self.fleet.swarm_distillation.get_unified_context()
        print(f"Unified Context: {unified}")
        self.assertIn("CoderAgent", unified["distilled_indices"])
        self.assertIn("TesterAgent", unified["distilled_indices"])
        self.assertEqual(len(unified["distilled_indices"]), 2)

if __name__ == "__main__":
    unittest.main()
