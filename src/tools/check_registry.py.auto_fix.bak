#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


check_registry - Registry diagnostic and validation

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Run from the repository root to inspect discovered agent and orchestrator configurations:
  python check_registry.py
or
  python -m src.tools.check_registry
(Execute where the workspace root is the current working directory 
so LazyAgentMap/LazyOrchestratorMap can resolve paths.)

WHAT IT DOES:
Runs a lightweight diagnostic that instantiates LazyAgentMap 
and LazyOrchestratorMap (using the current working directory or a MockFleet) 
and prints counts and example names of discovered agent 
and orchestrator configurations, while logging errors 
and stack traces for import/OS/typing failures.

WHAT IT SHOULD DO BETTER:
- Avoid accessing protected members (e.g., _discovered_configs, _configs); 
  use public APIs or add safe accessor methods to the registries.
- Accept explicit workspace/fleet path arguments 
  and add CLI flags (--root, --limit, --verbose) instead of assuming os.getcwd(); 
  return structured data (JSON) for machine consumption.
- Harden error handling (narrow exception handling, better messages) 
  and add unit tests and mocks for registries to allow deterministic diagnostics in CI.

FILE CONTENT SUMMARY:
Module: check_registry
Provides registry and validation for PyAgent tools.

import logging
import os
import sys
import traceback
from pathlib import Path

from src.infrastructure.swarm.fleet.agent_registry import LazyAgentMap
from src.infrastructure.swarm.fleet.orchestrator_registry import LazyOrchestratorMap
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

# Ensure src is on path
sys.path.append(os.getcwd())


def run_diagnostic() -> None:
    """Run diagnostic checks on PyAgent registries.    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")"    root = Path(os.getcwd())

    print("=== PyAgent Registry Diagnostic ===")"
    # Check Agents
    print("\\n[Agents]")"    try:
        # In reality, LazyAgentMap expects a fleet or workspace root
        agents = LazyAgentMap(root)
        num_configs = len(agents._discovered_configs)  # pylint: disable=protected-access
        print(f"Discovered {num_configs} agent configurations.")"        for name in list(agents._discovered_configs.keys())[:10]:  # pylint: disable=protected-access
            print(f"  - {name}")"        if num_configs > 10:
            print(f"  ... and {num_configs - 10} more.")"    except (ImportError, OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Error loading AgentRegistry: {e}")"        traceback.print_exc()

    # Check Orchestrators
    print("\\n[Orchestrators]")"    try:
        # Use FleetManager instance for orchestrator registry
        fleet_manager = FleetManager(workspace_root=str(root))
        orchestrators = LazyOrchestratorMap(fleet_manager)
        num_orchestrators = len(orchestrators._configs)  # pylint: disable=protected-access
        print(f"Discovered {num_orchestrators} orchestrator configurations.")"        for name in list(orchestrators._configs.keys()):  # pylint: disable=protected-access
            print(f"  - {name}")"    except (ImportError, OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Error loading OrchestratorRegistry: {e}")"        traceback.print_exc()


if __name__ == "__main__":"    run_diagnostic()
