import unittest
import os
from pathlib import Path
from src.infrastructure.fleet.fleet_manager import FleetManager


class TestPhase43(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Ensure directories exist
        os.makedirs(
            os.path.join(self.workspace, "data/memory/agent_store/features"),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(self.workspace, "data/memory/knowledge_exports"), exist_ok=True
        )

    def test_feature_store(self) -> None:
        print("\nTesting Feature Store...")
        res = self.fleet.feature_store.register_feature(
            "dist_training_config",
            {"nodes": 8, "gpu": "H100", "strategy": "FSDP"},
            {"version": "1.0", "author": "damien-mlops"},
        )
        print(f"Result: {res}")
        self.assertIn("successfully registered", res)

        val = self.fleet.feature_store.get_feature("dist_training_config")
        self.assertEqual(val["strategy"], "FSDP")

    def test_experiment_orchestration(self) -> None:
        print("\nTesting Experiment Orchestration...")
        res = self.fleet.experiment_orchestrator.run_benchmark_experiment(
            "Phase-43-Suite", ["LinguisticAgent", "ReasoningAgent"]
        )

        print(f"Result: {res}")
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(len(res["agents"]), 2)

    def test_resource_curation(self) -> None:
        print("\nTesting Resource Curation...")
        res = self.fleet.resource_curator.add_resource(
            "https://example.com/fsdp-paper",
            "FSDP: Distributed Training at Scale",
            "Paper on Fully Sharded Data Parallelism implementation",
            ["MLOps", "Distributed", "Infrastructure"],
        )
        print(f"Result: {res}")
        self.assertIn("added to the Research Library", res)


if __name__ == "__main__":
    unittest.main()
