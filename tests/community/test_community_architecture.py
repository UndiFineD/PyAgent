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
Test Community Architecture module.
"""

#!/usr/bin/env python3
import logging
from pathlib import Path

# Add project root to sys.path

from src.infrastructure.swarm.fleet.agent_registry import AgentRegistry
from src.core.base.lifecycle.version import SDK_VERSION


def test_community_loading_workflow() -> None:
    """Test the complete workflow for loading community plugins."""
    print(f"--- Testing Community Plugin Workflow (SDK {SDK_VERSION}) ---")
    workspace = Path(".").resolve()

    # 1. Test Registry Gatekeeping
    agents = AgentRegistry.get_agent_map(workspace)

    print("Checking FutureAgent (v3.0)...")
    # pylint: disable=protected-access
    is_in_manifest = "FutureAgent" in agents._manifest_configs
    print(f"FutureAgent in manifest? {is_in_manifest} (Expect: False)")

    # 2. Test Self-Healing reload

    print("\n--- Testing Self-Healing Reload ---")
    # Simulate a failed agent
    agents.registry_configs["HealTest"] = ("non.existent.module", "HealTestAgent", None)

    # Try to load it - should return a ResilientStub
    stub = agents["HealTest"]
    print(f"Initial load of HealTest: {type(stub).__name__}")

    # Simulate 'fixing' it

    agents.registry_configs["HealTest"] = (
        "src.logic.agents.development.coder_agent",
        "CoderAgent",
        "src/coder/agents/CoderAgent.py",
    )

    # Trigger self-healing try_reload
    success = agents.try_reload("HealTest")
    print(f"Reload successful? {success}")

    if success:
        new_instance = agents["HealTest"]
        print(f"New instance type: {type(new_instance).__name__}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    test_community_loading_workflow()

    test_community_loading_workflow()