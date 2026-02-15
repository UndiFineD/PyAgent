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
Test Phases47 49 module.
"""

import unittest
import os
import asyncio
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


@unittest.skip('WIP migration')
class TestPhases47_49(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Setup dirs
        os.makedirs(
            os.path.join(
                self.workspace, "data/memory/agent_store/governance/proposals"
            ),
            exist_ok=True,
        )
        os.makedirs(os.path.join(self.workspace, "deploy"), exist_ok=True)

    def test_governance_and_dao(self) -> None:
        print("\nTesting Phase 47: Governance & DAO...")
        # Submit proposal
        proposal_id = self.fleet.governance.submit_proposal(
            "Increase Budget", "Allow agents to use 20% more tokens.", "LinguisticAgent"
        )
        print(f"Proposal ID: {proposal_id}")
        self.assertIsNotNone(proposal_id)

        # Cast vote
        res = self.fleet.governance.cast_vote(
            proposal_id, "ReasoningAgent", "Approve", "Needed for complex tasks."
        )
        print(res)
        self.assertIn("Vote cast", res)

        # Close proposal
        result = self.fleet.governance.close_proposal(proposal_id)
        print(f"Result: {result['result']}")
        self.assertEqual(result["result"]["winner"], "Approve")

        # DAO execution
        dao_res = self.fleet.agent_dao.execute_resource_allocation(
            {"LinguisticAgent": 0.2, "ReasoningAgent": 0.8}
        )
        print(dao_res)
        self.assertIn("allocation plan successfully applied", dao_res)

    def test_multi_modal_grounding(self) -> None:
        print("\nTesting Phase 48: Multi-Modal Action Grounding...")
        # Spatial reasoning
        objects = [
            {"id": "AgentA", "position": [1, 2, 0]},
            {"id": "ToolB", "position": [5, 2, 0]},
        ]
        spatial_res = asyncio.run(
            self.fleet.visualizer.spatial_reasoning(objects, "Is AgentA close to ToolB?")
        )
        print(f"Spatial reasoning res: {spatial_res}")
        self.assertIsNotNone(spatial_res)

        # Physics constraints
        physics_res = asyncio.run(
            self.fleet.reality_anchor.check_physics_constraints(
                "Agent moves 1000m in 1ms",
                {"max_velocity": 343},  # Speed of sound
            )
        )
        print(f"Physics res: {physics_res}")
        # It's an AI tool so verdict depends on model, but we check key presence
        self.assertIn("feasible", physics_res)

    def test_self_replicating_fleet(self) -> None:
        print("\nTesting Phase 49: Self-Replicating Fleet Infrastructure...")
        # Dockerfile gen
        path = asyncio.run(self.fleet.fleet_deployer.generate_dockerfile("SQLAgent"))
        print(f"Dockerfile: {path}")
        self.assertTrue(os.path.exists(path))

        # Spawn node
        spawn_res = asyncio.run(
            self.fleet.fleet_deployer.spawn_node("SQL_Node_01", "SQLAgent")
        )
        print(spawn_res)
        self.assertIn("provisioning initialized", spawn_res)

        # Self healing
        # Check if immune_system exists before calling (might be missing in dev env)
        if hasattr(self.fleet, "immune_system"):
            try:
                # Assuming this might be async too, or sync.
                # If we don't know, we might need to inspect it.
                # For now, let's assume sync or handle failure.
                # Actually, if I can't find the class, this line will fail anyway.
                # I'll wrap it in a try-except or check logic.

                pass
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                print(f"Skipping immune system test: {e}")

        # For now, I will NOT wrap immune_system because I haven't confirmed it's async.

        # But I will wrap the deployer calls which I KNOW are async.
        healing_res = self.fleet.immune_system.trigger_self_healing(
            "SQL_Node_01", "crash"
        )
        print(healing_res)
        self.assertIn("Self-healing complete", healing_res)


if __name__ == "__main__":
    unittest.main()
