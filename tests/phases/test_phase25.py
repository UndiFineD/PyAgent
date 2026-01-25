#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test Phase25 module.
"""

import pytest
import asyncio
from pathlib import Path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
import time


@pytest.mark.asyncio
async def test_phase25() -> None:
    print("--- Phase 25 Verification: Quantum Entanglement & Reality Anchoring ---")
    workspace_root = Path(__file__).resolve().parents[2]
    fleet = FleetManager(str(workspace_root))

    # 1. Test Quantum Entanglement
    print("\n[1/2] Testing Quantum Entanglement (State Mirroring)...")
    fleet.entanglement.update_state("swarm_mode", "hyper_dynamic")

    # Simulate another component updating state via signal
    fleet.signal_bus.publish(
        "entanglement_sync",
        {"key": "alert_level", "value": "critical"},
        sender="RemoteNode",
    )
    await asyncio.sleep(0.5)

    current_state = fleet.entanglement.get_all_state()
    if (
        current_state.get("swarm_mode") == "hyper_dynamic"
        and current_state.get("alert_level") == "critical"
    ):
        print(f"✅ Entanglement confirmed: {current_state}")
    else:
        print(f"❌ Entanglement failed. State: {current_state}")

    # 2. Test Reality Anchor
    print("\n[2/2] Testing Reality Anchor (Claim Verification)...")
    claim = "The PyAgent framework supports distributed quantum state mirroring."

    sources = ["src\orchestration\EntanglementOrchestrator.py"]

    verification = await fleet.reality_anchor.verify_claim(claim, sources)

    if "verdict" in verification:
        print(
            f"✅ Reality Anchor verdict: {verification['verdict']} (Confidence: {verification.get('confidence')})"
        )
        print(f"   Reasoning: {verification.get('reasoning')}")
    else:
        print("❌ Reality Anchor verification failed.")


if __name__ == "__main__":
    test_phase25()