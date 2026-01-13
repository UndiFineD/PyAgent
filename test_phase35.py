#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path

# Add the workspace root to sys.path
<<<<<<< HEAD:test_phase35.py
sys.path.append(str(Path(__file__).parent))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase35.py

from src.classes.fleet.FleetManager import FleetManager

def test_phase35() -> None:
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 35 Verification...")
    
    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)
    
    # 1. Test Swarm-to-Swarm Telepathy (Inter-Fleet Bridge)
    print("\n--- Testing Swarm-to-Swarm Telepathy ---")
    fleet.inter_fleet_bridge.connect_to_peer("fleet_beta", "http://192.168.1.50:8000")
    fleet.inter_fleet_bridge.broadcast_state("swarm_objective", "Scale neural bridge")
    
    # Simulate receiving state from peer
    fleet.inter_fleet_bridge.sync_external_state("fleet_beta", {"peer_capability": "extreme_compression"})
    
    discovery = fleet.inter_fleet_bridge.query_global_intelligence("peer_capability")
    print(f"✅ Discovered Intelligence: {discovery}")
    
    if discovery == "extreme_compression":
        print("✅ Swarm-to-Swarm Telepathy flow verified.")
    else:
        print("❌ Swarm-to-Swarm Telepathy flow failed.")

    # 2. Test Recursive Self-Archiving
    print("\n--- Testing Recursive Self-Archiving ---")
    # Identify targets
    targets = fleet.call_by_capability("SelfArchiving", threshold_days=30)
    print(f"✅ Archiving Targets: {targets}")
    
    if "session_old_001.log" in str(targets):
        print("✅ Self-Archiving identification verified.")
    else:
        print("❌ Self-Archiving identification failed.")

    print("\n🏁 Phase 35 Verification Complete.")

if __name__ == "__main__":
    test_phase35()
