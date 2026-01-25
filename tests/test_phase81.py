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
Test Phase81 module.
"""

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.classes.specialized.ResearchSynthesisAgent import ResearchSynthesisAgent

class TestResearchSynthesis(unittest.TestCase):
    def setUp(self):
        self.agent = ResearchSynthesisAgent(os.getcwd())

    def test_research_cycle(self) -> None:
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

    def test_metrics(self) -> None:
        self.agent.conduct_research("AI Safety", ["Alignment", "Oversight"])
        metrics = self.agent.get_research_metrics()
        self.assertEqual(metrics['topics_researched'], 1)
        self.assertTrue(metrics['total_insights_generated'] > 0)

if __name__ == "__main__":
    unittest.main()