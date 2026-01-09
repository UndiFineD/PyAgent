import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.orchestration.MultiCloudBridgeOrchestrator import MultiCloudBridgeOrchestrator

class TestMultiCloudBridge(unittest.TestCase):
    def setUp(self):
        self.orchestrator = MultiCloudBridgeOrchestrator(None)

    def test_registration_and_sync(self):
        self.orchestrator.register_cloud_node("AWS-01", "AWS", "us-east-1")
        self.orchestrator.register_cloud_node("AZ-01", "Azure", "eastus")
        
        topology = self.orchestrator.get_bridge_topology()
        self.assertEqual(topology['total_nodes'], 2)
        
        sync = self.orchestrator.sync_state_cross_cloud({"data": 123}, "AWS")
        self.assertEqual(sync['nodes_synced'], 1) # Synced to Azure
        self.assertIn("Azure", sync['targets'])

    def test_routing(self):
        self.orchestrator.register_cloud_node("GCP-01", "GCP", "us-central1")
        success = self.orchestrator.route_message("Hello GCP", "GCP")
        self.assertTrue(success)
        
        fail = self.orchestrator.route_message("Hello AWS", "AWS")
        self.assertFalse(fail)

if __name__ == "__main__":
    unittest.main()
