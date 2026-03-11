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
"""Test Phase37 module.
"""


import logging
import os
import sys
from pathlib import Path

from src.classes.fleet.FleetManager import FleetManager

# Add the workspace root to sys.path
sys.path.append(str(Path(__file__).parent))


def test_phase37() -> None:
    """Test function for Phase 37 features."""
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting Phase 37 Verification...")

    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    # 1. Test Swarm Telemetry Visualization
    print("\n--- Testing Swarm Telemetry Visualization ---")
    fleet.fleet_telemetry.log_signal_flow("TASK_ASSIGNED", "FleetManager", ["Reasoner", "Linguistic"])
    fleet.fleet_telemetry.log_signal_flow("ANALYSIS_COMPLETE", "Reasoner", ["FleetManager"])

    mermaid_flow = fleet.fleet_telemetry.generate_mermaid_flow()
    print(f"✅ Mermaid Flow Generated:\n{mermaid_flow}")

    bottlenecks = fleet.fleet_telemetry.identify_bottlenecks()
    print(f"✅ Identified Traffic Centers: {bottlenecks}")

    if "FleetManager" in mermaid_flow and "Reasoner" in bottlenecks:
        print("✅ Swarm Telemetry flow verified.")
    else:
        print("❌ Swarm Telemetry flow failed.")

    # 2. Test Morphological Code Generation
    print("\n--- Testing Morphological Code Generation ---")
    mock_logs = [{"params": ["input_text", "urgency"]} for _ in range(15)]
    evolution_report = fleet.call_by_capability("MorphologicalEvolution", agent_name="Linguistic", call_logs=mock_logs)

    print(f"✅ Evolution Report: {evolution_report}")

    if isinstance(evolution_report, dict) and evolution_report.get("morphological_proposals"):
        print("✅ Morphological Evolution flow verified.")
    else:
        print("❌ Morphological Evolution flow failed.")

    print("\n🏁 Phase 37 Verification Complete.")


if __name__ == "__main__":
    test_phase37()
