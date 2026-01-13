import sys
from pathlib import Path
<<<<<<< HEAD:test_phase25.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase25.py

from classes.fleet.FleetManager import FleetManager
import time

def test_phase25() -> None:
    print("--- Phase 25 Verification: Quantum Entanglement & Reality Anchoring ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Quantum Entanglement
    print("\n[1/2] Testing Quantum Entanglement (State Mirroring)...")
    fleet.entanglement.update_state("swarm_mode", "hyper_dynamic")
    
    # Simulate another component updating state via signal
    fleet.signal_bus.publish("entanglement_sync", {"key": "alert_level", "value": "critical"}, sender="RemoteNode")
    time.sleep(0.5)
    
    current_state = fleet.entanglement.get_all_state()
    if current_state.get("swarm_mode") == "hyper_dynamic" and current_state.get("alert_level") == "critical":
        print(f"✅ Entanglement confirmed: {current_state}")
    else:
        print(f"❌ Entanglement failed. State: {current_state}")

    # 2. Test Reality Anchor
    print("\n[2/2] Testing Reality Anchor (Claim Verification)...")
    claim = "The PyAgent framework supports distributed quantum state mirroring."
    sources = ["src/classes/orchestration/EntanglementOrchestrator.py"]
    
    verification = fleet.reality_anchor.verify_claim(claim, sources)
    
    if "verdict" in verification:
        print(f"✅ Reality Anchor verdict: {verification['verdict']} (Confidence: {verification.get('confidence')})")
        print(f"   Reasoning: {verification.get('reasoning')}")
    else:
        print("❌ Reality Anchor verification failed.")

if __name__ == "__main__":
    test_phase25()
