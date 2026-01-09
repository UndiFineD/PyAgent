import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from classes.fleet.FleetManager import FleetManager

def test_phase24():
    print("--- Phase 24 Verification: Swarm Immortality & Temporal Sharding ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Heartbeat
    print("\n[1/2] Testing Heartbeat Verification...")
    fleet.heartbeat.record_heartbeat("Reasoner")
    if "Reasoner" in fleet.heartbeat.last_seen:
        print("✅ Heartbeat recorded successfully.")
    else:
        print("❌ Heartbeat failed to record.")

    # 2. Test Temporal Sharding
    print("\n[2/2] Testing Temporal Sharding (Flashback)...")
    context = fleet.temporal_shard.retrieve_temporal_context("Verify agent logic")
    if "FLASHBACK" in context:
        print(f"✅ Temporal context retrieved: {context}")
    else:
        print("❌ Temporal sharding failed.")

if __name__ == "__main__":
    test_phase24()
