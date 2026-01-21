#!/usr/bin/env python3
import sys
import os
import logging
from pathlib import Path

# Ensure src is on path
sys.path.append(os.getcwd())

from src.infrastructure.swarm.fleet.agent_registry import LazyAgentMap
from src.infrastructure.swarm.fleet.orchestrator_registry import LazyOrchestratorMap

def run_diagnostic():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
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
            def __init__(self): self.workspace_root = root

        orchestrators = LazyOrchestratorMap(MockFleet())
        print(f"Discovered {len(orchestrators._configs)} orchestrator configurations.")
        for name in list(orchestrators._configs.keys()):
            print(f"  - {name}")
    except Exception as e:
        print(f"Error loading OrchestratorRegistry: {e}")

if __name__ == "__main__":
    run_diagnostic()
