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
Test Phase79 module.
"""

import unittest
import sys
from pathlib import Path

# Ensure src is in sys.path
root = Path(__file__).resolve().parents[2].parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase79(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_swarm_visualizer(self) -> None:
        print("\nTesting Phase 79: Neural Network Topology & Swarm Visualization...")

        # 1. Log interactions
        self.fleet.swarm_visualizer.log_interaction(
            "AgentA", "AgentB", "task_delegation"
        )

        self.fleet.swarm_visualizer.log_interaction("AgentB", "AgentC", "query")
        self.fleet.swarm_visualizer.log_interaction("AgentC", "AgentA", "response")

        # 2. Update positions

        self.fleet.swarm_visualizer.update_agent_position("AgentA", 10.0, 20.0)
        self.fleet.swarm_visualizer.update_agent_position("AgentB", 50.0, 50.0)

        # 3. Generate topology map
        topology = self.fleet.swarm_visualizer.generate_topology_map()

        print(f"Topology: {topology}")
        self.assertEqual(len(topology["nodes"]), 3)
        self.assertEqual(len(topology["edges"]), 3)

        # 4. Get visualization data

        viz_data = self.fleet.swarm_visualizer.get_visualization_data()
        print(f"Viz Data: {viz_data}")
        self.assertEqual(viz_data["metrics"]["total_interactions"], 3)
        self.assertEqual(viz_data["metrics"]["active_agents"], 2)


if __name__ == "__main__":
    unittest.main()