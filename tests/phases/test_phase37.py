#!/usr/bin/env python3

import os
import logging

# Add the workspace root to sys.path

from src.infrastructure.fleet.fleet_manager import FleetManager
import asyncio


async def run_phase37():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 37 Verification...")

    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    # 1. Test Swarm Telemetry Visualization
    print("\n--- Testing Swarm Telemetry Visualization ---")
    fleet.fleet_telemetry.log_signal_flow(
        "TASK_ASSIGNED", "FleetManager", ["Reasoner", "Linguistic"]
    )
    fleet.fleet_telemetry.log_signal_flow(
        "ANALYSIS_COMPLETE", "Reasoner", ["FleetManager"]
    )

    # Check if generate_mermaid_flow is async
    res = fleet.fleet_telemetry.generate_mermaid_flow()
    if asyncio.iscoroutine(res):
        mermaid_flow = await res
    else:
        mermaid_flow = res
    print(f"✅ Mermaid Flow Generated:\n{mermaid_flow}")

    res = fleet.fleet_telemetry.identify_bottlenecks()
    if asyncio.iscoroutine(res):
        bottlenecks = await res
    else:
        bottlenecks = res
    print(f"✅ Identified Traffic Centers: {bottlenecks}")

    if "FleetManager" in mermaid_flow and "Reasoner" in bottlenecks:
        print("✅ Swarm Telemetry flow verified.")
    else:
        print("❌ Swarm Telemetry flow failed.")

    # 2. Test Morphological Code Generation
    print("\n--- Testing Morphological Code Generation ---")

    mock_logs = [{"params": ["input_text", "urgency"]} for _ in range(15)]
    evolution_report = await fleet.call_by_capability(
        "MorphologicalEvolution", agent_name="Linguistic", call_logs=mock_logs
    )

    print(f"✅ Evolution Report: {evolution_report}")

    if evolution_report.get("morphological_proposals"):
        print("✅ Morphological Evolution flow verified.")

    else:
        print("❌ Morphological Evolution flow failed.")

    print("\n🏁 Phase 37 Verification Complete.")


def test_phase37() -> None:
    asyncio.run(run_phase37())


if __name__ == "__main__":
    test_phase37()
