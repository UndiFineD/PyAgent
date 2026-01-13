import unittest
from src.classes.fleet.FleetManager import FleetManager

class TestPhase52(unittest.TestCase):
    def setUp(self):
        self.fleet = FleetManager(Path(__file__).resolve().parents[2])

    def test_neuro_optimization(self) -> None:
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
