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
Test Phase73 module.
"""

import unittest
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase73(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_dependency_graph_agent(self) -> None:
        print("\nTesting Phase 73: Semantic Versioning & Dependency Graphing...")

        # Scan a small subset for speed in test

        res = self.fleet.dependency_graph.scan_dependencies(
            start_dir="src/logic/agents"
        )
        print(f"Scan Result: {res}")
        self.assertGreater(res["modules_scanned"], 0)

        # Check impact

        impact = self.fleet.dependency_graph.get_impact_scope("os")
        print(f"Impact of 'os': {impact}")
        # CoreEvolutionGuard should be in there
        self.assertTrue(any("core_evolution_guard" in m.lower() for m in impact))

        # Stats
        stats = self.fleet.dependency_graph.generate_graph_stats()
        print(f"Graph Stats: {stats}")
        self.assertGreater(stats["node_count"], 0)


if __name__ == "__main__":
    unittest.main()