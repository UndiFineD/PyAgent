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
Test Phase42 module.
"""

#!/usr/bin/env python3

import os
import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase

# Add src to path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase42(IsolatedAsyncioTestCase):
    def setUp(self):
        self.workspace = os.getcwd()
        self.fleet = FleetManager(self.workspace)

    async def test_reward_model_ranking(self) -> None:
        print("\nTesting RewardModelAgent...")
        rm = self.fleet.reward_model
        proposals = {
            "Agent_Good": "def add(a, b): return a + b",
            "Agent_Bad": "def add(a, b): pass # TODO",
        }
        # Check if async
        res = rm.rank_proposals("Write an addition function", proposals)
        if asyncio.iscoroutine(res):
            result = await res
        else:
            result = res

        self.assertIn("ranking", result)
        self.assertIn("scores", result)
        # In our simulated logic, Good should be higher
        self.assertGreater(
            result["scores"].get("Agent_Good", 0), result["scores"].get("Agent_Bad", 10)
        )

    async def test_byzantine_consensus_real(self) -> None:
        print("\nTesting ByzantineConsensus with real AI scoring...")
        judge = self.fleet.byzantine_judge
        proposals = {
            "CoderA": "print('hello')",
            "CoderB": "print('hello world')",
            "Broken": "prnt('error')",
        }
        # This will trigger subagent calls for scoring
        res = judge.run_committee_vote("Print hello world", proposals)

        if asyncio.iscoroutine(res):
            result = await res
        else:
            result = res

        self.assertEqual(result["decision"], "ACCEPTED")
        self.assertNotEqual(result["winner"], "Broken")
        self.assertTrue(result["confidence"] > 0)

    async def test_federated_knowledge_broadcast(self) -> None:
        print("\nTesting Federated Knowledge broadcast...")
        fk = self.fleet.federated_knowledge
        res = fk.broadcast_lesson(
            "test_lesson",
            {
                "agent": "Tester",
                "task_type": "unit_test",
                "success": True,
                "fix": "Fixed bug X",
            },
        )
        if asyncio.iscoroutine(res):
            res = await res

        self.assertEqual(res["status"], "success")
        self.assertTrue(res["peer_count"] >= 1)


if __name__ == "__main__":
    unittest.main()