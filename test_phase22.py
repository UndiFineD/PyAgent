import sys
from pathlib import Path
<<<<<<< HEAD:test_phase22.py
<<<<<<< HEAD:test_phase22.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase22.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase22.py

from classes.fleet.FleetManager import FleetManager

def test_phase22() -> None:
    print("--- Phase 22 Verification: Federated Sovereignty & Recursive World Modeling ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Sovereignty Orchestrator
    print("\n[1/2] Testing Federated Sovereignty Negotiation...")
    proposal_id = fleet.sovereignty_orchestrator.propose_federated_task(
        "Joint research on quantum linguistics",
        ["Swarm-Delta", "Swarm-Epsilon"]
    )
    
    fleet.sovereignty_orchestrator.negotiate_privacy_boundaries(
        proposal_id, "Swarm-Delta", ["No raw IP leakage", "Anonymized results"]
    )
    
    agreement = fleet.sovereignty_orchestrator.finalize_federated_agreement(proposal_id)
    
    if agreement["agreement_status"] == "signed":
        print(f"✅ Federated agreement signed for proposal {proposal_id}")
    else:
        print("❌ Federated negotiation failed.")

    # 2. Test Recursive World Modeling
    print("\n[2/2] Testing Recursive World Modeling (Interaction Simulation)...")
    interaction = fleet.world_model.simulate_agent_interaction(
        "Reasoner", "Reflector", "Implement a thread-safe signal registry"
    )
    
    if "convergence_probability" in interaction:
        print(f"✅ Interaction simulated. Success probability: {interaction['convergence_probability']}")
        print(f"   Division of labor: {interaction['division_of_labor']}")
    else:
        print("❌ Recursive World Modeling simulation failed.")

if __name__ == "__main__":
    test_phase22()
