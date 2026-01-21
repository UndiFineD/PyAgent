#!/usr/bin/env python3
import logging
from pathlib import Path

# Add project root to sys.path

from src.infrastructure.fleet.agent_registry import AgentRegistry
from src.core.base.version import SDK_VERSION


def test_community_loading_workflow() -> None:
    print(f"--- Testing Community Plugin Workflow (SDK {SDK_VERSION}) ---")
    workspace = Path(".").resolve()

    # 1. Test Registry Gatekeeping
    agents = AgentRegistry.get_agent_map(workspace)

    print("Checking FutureAgent (v3.0)...")
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
        "src\coder\agents\CoderAgent.py",
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
