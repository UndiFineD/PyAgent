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
Test Phase38 module.
"""

#!/usr/bin/env python3

import logging
import os

# Add project root to path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
import asyncio


async def run_phase38():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    print("\n--- Testing Phase 38: Holographic State & Resource Prediction ---")

    # 1. Test Holographic Sharding
    test_state = {
        "goal": "Rebuild the universe",
        "progress": 0.42,
        "active_nodes": ["NodeA", "NodeB", "NodeC"],
    }

    # Shard into 3 parts
    # Assuming shard_state might be async or sync, check first (safety pattern)
    res = fleet.holographic_state.shard_state(
        "rebuild_universe_plan", test_state, redundant_factor=3
    )
    if asyncio.iscoroutine(res):
        await res
    print("HolographicState: Generated shards for 'rebuild_universe_plan'.")

    # Reconstruct
    res = fleet.holographic_state.reconstruct_state("rebuild_universe_plan")
    if asyncio.iscoroutine(res):
        reconstructed_str = await res
    else:
        reconstructed_str = res
    print(f"HolographicState: Reconstruction result: {reconstructed_str[:50]}...")

    # Note: HolographicState currently returns a string (serialized dict)
    assert reconstructed_str is not None, "Holographic state reconstruction failed!"

    # 2. Test Resource Prediction

    task = "Complex neural refactoring of the memory bus with high entropy data."
    res = fleet.resource_predictor.forecast_and_allocate(task)
    if asyncio.iscoroutine(res):
        prediction = await res
    else:
        prediction = res

    print(f"ResourcePredictor: Task: '{task[:40]}...'")
    print(
        f"ResourcePredictor: Complexity Forecast: {prediction['complexity_forecast']}"
    )
    print(f"ResourcePredictor: Allocation: {prediction['allocation']}")

    assert prediction["allocation"]["vram_mb"] > 512, "Resource allocation failed!"

    print("\n[SUCCESS] Phase 38 verification complete.")


def test_phase38() -> None:
    asyncio.run(run_phase38())


if __name__ == "__main__":
    test_phase38()