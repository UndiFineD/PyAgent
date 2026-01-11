"""Unit tests for OrchestratorRegistry and lazy loading resilience."""
#!/usr/bin/env python3
import sys
import logging
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path('.').resolve()))

from src.infrastructure.fleet.OrchestratorRegistry import LazyOrchestratorMap, OrchestratorRegistry
from src.core.base.version import SDK_VERSION

class MockFleet:
    def __init__(self, root: Path) -> None:
        self.workspace_root: Path = root

def test_orchestrator_workflow() -> None:
    print(f"--- Testing Orchestrator Workflow (SDK {SDK_VERSION}) ---")
    workspace: Path = Path('.').resolve()
    fleet = MockFleet(workspace)
    
    # 1. Test Registry Gatekeeping
    orc_map: LazyOrchestratorMap = OrchestratorRegistry.get_orchestrator_map(fleet)
    
    print(f"Checking FutureOrchestrator (v3.0)...")
    is_in_manifest: bool = "FutureOrchestrator" in orc_map._manifest_configs
    print(f"FutureOrchestrator in manifest? {is_in_manifest} (Expect: False)")

    print(f"Checking LegacyOrchestrator (v1.0)...")
    is_in_manifest: bool = "LegacyOrchestrator" in orc_map._manifest_configs
    print(f"LegacyOrchestrator in manifest? {is_in_manifest} (Expect: True)")

    # 2. Test Self-Healing reload
    print(f"\n--- Testing Orchestrator Self-Healing Reload ---")
    orc_map._configs["HealTest"] = ("non.existent.module", "HealTestOrc", False, None)
    
    # Try to load it - should return a ResilientStub
    stub = getattr(orc_map, "HealTest")
    print(f"Initial load of HealTest: {type(stub).__name__}")
    
    # Simulate 'fixing' it by pointing to a real class (e.g. MemoryEngine)
    orc_map._configs["HealTest"] = ("src.logic.agents.cognitive.context.engines.MemoryEngine", "MemoryEngine", False, "")
    
    # Trigger self-healing try_reload
    success: bool = orc_map.try_reload("HealTest")
    print(f"Reload successful? {success}")
    
    if success:
        new_instance = getattr(orc_map, "HealTest")
        print(f"New instance type: {type(new_instance).__name__}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    test_orchestrator_workflow()
