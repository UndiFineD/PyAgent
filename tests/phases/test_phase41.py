#!/usr/bin/env python3

import os
import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase

# Add src to path

from src.infrastructure.fleet.FleetManager import FleetManager


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
