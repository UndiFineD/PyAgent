import unittest
import sys
from pathlib import Path

# Ensure src is in sys.path
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from src.classes.fleet.FleetManager import FleetManager

class TestPhase80(unittest.TestCase):
    def setUp(self):
        self.workspace = "c:/DEV/PyAgent"
        self.fleet = FleetManager(self.workspace)

    def test_consensus_conflict_agent(self) -> None:
        print("\nTesting Phase 80: Multi-Agent Consensus & Conflict Resolution v2...")
        
        # 1. Initiate dispute
        dispute_id = "D-101"
        self.fleet.consensus_conflict.initiate_dispute(
            dispute_id, 
            "Should we refactor the core backend?", 
            ["Yes", "No", "Partially"]
        )
        
        # 2. Cast votes
        self.fleet.consensus_conflict.cast_vote(dispute_id, "AgentA", 0, "Current code is messy")
        self.fleet.consensus_conflict.cast_vote(dispute_id, "AgentB", 0, "Better for long term maintainability")
        self.fleet.consensus_conflict.cast_vote(dispute_id, "AgentC", 2, "Risky to do all at once")
        
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
