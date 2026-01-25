#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test Phase74 module.
"""

import unittest
import os
from src.classes.fleet.FleetManager import FleetManager

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