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
Test Phase77 module.
"""

import unittest
from src.classes.fleet.FleetManager import FleetManager

class TestPhase77(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_fleet_economy_agent(self) -> None:
        print("\nTesting Phase 77: Autonomous Agent Financials & Bidding...")
        
        # Setup wallets
        self.fleet.fleet_economy.deposit_credits("AgentA", 100.0)
        self.fleet.fleet_economy.deposit_credits("AgentB", 50.0)
        
        # Place bids
        bid1 = self.fleet.fleet_economy.place_bid("AgentA", "task_refactor", 20.0, priority=2)
        bid2 = self.fleet.fleet_economy.place_bid("AgentB", "task_test", 10.0, priority=1)
        
        print(f"Bid 1: {bid1}")
        self.assertEqual(bid1["status"], "bid_placed")
        
        # Resolve
        resolution = self.fleet.fleet_economy.resolve_bids()
        print(f"Bid Resolution: {resolution}")
        self.assertIn("task_refactor", resolution["allocated_tasks"])
        self.assertEqual(resolution["allocated_tasks"][0], "task_refactor")

if __name__ == "__main__":
    unittest.main()