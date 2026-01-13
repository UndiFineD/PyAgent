#!/usr/bin/env python3

import logging
import os
import sys
from pathlib import Path

# Add project root to path
<<<<<<< HEAD:test_phase38.py
sys.path.append(str(Path(__file__).parent))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase38.py

from src.classes.fleet.FleetManager import FleetManager

def test_phase38() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)
    
    print("\n--- Testing Phase 38: Holographic State & Resource Prediction ---")
    
    # 1. Test Holographic Sharding
    test_state = {
        "goal": "Rebuild the universe",
        "progress": 0.42,
        "active_nodes": ["NodeA", "NodeB", "NodeC"]
    }
    
    # Shard into 3 parts
    fleet.holographic_state.shard_state("rebuild_universe_plan", test_state, redundant_factor=3)
    print(f"HolographicState: Generated shards for 'rebuild_universe_plan'.")
    
    # Reconstruct
    reconstructed_str = fleet.holographic_state.reconstruct_state("rebuild_universe_plan")
    print(f"HolographicState: Reconstruction result: {reconstructed_str[:50]}...")
    
    # Note: HolographicState currently returns a string (serialized dict)
    assert reconstructed_str is not None, "Holographic state reconstruction failed!"
    
    # 2. Test Resource Prediction
    task = "Complex neural refactoring of the memory bus with high entropy data."
    prediction = fleet.resource_predictor.forecast_and_allocate(task)
    
    print(f"ResourcePredictor: Task: '{task[:40]}...'")
    print(f"ResourcePredictor: Complexity Forecast: {prediction['complexity_forecast']}")
    print(f"ResourcePredictor: Allocation: {prediction['allocation']}")
    
    assert prediction['allocation']['vram_mb'] > 512, "Resource allocation failed!"
    
    print("\n[SUCCESS] Phase 38 verification complete.")

if __name__ == "__main__":
    test_phase38()
