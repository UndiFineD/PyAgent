#!/usr/bin/env python3
"""
Module: check_registry
Provides registry and validation for PyAgent tools.
"""
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

import logging
import os
import sys
import traceback
from pathlib import Path

# Ensure src is on path
sys.path.append(os.getcwd())

from src.infrastructure.swarm.fleet.agent_registry import (  # noqa: E402
    LazyAgentMap,
)  # pylint: disable=wrong-import-position
from src.infrastructure.swarm.fleet.orchestrator_registry import \
    LazyOrchestratorMap  # noqa: E402  # pylint: disable=wrong-import-position


def run_diagnostic() -> None:
    """Run diagnostic checks on PyAgent registries."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    root = Path(os.getcwd())

    print("=== PyAgent Registry Diagnostic ===")

    # Check Agents
    print("\n[Agents]")
    try:
        # In reality, LazyAgentMap expects a fleet or workspace root
        agents = LazyAgentMap(root)
        num_configs = len(agents._discovered_configs)  # pylint: disable=protected-access
        print(f"Discovered {num_configs} agent configurations.")
        for name in list(agents._discovered_configs.keys())[:10]:  # pylint: disable=protected-access
            print(f"  - {name}")
        if num_configs > 10:
            print(f"  ... and {num_configs - 10} more.")
    except (ImportError, OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Error loading AgentRegistry: {e}")
        traceback.print_exc()

    # Check Orchestrators
    print("\n[Orchestrators]")
    try:
        # Mocking a fleet since OrchestratorRegistry needs it
        class MockFleet:
            """Mock fleet class for orchestrator registry testing."""

            def __init__(self) -> None:
                self.workspace_root: Path = root

        orchestrators = LazyOrchestratorMap(MockFleet())
        num_orchestrators = len(orchestrators._configs)  # pylint: disable=protected-access
        print(f"Discovered {num_orchestrators} orchestrator configurations.")
        for name in list(orchestrators._configs.keys()):  # pylint: disable=protected-access
            print(f"  - {name}")
    except (ImportError, OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Error loading OrchestratorRegistry: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_diagnostic()
