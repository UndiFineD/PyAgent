#!/usr/bin/env python3
import sys
import logging
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path('.').resolve()))

from src.infrastructure.fleet.OrchestratorRegistry import OrchestratorRegistry
from src.core.base.version import SDK_VERSION

class MockFleet:
    def __init__(self, root: Path):
        self.workspace_root = root

def test_community_orchestrator():
    print(f"--- Running Community Orchestrator Test (SDK {SDK_VERSION}) ---")
    workspace = Path('.').resolve()
    fleet = MockFleet(workspace)
    
    orc_map = OrchestratorRegistry.get_orchestrator_map(fleet)
    
    print("Loading CommunityDemoOrc...")
    try:
        # Using getattr since it's a LazyOrchestratorMap
        orc = getattr(orc_map, "CommunityDemoOrc")
        print(f"Orchestrator Type: {type(orc).__name__}")
        
        result = orc.coordinate("Ping Fleet")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error loading orchestrator: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_community_orchestrator()
