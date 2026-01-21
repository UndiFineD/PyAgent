import unittest
from pathlib import Path
from src.infrastructure.fleet.fleet_manager import FleetManager


class TestPhases65_67(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_semantic_search_mesh(self) -> None:
        print("\nTesting Phase 65: Fleet-Wide Semantic Search Mesh...")
        # Register shard
        reg = self.fleet.search_mesh.register_shard(
            "shard-01", {"domain": "python_docs"}
        )
        print(f"Registration: {reg}")
        self.assertEqual(reg["shard_count"], 1)

        # Federated search
        results = self.fleet.search_mesh.federated_search([0.1, 0.2, 0.3])
        print(f"Search Results: {results}")
        self.assertTrue(len(results) > 0)

        # Sync
        sync = self.fleet.search_mesh.replicate_shard("shard-01", "node-B")
        print(f"Sync: {sync}")
        self.assertEqual(sync["status"], "synchronized")

    def test_policy_enforcement(self) -> None:
        print("\nTesting Phase 66: Autonomous Policy Enforcement...")
        # Evaluation ok
        ok_res = self.fleet.policy_enforcement.evaluate_action(
            "AgentA", "read_file", {"path": "test.txt"}
        )
        print(f"Evaluation OK: {ok_res}")
        self.assertEqual(ok_res["status"], "authorized")

        # Evaluation violation
        fail_res = self.fleet.policy_enforcement.evaluate_action(
            "AgentA", "external_push", {"content": "my credentials are secret"}
        )
        print(f"Evaluation FAIL: {fail_res}")
        self.assertEqual(fail_res["status"], "violation")

        # Quarantine
        q_res = self.fleet.policy_enforcement.quarantine_agent(
            "AgentA", "Security Violation"
        )
        print(f"Quarantine: {q_res}")
        self.assertTrue(self.fleet.policy_enforcement.is_agent_quarantined("AgentA"))

    def test_dynamic_model_routing(self) -> None:
        print("\nTesting Phase 67: Dynamic Model Routing...")
        # Routing

        p1 = self.fleet.model_router.determine_optimal_provider("high_reasoning")
        print(f"High Reasoning Provider: {p1}")
        self.assertEqual(p1, "glm_4_7")

        p2 = self.fleet.model_router.determine_optimal_provider("simple_task")

        print(f"Simple Task Provider: {p2}")
        self.assertEqual(p2, "local_llama")

        # Compression
        long_prompt = "A" * 2000

        compressed = self.fleet.model_router.compress_context(long_prompt)
        print(f"Compressed Length: {len(compressed)}")
        self.assertTrue(len(compressed) < len(long_prompt))
        self.assertIn("[OMITTED]", compressed)


if __name__ == "__main__":
    unittest.main()
