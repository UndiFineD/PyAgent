import sys
from pathlib import Path
<<<<<<< HEAD:test_phase21.py
<<<<<<< HEAD:test_phase21.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase21.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase21.py

from classes.fleet.FleetManager import FleetManager

def test_phase21() -> None:
    print("--- Phase 21 Verification: World Model & Speciation ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test World Model
    print("\n[1/2] Testing World Model Prediction...")
    action = "Refactor the BaseAgent to use async/await"
    context = "Source code uses synchronous standard library calls."
    prediction = fleet.world_model.predict_action_outcome(action, context)
    
    if "success_probability" in prediction:
        print(f"✅ Prediction received. Risk level: {prediction.get('risks', ['unknown'])[0]}")
    else:
        print("❌ World Model prediction failed.")

    # 2. Test Speciation
    print("\n[2/2] Testing Agent Speciation (Specialization)...")
    base_agent = "CoderAgent"
    niche = "asyncio threading"
    result = fleet.speciation.evolve_specialized_agent(base_agent, niche)
    
    expected_file = Path("src/classes/specialized/asynciothreadingCoderAgent.py")
    if expected_file.exists():
        print(f"✅ Speciation confirmed: {result}")
        # Cleanup
        expected_file.unlink()
    else:
        print(f"❌ Speciation failed. Expected {expected_file}")

if __name__ == "__main__":
    test_phase21()
