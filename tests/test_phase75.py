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
Test Phase75 module.
"""

import unittest
import time
from src.classes.fleet.FleetManager import FleetManager

class TestPhase75(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_memory_replay_agent(self) -> None:
        print("\nTesting Phase 75: Bio-Mimetic Memory Replay...")
        
        # Simulated episodic memories
        memories = [
            {"id": "m1", "action": "test_fix", "content": "Fixed bug in auth module", "success": True},
            {"id": "m2", "action": "read_file", "content": "Just reading readme", "success": True},
            {"id": "m3", "action": "run_error", "content": "Syntax error in main.py", "success": False},
        ]
        
        # Start sleep cycle
        res = self.fleet.memory_replay.start_sleep_cycle(memories)
        print(f"Sleep Cycle Result: {res}")
        self.assertEqual(res["memories_processed"], 3)
        self.assertIn("consolidated", res)
        self.assertIn("pruned", res)

        # Check insights
        log = self.fleet.memory_replay.get_dream_log()
        print(f"Dream Log: {log}")
        self.assertGreaterEqual(log["insights_count"], 0)

if __name__ == "__main__":
    unittest.main()