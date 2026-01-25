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
Test Phase76 module.
"""

import unittest
import asyncio
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase76(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_swarm_distillation_agent(self) -> None:
        print("\nTesting Phase 76: Neural Swarm Compression & Distillation...")

        # Knowledge data from agents
        coder_kb = {
            "specialty": "python_refactoring",
            "patterns": {"async_io": 0.9, "type_hints": 0.8},
            "metrics": {"files_improved": 45},
        }
        tester_kb = {
            "specialty": "unit_tests",
            "patterns": {"pytest_fixtures": 0.95},
            "metrics": {"coverage_avg": 0.88},
        }

        # Distill
        res1 = asyncio.run(self.fleet.swarm_distillation.distill_agent_knowledge(
            "CoderAgent", coder_kb
        ))
        res2 = asyncio.run(self.fleet.swarm_distillation.distill_agent_knowledge(
            "TesterAgent", tester_kb
        ))

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