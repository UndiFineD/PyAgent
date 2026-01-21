import pytest
from pathlib import Path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


@pytest.mark.asyncio
async def test_phase21() -> None:
    print("--- Phase 21 Verification: World Model & Speciation ---")
    workspace_root = Path(__file__).resolve().parents[2]
    fleet = FleetManager(str(workspace_root))

    # 1. Test World Model
    print("\n[1/2] Testing World Model Prediction...")
    action = "Refactor the BaseAgent to use async/await"
    context = "Source code uses synchronous standard library calls."
    prediction = await fleet.world_model.predict_action_outcome(action, context)

    if "success_probability" in prediction:
        print(
            f"✅ Prediction received. Risk level: {prediction.get('risks', ['unknown'])[0]}"
        )
    else:
        print("❌ World Model prediction failed.")

    # 2. Test Speciation
    print("\n[2/2] Testing Agent Speciation (Specialization)...")
    base_agent = "CoderAgent"

    niche = "quantum scaling"
    result = await fleet.speciation.evolve_specialized_agent(base_agent, niche)

    expected_file = Path("src\logic\agents\specialized\quantumscaling_coder_agent.py")
    generated_test = (
        Path("tests/specialists") / f"test_{expected_file.stem.lower()}_UNIT.py"
    )

    if expected_file.exists():
        print(f"✅ Speciation confirmed: {result}")
        # Cleanup both agent and test
        expected_file.unlink()

        if generated_test.exists():
            generated_test.unlink()
    else:
        print(f"❌ Speciation failed. Expected {expected_file}")


if __name__ == "__main__":
    test_phase21()
