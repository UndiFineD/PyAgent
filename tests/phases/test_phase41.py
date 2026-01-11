#!/usr/bin/env python3

import os
import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.append(os.getcwd())

from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhase41(unittest.TestCase):
    def setUp(self):
        self.workspace = os.getcwd()
        self.fleet = FleetManager(self.workspace)

    def test_byzantine_consensus(self):
        print("\nTesting ByzantineConsensusAgent...")
        judge = self.fleet.byzantine_judge
        proposals = {
            "AgentA": "def hello(): return 'world'",
            "AgentB": "def hello(): return 'world' # Improved",
            "AgentC": "TODO: implement"
        }
        result = judge.run_committee_vote("Write a hello world function", proposals)
        self.assertEqual(result["decision"], "ACCEPTED")
        self.assertIn(result["winner"], ["AgentA", "AgentB"])
        self.assertTrue(result["consensus_stats"]["avg_integrity"] > 0.5)

    def test_federated_knowledge(self):
        print("\nTesting FederatedKnowledgeOrchestrator...")
        fk = self.fleet.federated_knowledge
        result = fk.run_fleet_wide_sync()
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["fused_insights"] > 0)
        
    def test_sql_bug_fix(self):
        print("\nTesting SQLAgent bug fix...")
        sql_agent = self.fleet.sql
        # Should not raise AttributeError now
        res = sql_agent.improve_content("Show me tables")
        self.assertIn("Connection active", res)

if __name__ == "__main__":
    unittest.main()
