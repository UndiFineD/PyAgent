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
Test Phase35 module.
"""

#!/usr/bin/env python3

import os
import logging

# Add the workspace root to sys.path

import pytest
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


@pytest.mark.asyncio
async def test_phase35() -> None:
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 35 Verification...")

    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    # 1. Test Swarm-to-Swarm Telepathy (Inter-Fleet Bridge)
    print("\n--- Testing Swarm-to-Swarm Telepathy ---")
    fleet.inter_fleet_bridge.connect_to_peer("fleet_beta", "http://192.168.1.50:8000")
    fleet.inter_fleet_bridge.broadcast_state("swarm_objective", "Scale neural bridge")

    # Simulate receiving state from peer
    fleet.inter_fleet_bridge.sync_external_state(
        "fleet_beta", {"peer_capability": "extreme_compression"}
    )

    discovery = fleet.inter_fleet_bridge.query_global_intelligence("peer_capability")
    print(f"✅ Discovered Intelligence: {discovery}")

    if discovery == "extreme_compression":
        print("✅ Swarm-to-Swarm Telepathy flow verified.")
    else:
        print("❌ Swarm-to-Swarm Telepathy flow failed.")

    # 2. Test Recursive Self-Archiving
    print("\n--- Testing Recursive Self-Archiving ---")
    # Identify targets
    targets = await fleet.call_by_capability("SelfArchiving", threshold_days=30)
    print(f"✅ Archiving Targets: {targets}")

    if "session_old_001.log" in str(targets):
        print("✅ Self-Archiving identification verified.")
    else:
        print("❌ Self-Archiving identification failed.")

    print("\n🏁 Phase 35 Verification Complete.")


if __name__ == "__main__":
    test_phase35()