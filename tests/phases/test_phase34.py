#!/usr/bin/env python3

import os
import time
import logging
import asyncio

# Add the workspace root to sys.path

from src.infrastructure.fleet.FleetManager import FleetManager




async def run_phase34():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 34 Verification...")

    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    # 1. Test Temporal Sync
    print("\n--- Testing Bio-Temporal Synchronization ---")
    fleet.temporal_sync.report_activity()
    metabolism = fleet.temporal_sync.get_current_metabolism()
    print(f"✅ Initial Metabolism: {metabolism:.2f}")

    # Manually adjust for testing
    fleet.temporal_sync.last_activity_time -= 400
    metabolism_idle = fleet.temporal_sync.get_current_metabolism()
    print(f"✅ Idle Metabolism (400s): {metabolism_idle:.2f}")

    fleet.temporal_sync.set_sprint_mode(True)
    metabolism_sprint = fleet.temporal_sync.get_current_metabolism()
    print(f"✅ Sprint Metabolism: {metabolism_sprint:.2f}")

    # Test sync_wait (should be fast in sprint mode)
    start = time.time()
    fleet.temporal_sync.sync_wait(0.01)
    end = time.time()
    print(f"✅ Sync Wait actual: {end-start:.4f}s")






    # 2. Test Reality Grafting
    print("\n--- Testing Reality Grafting ---")
    # Simulate a dream result










    dream_intelligence = "Synthesized logic for high-performance multi-vector indexing discovered during simulation."




    # Use call_by_capability to test the whole path
    res = fleet.call_by_capability("RealityGrafting", focus_area="Search Logic", dream_output=dream_intelligence)
    if asyncio.iscoroutine(res):


        graft_result = await res
    else:



        graft_result = res
    print(f"✅ Graft Result: {graft_result}")

    if "Reality Grafting Report" in graft_result:
        print("✅ Reality Grafting flow verified.")

    else:
        print("❌ Reality Grafting flow failed.")




    print("\n🏁 Phase 34 Verification Complete.")





def test_phase34() -> None:
    asyncio.run(run_phase34())





if __name__ == "__main__":
    test_phase34()
