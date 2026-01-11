import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.logic.agents.swarm.SwarmDeploymentAgent import SwarmDeploymentAgent

class TestSwarmDeployment(unittest.TestCase):
    def setUp(self):
        self.agent = SwarmDeploymentAgent(os.getcwd())

    def test_provision(self):
        node = self.agent.provision_node("Compute", "us-west-2")
        self.assertEqual(node['node_type'], "Compute")
        self.assertEqual(node['region'], "us-west-2")
        self.assertIn("DEP-", node['deployment_id'])

    def test_scaling(self):
        new_nodes = self.agent.scale_swarm(3, "Storage")
        self.assertEqual(len(new_nodes), 3)
        inventory = self.agent.get_deployment_inventory()
        self.assertEqual(inventory['total_nodes'], 3)

if __name__ == "__main__":
    unittest.main()
