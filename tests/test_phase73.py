import unittest
import os
from src.classes.fleet.FleetManager import FleetManager

class TestPhase73(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_dependency_graph_agent(self) -> None:
        print("\nTesting Phase 73: Semantic Versioning & Dependency Graphing...")
        
        # Scan a small subset for speed in test
        res = self.fleet.dependency_graph.scan_dependencies(start_dir="src/classes/specialized")
        print(f"Scan Result: {res}")
        self.assertGreater(res["modules_scanned"], 0)
        
        # Check impact
        impact = self.fleet.dependency_graph.get_impact_scope("os")
        print(f"Impact of 'os': {impact}")
        # CoreEvolutionGuard should be in there
        self.assertTrue(any("CoreEvolutionGuard" in m for m in impact))
        
        # Stats
        stats = self.fleet.dependency_graph.generate_graph_stats()
        print(f"Graph Stats: {stats}")
        self.assertGreater(stats["node_count"], 0)

if __name__ == "__main__":
    unittest.main()
