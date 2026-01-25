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
Test Phase41 module.
"""

#!/usr/bin/env python3

import os
import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase

# Add src to path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase41(IsolatedAsyncioTestCase):
    def setUp(self):
        self.workspace = os.getcwd()
        self.fleet = FleetManager(self.workspace)

    async def test_byzantine_consensus(self) -> None:
        print("\nTesting ByzantineConsensusAgent...")
        judge = self.fleet.byzantine_judge
        proposals = {
            "AgentA": "def hello(): return 'world'",
            "AgentB": "def hello(): return 'world' # Improved",
            "AgentC": "TODO: implement",
        }
        res = judge.run_committee_vote("Write a hello world function", proposals)
        if asyncio.iscoroutine(res):
            result = await res
        else:
            result = res
        self.assertEqual(result["decision"], "ACCEPTED")
        self.assertIn(result["winner"], ["AgentA", "AgentB"])
        self.assertTrue(result["consensus_stats"]["avg_integrity"] > 0.5)

    async def test_federated_knowledge(self) -> None:
        print("\nTesting FederatedKnowledgeOrchestrator...")

        fk = self.fleet.federated_knowledge
        res = fk.run_fleet_wide_sync()
        if asyncio.iscoroutine(res):
            result = await res

        else:
            result = res
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["fused_insights"] > 0)

    async def test_sql_bug_fix(self) -> None:
        print("\nTesting SQLAgent bug fix...")
        sql_agent = self.fleet.sql
        # Should not raise AttributeError now
        res = sql_agent.improve_content("Show me tables")

        if asyncio.iscoroutine(res):
            res = await res
        # Check for successful output OR graceful degradation (no crash)
        self.assertTrue(
            "Connection active" in res or "AI Improvement" in res or "GitHub CLI" in res
        )


if __name__ == "__main__":
    unittest.main()