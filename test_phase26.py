import sys
from pathlib import Path
<<<<<<< HEAD:test_phase26.py
<<<<<<< HEAD:test_phase26.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase26.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase26.py

from classes.fleet.FleetManager import FleetManager

def test_phase26() -> None:
    print("--- Phase 26 Verification: Neural Symbiosis & Autonomous Infrastructure ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Cognitive Borrowing
    print("\n[1/2] Testing Cognitive Borrowing (Skill Transfer)...")
    fleet.cognitive_borrowing.establish_bridge("Linguistic", "Reasoner")
    skill_pattern = fleet.cognitive_borrowing.borrow_skill("Linguistic", "Complex logical deduction")
    
    if skill_pattern and "PATTERN" in skill_pattern:
        print(f"✅ Cognitive borrowing successful: {skill_pattern}")
    else:
        print("❌ Cognitive borrowing failed.")

    # 2. Test Resilience Manager
    print("\n[2/2] Testing Resilience Manager (Resource Optimization)...")
    optimization = fleet.resilience_manager.optimize_resource_allocation()
    
    if "rebalanced_agents" in optimization:
        print(f"✅ Resilience optimization confirmed: {optimization}")
    else:
        print("❌ Resilience optimization failed.")

if __name__ == "__main__":
    test_phase26()
