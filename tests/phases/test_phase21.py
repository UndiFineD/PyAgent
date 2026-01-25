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
Test Phase21 module.
"""

from pathlib import Path
import pytest

from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


@pytest.mark.asyncio
async def test_phase21() -> None:
    """Verify World Model and Speciation functionality."""
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

    expected_file = Path("src/logic/agents/specialized/quantum_scaling_coder_agent.py")
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
