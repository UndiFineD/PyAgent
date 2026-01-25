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
import sys
import unittest
from pathlib import Path

# Add src to path

from src.classes.fleet.FleetManager import FleetManager

class TestPhase41(unittest.TestCase):
    def setUp(self):
        self.workspace = os.getcwd()
        self.fleet = FleetManager(self.workspace)

    def test_byzantine_consensus(self) -> None:
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

    def test_federated_knowledge(self) -> None:
        print("\nTesting FederatedKnowledgeOrchestrator...")
        fk = self.fleet.federated_knowledge
        result = fk.run_fleet_wide_sync()
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["fused_insights"] > 0)
        
    def test_sql_bug_fix(self) -> None:
        print("\nTesting SQLAgent bug fix...")
        sql_agent = self.fleet.sql
        # Should not raise AttributeError now
        res = sql_agent.improve_content("Show me tables")
        self.assertIn("Connection active", res)

if __name__ == "__main__":
    unittest.main()