import unittest
import os
from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhase74(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_tool_synthesis_agent(self) -> None:
        print("\nTesting Phase 74: Dynamic Tool Synthesis...")
        
        # Synthesize
        res = self.fleet.tool_synthesis.synthesize_tool("CSV Parsing", "Read CSV and sum column A")
        print(f"Synthesis Result: {res}")
        self.assertEqual(res["status"], "synthesized")
        
        tool_name = res["tool_name"]
        
        # Check tools
        tools = self.fleet.tool_synthesis.get_available_tools()
        print(f"Available Tools: {tools}")
        self.assertEqual(len(tools), 1)
        
        # Feedback
        fb_res = self.fleet.tool_synthesis.analyze_feedback(tool_name, "Works well on small files")
        print(f"Feedback Result: {fb_res}")
        self.assertEqual(fb_res["status"], "feedback_logged")

if __name__ == "__main__":
    unittest.main()
