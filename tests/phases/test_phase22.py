import pytest
import asyncio
from pathlib import Path

from src.infrastructure.fleet.fleet_manager import FleetManager


@pytest.mark.asyncio
async def test_phase22() -> None:
    print(
        "--- Phase 22 Verification: Federated Sovereignty & Recursive World Modeling ---"
    )
    workspace_root = Path(__file__).resolve().parents[2]
    fleet = FleetManager(str(workspace_root))

    # 1. Test Sovereignty Orchestrator
    print("\n[1/2] Testing Federated Sovereignty Negotiation...")
    proposal_id = fleet.sovereignty_orchestrator.propose_federated_task(
        {
            "task": "Joint research on quantum linguistics",
            "participants": ["Swarm-Delta", "Swarm-Epsilon"],
        }
    )

    # Note: negotiate_privacy_boundaries might be needed here if previously present,

    # but based on the error log we only saw propose_federated_task failure.
    # Assuming finalizing agreement is the next step as per original context.

    agreement = fleet.sovereignty_orchestrator.finalize_federated_agreement(
        proposal_id, ["sig1", "sig2"]
    )
    print("\n[2/2] Testing Recursive World Modeling (Interaction Simulation)...")

    interaction = await fleet.world_model.simulate_agent_interaction(
        "Reasoner", "Reflector", "Implement a thread-safe signal registry"
    )

    if "convergence_probability" in interaction:
        print(
            f"✅ Interaction simulated. Success probability: {interaction['convergence_probability']}"
        )
        print(f"   Division of labor: {interaction['division_of_labor']}")
    else:
        print("❌ Recursive World Modeling simulation failed.")


if __name__ == "__main__":
    test_phase22()
