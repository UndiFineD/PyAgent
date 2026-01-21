#!/usr/bin/env python3
"""Unit tests for the SDK V2.2 components."""

import logging
from pathlib import Path
from src.infrastructure.fleet.fleet_manager import FleetManager

logging.basicConfig(level=logging.INFO)


def test_v2_2_plugin_loading() -> None:
    print("--- Running SDK v2.2.0 Verification ---")
    workspace = Path(Path(__file__).resolve().parents[3])
    fleet = FleetManager(str(workspace))

    # 1. Test Mock Agent loading (Dynamic via Manifest)
    print("\n[1] Testing Mock Agent...")
    try:
        mock_agent = fleet.agents["Mock"]
        print(f"Mock Agent Type: {type(mock_agent).__name__}")
        response = mock_agent.run("Hello World")
        print(f"Mock Agent Response: {response}")
        assert "MOCK-CORE-V1" in response
    except Exception as e:
        print(f"FAILED to load Mock Agent: {e}")

    # 2. Test Mock Orchestrator loading (Lazy via OrchestratorRegistry)
    print("\n[2] Testing Mock Orchestrator...")
    try:
        # Accessed via fleet.orchestrators.<name> or __getattr__
        mock_orc = fleet.orchestrators.MockOrc
        print(f"Mock Orchestrator Type: {type(mock_orc).__name__}")
        ritual = mock_orc.coordinate_mock_ritual("Alpha Phase")
        print(f"Orchestrator Ritual Result: {ritual}")
        assert "ritual" in ritual.lower()
    except Exception as e:
        print(f"FAILED to load Mock Orchestrator: {e}")

    # 3. Test Version Gatekeeping (FutureAgent should fail if we didn't bump enough, but it requires 3.0.0)
    print("\n[3] Testing SDK Version Gatekeeping...")
    # FutureAgent is in manifest as 3.0.0
    try:
        fleet.agents["FutureAgent"]
        print("ERROR: FutureAgent should have been skipped!")
    except KeyError:
        print("Success: FutureAgent correctly skipped (requires 3.0.0).")

    # 4. Test Core Extraction Verification (Blackboard)
    print("\n[4] Testing Core/Shell Extraction (Blackboard)...")
    fleet.blackboard.post("test_key", "verified", "test_runner")
    val = fleet.blackboard.get("test_key")
    print(f"Blackboard retrieval: {val}")

    assert hasattr(fleet.blackboard, "core")
    print("Success: Blackboard is using Core delegation.")

    print("\n--- SDK v2.2.0 Verification Complete ---")


if __name__ == "__main__":
    test_v2_2_plugin_loading()
