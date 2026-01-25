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
Test Phase22 module.
"""

import pytest
import asyncio
from pathlib import Path

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


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