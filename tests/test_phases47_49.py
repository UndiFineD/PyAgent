import unittest
import os
import json
from src.classes.fleet.FleetManager import FleetManager

class TestPhases47_49(unittest.TestCase):
    def setUp(self):
        self.workspace = os.path.abspath("c:/DEV/PyAgent")
        self.fleet = FleetManager(self.workspace)
        # Setup dirs
        os.makedirs(os.path.join(self.workspace, "agent_store/governance/proposals"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace, "deploy"), exist_ok=True)

    def test_governance_and_dao(self):
        print("\nTesting Phase 47: Governance & DAO...")
        # Submit proposal
        proposal_id = self.fleet.governance.submit_proposal(
            "Increase Budget", "Allow agents to use 20% more tokens.", "LinguisticAgent"
        )
        print(f"Proposal ID: {proposal_id}")
        self.assertIsNotNone(proposal_id)
        
        # Cast vote
        res = self.fleet.governance.cast_vote(proposal_id, "ReasoningAgent", "Approve", "Needed for complex tasks.")
        print(res)
        self.assertIn("Vote cast", res)
        
        # Close proposal
        result = self.fleet.governance.close_proposal(proposal_id)
        print(f"Result: {result['result']}")
        self.assertEqual(result['result']['winner'], "Approve")
        
        # DAO execution
        dao_res = self.fleet.agent_dao.execute_resource_allocation({"LinguisticAgent": 0.2, "ReasoningAgent": 0.8})
        print(dao_res)
        self.assertIn("allocation plan successfully applied", dao_res)

    def test_multi_modal_grounding(self):
        print("\nTesting Phase 48: Multi-Modal Action Grounding...")
        # Spatial reasoning
        objects = [{"id": "AgentA", "position": [1, 2, 0]}, {"id": "ToolB", "position": [5, 2, 0]}]
        spatial_res = self.fleet.visualizer.spatial_reasoning(objects, "Is AgentA close to ToolB?")
        print(f"Spatial reasoning res: {spatial_res}")
        self.assertIsNotNone(spatial_res)
        
        # Physics constraints
        physics_res = self.fleet.reality_anchor.check_physics_constraints(
            "Agent moves 1000m in 1ms", {"max_velocity": 343} # Speed of sound
        )
        print(f"Physics res: {physics_res}")
        # It's an AI tool so verdict depends on model, but we check key presence
        self.assertIn("feasible", physics_res)

    def test_self_replicating_fleet(self):
        print("\nTesting Phase 49: Self-Replicating Fleet Infrastructure...")
        # Dockerfile gen
        path = self.fleet.fleet_deployer.generate_dockerfile("SQLAgent")
        print(f"Dockerfile: {path}")
        self.assertTrue(os.path.exists(path))
        
        # Spawn node
        spawn_res = self.fleet.fleet_deployer.spawn_node("SQL_Node_01", "SQLAgent")
        print(spawn_res)
        self.assertIn("provisioning initialized", spawn_res)
        
        # Self healing
        healing_res = self.fleet.immune_system.trigger_self_healing("SQL_Node_01", "crash")
        print(healing_res)
        self.assertIn("Self-healing complete", healing_res)

if __name__ == "__main__":
    unittest.main()
