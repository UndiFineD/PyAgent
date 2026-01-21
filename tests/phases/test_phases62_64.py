import unittest
import json
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhases62_64(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_resource_arbitration(self) -> None:
        print("\nTesting Phase 62: Autonomous Resource Arbitrator...")
        # Submit high bid
        res_high = self.fleet.resource_arbitrator.submit_bid(
            "CoderAgent", "GPU", 1, 100
        )
        print(f"High Bid: {res_high}")
        self.assertEqual(res_high["status"], "allocated")

        # Submit low bid
        res_low = self.fleet.resource_arbitrator.submit_bid(
            "DraftAgent", "CPU", 0.5, 10
        )
        print(f"Low Bid: {res_low}")
        self.assertEqual(res_low["status"], "queued")

        # Check report
        report = self.fleet.resource_arbitrator.get_resource_usage_report()
        print(f"Resource Report: {report}")
        self.assertEqual(report["allocation_count"], 1)

        # Preempt
        preempt = self.fleet.resource_arbitrator.preempt_low_priority_task(min_bid=150)
        print(f"Preemption: {preempt}")
        self.assertEqual(preempt["count"], 1)

    def test_agent_did_identity(self) -> None:
        print("\nTesting Phase 63: Cross-Chain Agent Identity (DID)...")
        # Create DID
        did = self.fleet.agent_identity.create_agent_did("SecurityAgent", "fleet-beta")
        print(f"Agent DID: {did}")
        self.assertTrue(did.startswith("did:pyagent:fleet-beta:"))

        # Issue VC
        issuer_did = "did:pyagent:fleet-01:root-authority"
        vc = self.fleet.agent_identity.issue_verifiable_credential(
            issuer_did, did, "FleetAccessClaim", "Level_4"
        )
        print(f"Verifiable Credential: {json.dumps(vc, indent=2)}")
        self.assertEqual(vc["credentialSubject"]["FleetAccessClaim"], "Level_4")

        # Verify VC
        verification = self.fleet.agent_identity.verify_credential(vc)
        print(f"Verification: {verification}")
        self.assertEqual(verification["status"], "verified")

    def test_neural_memory_pruning(self) -> None:
        print("\nTesting Phase 64: Neural Memory Pruning...")
        memories = [
            {
                "id": "mem_01",
                "content": "Critical error fixed in main.py",
                "timestamp": 100,
                "access_count": 50,
            },  # Strong
            {
                "id": "mem_02",
                "content": "Hello world test",
                "timestamp": 0,
                "access_count": 0,
            },  # Stale
            {
                "id": "mem_03",
                "content": "Drafting notes for readme",
                "timestamp": 1000,
                "access_count": 2,
            },  # Weak
        ]

        # Ranking

        for m in memories:
            rank = self.fleet.memory_pruning.rank_memory_importance(m)
            print(f"ID: {m['id']}, Rank: {rank}")

        # Plan

        plan = self.fleet.memory_pruning.generate_archival_plan(memories)
        print(f"Archival Plan: {plan}")
        self.assertIn("mem_02", plan["delete"])
        self.assertIn("mem_03", plan["cold_storage"])


if __name__ == "__main__":
    unittest.main()
