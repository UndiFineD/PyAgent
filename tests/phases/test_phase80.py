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
Test Phase80 module.
"""

import unittest
import sys
from pathlib import Path

# Ensure src is in sys.path
root = Path(__file__).resolve().parents[2].parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase80(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_consensus_conflict_agent(self) -> None:
        print("\nTesting Phase 80: Multi-Agent Consensus & Conflict Resolution v2...")

        # 1. Initiate dispute
        dispute_id = "D-101"
        self.fleet.consensus_conflict.initiate_dispute(
            dispute_id,
            "Should we refactor the core backend?",
            ["Yes", "No", "Partially"],
        )

        # 2. Cast votes
        self.fleet.consensus_conflict.cast_vote(
            dispute_id, "AgentA", 0, "Current code is messy"
        )
        self.fleet.consensus_conflict.cast_vote(
            dispute_id, "AgentB", 0, "Better for long term maintainability"
        )

        self.fleet.consensus_conflict.cast_vote(
            dispute_id, "AgentC", 2, "Risky to do all at once"
        )

        # 3. Resolve dispute
        res = self.fleet.consensus_conflict.resolve_dispute(dispute_id)
        print(f"Resolution: {res}")

        self.assertEqual(res["winner"], "Yes")
        self.assertEqual(res["total_votes"], 3)
        self.assertEqual(res["vote_counts"][0], 2)

        # 4. Conflict summary

        summary = self.fleet.consensus_conflict.get_conflict_summary()
        print(f"Summary: {summary}")
        self.assertEqual(summary["total_disputes"], 1)
        self.assertEqual(summary["resolved_disputes"], 1)


if __name__ == "__main__":
    unittest.main()