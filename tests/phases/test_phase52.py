import unittest
from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhase52(unittest.TestCase):
    def setUp(self):
        self.fleet = FleetManager("c:/DEV/PyAgent")

    def test_neuro_optimization(self):
        print("\nTesting Phase 52: Evolutionary Neuro-Optimization...")
        # Mock fleet stats
        stats = {
            "LinguisticAgent": {"success_rate": 0.5, "avg_latency": 1.2}, # Failing
            "ReasoningAgent": {"success_rate": 0.95, "avg_latency": 4.5}   # Succeeding
        }
        
        optimized = self.fleet.evolution.optimize_hyperparameters(stats)
        print(f"Optimized Params: {optimized}")
        
        # Checking logic
        self.assertLess(optimized["LinguisticAgent"]["temperature"], 0.7)
        self.assertGreater(optimized["ReasoningAgent"]["temperature"], 0.7)

if __name__ == "__main__":
    unittest.main()
