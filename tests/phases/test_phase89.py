import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.infrastructure.orchestration.IntelligenceOrchestrator import IntelligenceOrchestrator

class TestIntelligence(unittest.TestCase):
    def setUp(self):
        self.orchestrator = IntelligenceOrchestrator(None)

    def test_synthesis(self) -> None:
        self.orchestrator.contribute_insight("AgentA", "Detected quantum fluctuation in memory", 0.9)
        self.orchestrator.contribute_insight("AgentB", "Quantum patterns appearing in the shard", 0.8)
        
        patterns = self.orchestrator.synthesize_collective_intelligence()
        self.assertTrue(any("quantum" in p.lower() for p in patterns))
        
        report = self.orchestrator.get_intelligence_report()
        self.assertEqual(report['insights_collected'], 2)
        self.assertEqual(report['patterns_identified'], 1)

if __name__ == "__main__":
    unittest.main()
