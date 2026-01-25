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

"""Unit tests for OrchestratorRegistry and lazy loading resilience."""

#!/usr/bin/env python3
import logging
from pathlib import Path

# Add project root to sys.path

from src.infrastructure.swarm.fleet.orchestrator_registry import (
    LazyOrchestratorMap,
    OrchestratorRegistry,
)
from src.core.base.lifecycle.version import SDK_VERSION


class MockFleet:
    def __init__(self, root: Path) -> None:
        self.workspace_root: Path = root


def test_orchestrator_workflow() -> None:
    print(f"--- Testing Orchestrator Workflow (SDK {SDK_VERSION}) ---")
    workspace: Path = Path(".").resolve()
    fleet = MockFleet(workspace)

    # 1. Test Registry Gatekeeping
    orc_map: LazyOrchestratorMap = OrchestratorRegistry.get_orchestrator_map(fleet)

    print("Checking FutureOrchestrator (v3.0)...")
    is_in_manifest: bool = "FutureOrchestrator" in orc_map._manifest_configs

    print(f"FutureOrchestrator in manifest? {is_in_manifest} (Expect: False)")

    print("Checking LegacyOrchestrator (v1.0)...")
    is_in_manifest: bool = "LegacyOrchestrator" in orc_map._manifest_configs
    print(f"LegacyOrchestrator in manifest? {is_in_manifest} (Expect: True)")

    # 2. Test Self-Healing reload
    print("\n--- Testing Orchestrator Self-Healing Reload ---")
    orc_map._configs["HealTest"] = ("non.existent.module", "HealTestOrc", False, None)

    # Try to load it - should return a ResilientStub
    stub = getattr(orc_map, "HealTest")
    print(f"Initial load of HealTest: {type(stub).__name__}")

    # Simulate 'fixing' it by pointing to a real class (e.g. MemoryEngine)

    orc_map._configs["HealTest"] = (
        "src.logic.agents.cognitive.context.engines.memory_engine",
        "MemoryEngine",
        False,
        "",
    )

    # Trigger self-healing try_reload
    success: bool = orc_map.try_reload("HealTest")
    print(f"Reload successful? {success}")

    if success:
        new_instance = getattr(orc_map, "HealTest")
        print(f"New instance type: {type(new_instance).__name__}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    test_orchestrator_workflow()
