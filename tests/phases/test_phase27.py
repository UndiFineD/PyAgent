from pathlib import Path

from src.infrastructure.fleet.fleet_manager import FleetManager


def test_phase27() -> None:
    print("--- Phase 27 Verification: Fractal Orchestration & Swarm Singularity ---")
    workspace_root = Path(__file__).resolve().parents[2]
    fleet = FleetManager(str(workspace_root))

    # 1. Test Fractal Orchestration
    print("\n[1/2] Testing Fractal Orchestration (Recursive Decomposition)...")
    res = fleet.fractal_orchestrator.execute_fractal_task(
        "Handle a nested architectural overhaul."
    )

    if "Depth 1" in res:
        print(f"✅ Fractal orchestration confirmed: {res}")
    else:
        print(f"❌ Fractal orchestration failed: {res}")

    # 2. Test Architect Agent
    print("\n[2/2] Testing Architect Agent (Structural Evolution)...")
    pivot = fleet.architect.suggest_architectural_pivot(
        "Latency peaks at 200ms during shm sync."
    )

    if "component" in pivot:
        print(
            f"✅ Architectural pivot suggested: {pivot['proposed_change']} for {pivot['component']}"
        )
    else:
        print("❌ Architect agent failed to suggest pivot.")


if __name__ == "__main__":
    test_phase27()
