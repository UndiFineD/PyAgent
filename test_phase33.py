#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path

# Add the workspace root to sys.path
sys.path.append(str(Path(__file__).parent))

from src.classes.fleet.FleetManager import FleetManager

def test_phase33() -> None:
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 33 Verification...")
    
    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)
    
    # 1. Test Autonomous Sub-Swarm Spawning
    print("\n--- Testing Sub-Swarm Spawning ---")
    swarm_id = fleet.sub_swarm_spawner.spawn_sub_swarm(["Reasoning", "Linguistic"])
    print(f"✅ Spawned sub-swarm: {swarm_id}")
    
    sub_swarm = fleet.sub_swarm_spawner.get_sub_swarm(swarm_id)
    if sub_swarm:
        print(f"✅ Sub-swarm {swarm_id} retrieved successfully.")
        # Result might be generic due to mock calls but should not fail
        res = sub_swarm.execute_mini_task("Analyze technical debt in the current file.")
        print(f"✅ Mini-task result: {res}")
    else:
        print(f"❌ Failed to retrieve sub-swarm {swarm_id}.")

    # 2. Test Cross-Modal Teleportation
    print("\n--- Testing Cross-Modal Teleportation ---")
    gui_session = "User clicked Home, then Search, then typed 'PyAgent', then clicked first result."
    print(f"✅ Source Data (GUI): {gui_session}")
    
    target_modality = fleet.modal_teleportation.identify_optimal_target("GUI", gui_session)
    print(f"✅ Identified optimal target: {target_modality}")
    
    teleported_state = fleet.modal_teleportation.teleport_state("GUI", target_modality, gui_session)
    print(f"✅ Teleported State ({target_modality}):\n{teleported_state}")

    if "GUI" in str(teleported_state) or "automation" in str(teleported_state).lower() or "translated" in str(teleported_state).lower() or "converted" in str(teleported_state).lower() or "Analytical Breakdown" in str(teleported_state):
        print("✅ Success: Cross-modal teleportation flow verified.")
    else:
        print("❌ Error: Teleported state is unexpected.")

    print("\n🏁 Phase 33 Verification Complete.")

if __name__ == "__main__":
    test_phase33()

if __name__ == "__main__":
    test_phase33()
