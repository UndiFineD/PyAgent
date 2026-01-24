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
Registry check tool.
"""

import logging
import os
import sys
from pathlib import Path

# Ensure src is on path
sys.path.append(os.getcwd())

from src.infrastructure.swarm.fleet.agent_registry import LazyAgentMap  # noqa: E402
from src.infrastructure.swarm.fleet.orchestrator_registry import \
    LazyOrchestratorMap  # noqa: E402


def run_diagnostic():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    root = Path(os.getcwd())

    print("=== PyAgent Registry Diagnostic ===")

    # Check Agents
    print("\n[Agents]")
    try:
        # In reality, LazyAgentMap expects a fleet or workspace root
        agents = LazyAgentMap(root)
        print(f"Discovered {len(agents._discovered_configs)} agent configurations.")
        for name in list(agents._discovered_configs.keys())[:10]:
            print(f"  - {name}")
        if len(agents._discovered_configs) > 10:
            print(f"  ... and {len(agents._discovered_configs) - 10} more.")
    except Exception as e:
        print(f"Error loading AgentRegistry: {e}")

    # Check Orchestrators
    print("\n[Orchestrators]")
    try:
        # Mocking a fleet since OrchestratorRegistry needs it
        class MockFleet:
            def __init__(self):
                self.workspace_root = root

        orchestrators = LazyOrchestratorMap(MockFleet())
        print(f"Discovered {len(orchestrators._configs)} orchestrator configurations.")
        for name in list(orchestrators._configs.keys()):
            print(f"  - {name}")
    except Exception as e:
        print(f"Error loading OrchestratorRegistry: {e}")


if __name__ == "__main__":
    run_diagnostic()
