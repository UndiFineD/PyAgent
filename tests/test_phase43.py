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
Test Phase43 module.
"""

import unittest
import os
import shutil
from src.classes.fleet.FleetManager import FleetManager

class TestPhase43(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Ensure directories exist
        os.makedirs(os.path.join(self.workspace, "agent_store/features"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace, "knowledge_exports"), exist_ok=True)

    def test_feature_store(self) -> None:
        print("\nTesting Feature Store...")
        res = self.fleet.feature_store.register_feature(
            "dist_training_config", 
            {"nodes": 8, "gpu": "H100", "strategy": "FSDP"},
            {"version": "1.0", "author": "damien-mlops"}
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
            ["MLOps", "Distributed", "Infrastructure"]
        )
        print(f"Result: {res}")
        self.assertIn("added to the Research Library", res)

if __name__ == "__main__":
    unittest.main()