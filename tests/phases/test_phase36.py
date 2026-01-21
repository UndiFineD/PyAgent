#!/usr/bin/env python3

import os
import logging

# Add the workspace root to sys.path

from src.infrastructure.fleet.fleet_manager import FleetManager
import asyncio


async def run_phase36():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 36 Verification...")

    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    # 1. Test Synthetic Emotional Regulation
    print("\n--- Testing Synthetic Emotional Regulation ---")
    fleet.emotional_regulation.set_vibe(urgency=0.9, patience=0.2)

    # Check if determines_execution_path is async
    res = fleet.emotional_regulation.determine_execution_path("Fix this bug now!")
    if asyncio.iscoroutine(res):
        path_fast = await res
    else:
        path_fast = res
    print(f"✅ Urgency 0.9 Path: {path_fast}")

    fleet.emotional_regulation.set_vibe(urgency=0.1, patience=0.9)
    res = fleet.emotional_regulation.determine_execution_path(
        "Research the implications of quantum tunneling in synapses."
    )
    if asyncio.iscoroutine(res):
        path_deep = await res
    else:
        path_deep = res
    print(f"✅ Patience 0.9 Path: {path_deep}")

    if path_fast == "FAST_PATH" and path_deep == "DEEP_REASONING_PATH":
        print("✅ Emotional Regulation flow verified.")
    else:
        print("❌ Emotional Regulation flow failed.")

    # 2. Test Neuro-Symbolic Reasoning
    print("\n--- Testing Neuro-Symbolic Reasoning ---")
    # Test valid content
    valid_code = "def add(a: int, b: int) -> int: return a + b"
    res_valid = await fleet.call_by_capability("NeuroSymbolic", content=valid_code)

    print(
        f"✅ Valid Content Result (Passed={res_valid.get('content_verified')}): {res_valid.get('violations')}"
    )

    # Test violation (No plain passwords)

    invalid_password = "password = 'secret123'"

    res_invalid_pwd = await fleet.call_by_capability(
        "NeuroSymbolic", content=invalid_password
    )
    print(
        f"✅ Invalid Password Result (Passed={res_invalid_pwd.get('content_verified')}): {res_invalid_pwd.get('violations')}"
    )

    # Test violation (Deletions)
    invalid_del = "rm -rf /"

    res_invalid_del = await fleet.call_by_capability(
        "NeuroSymbolic", content=invalid_del
    )
    print(
        f"✅ Invalid Deletion Result (Passed={res_invalid_del.get('content_verified')}): {res_invalid_del.get('violations')}"
    )

    if (
        res_valid.get("content_verified")
        and not res_invalid_pwd.get("content_verified")
        and not res_invalid_del.get("content_verified")
    ):
        print("✅ Neuro-Symbolic Reasoning flow verified.")

    else:
        print("❌ Neuro-Symbolic Reasoning flow failed.")

    print("\n🏁 Phase 36 Verification Complete.")


def test_phase36() -> None:
    asyncio.run(run_phase36())


if __name__ == "__main__":
    test_phase36()
