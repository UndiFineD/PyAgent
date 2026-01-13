import unittest
import os
import sys
from pathlib import Path

# Ensure src is in sys.path
root = Path(__file__).resolve().parents[2].parent
if str(root) not in sys.path:

from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhase78(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_inter_fleet_identity(self) -> None:
        print("\nTesting Phase 78: Federated Identity & Inter-Fleet Bridge v2...")
        
        # 1. Generate handshake
        handshake = self.fleet.inter_fleet_identity.generate_fleet_handshake()
        print(f"Handshake: {handshake}")
        self.assertIn("fleet_id", handshake)
        
        # 2. Register remote fleet
        remote_fleet_id = "fleet-xyz-123"
        reg_res = self.fleet.inter_fleet_identity.register_remote_fleet(remote_fleet_id, {"url": "https://fleet-xyz.com"})
        print(f"Registration: {reg_res}")
        self.assertEqual(reg_res["status"], "registered")
        
        # 3. Authorize remote agent
        agent_id = "RemoteAgent-001"
        auth_res = self.fleet.inter_fleet_identity.authorize_remote_agent(agent_id, remote_fleet_id, ["read_core", "sync_state"])
        print(f"Authorization: {auth_res}")
        self.assertEqual(auth_res["status"], "authorized")
        self.assertIn("session_token", auth_res)
        
        # 4. Verify token
        token = auth_res["session_token"]
        is_valid = self.fleet.inter_fleet_identity.verify_token(token)
        print(f"Token verification: {is_valid}")
        self.assertTrue(is_valid)
        
        # 5. Identity Report
        report = self.fleet.inter_fleet_identity.get_identity_report()
        print(f"Identity Report: {report}")
        self.assertEqual(report["remote_fleets_count"], 1)
        self.assertEqual(report["active_sessions_count"], 1)

if __name__ == "__main__":
    unittest.main()
