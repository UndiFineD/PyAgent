import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.logic.agents.intelligence.ResearchSynthesisAgent import ResearchSynthesisAgent

class TestResearchSynthesis(unittest.TestCase):
    def setUp(self):
        self.agent = ResearchSynthesisAgent(os.getcwd())

    def test_research_cycle(self):
        topic = "Quantum Computing in 2025"
        focus = ["Error Correction", "Room Temp Qubits", "Cloud Access"]
        
        result = self.agent.conduct_research(topic, focus)
        
        self.assertEqual(result['topic'], topic)
        self.assertEqual(result['findings_count'], 3)
        self.assertIn("Synthesized", result['summary'])
        
        # Test library query
        query_results = self.agent.query_library("Quantum")
        self.assertTrue(len(query_results) >= 1)
        self.assertEqual(query_results[0]['topic'], topic)

    def test_metrics(self):
        self.agent.conduct_research("AI Safety", ["Alignment", "Oversight"])
        metrics = self.agent.get_research_metrics()
        self.assertEqual(metrics['topics_researched'], 1)
        self.assertTrue(metrics['total_insights_generated'] > 0)

if __name__ == "__main__":
    unittest.main()
