
import sys
import os
from pathlib import Path
import logging

# Setup path
sys.path.append(os.getcwd())

# Mock fleet













class MockFleet:



    def __init__(self):
        self.workspace_root = Path(os.getcwd())


from src.infrastructure.fleet.OrchestratorRegistry import LazyOrchestratorMap


def test_registry():
    logging.basicConfig(level=logging.DEBUG)
    fleet = MockFleet()
    registry = LazyOrchestratorMap(fleet)

    print("Discovered configs keys:", list(registry._discovered_configs.keys()))
    print("All configs keys:", list(registry._configs.keys()))

    try:
        sb = registry.SignalBusOrchestrator
        print(f"Successfully loaded: {sb}")
    except AttributeError as e:
        print(f"Failed to load SignalBusOrchestrator: {e}")
    except Exception as e:
        print(f"Exception loading SignalBusOrchestrator: {e}")

    try:
        sh = registry.SelfHealingOrchestrator
        print(f"Successfully loaded: {sh}")
    except AttributeError as e:
        print(f"Failed to load SelfHealingOrchestrator: {e}")




if __name__ == "__main__":
    test_registry()
