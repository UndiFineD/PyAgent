
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


from src.infrastructure.fleet.AgentRegistry import LazyAgentMap
from src.infrastructure.fleet.OrchestratorRegistry import LazyOrchestratorMap




def test_registry():
    logging.basicConfig(level=logging.INFO)
    fleet = MockFleet()

    # Check Agents
    print("\n--- Checking AgentRegistry ---")
    agents = LazyAgentMap(fleet.workspace_root, fleet_instance=fleet)
    # print("Discovered Agent configs keys:", list(agents._discovered_configs.keys()))

    tgt = "FeatureStoreAgent"
    if tgt in agents:
        print(f"'{tgt}' FOUND in agents.")
        try:
            inst = agents[tgt]
            print(f"Successfully loaded {tgt}: {inst}")
        except Exception as e:
            print(f"Failed to instantiate {tgt}: {e}")
    else:


        print(f"'{tgt}' NOT FOUND in agents.")

    # Check Orchestrators
    print("\n--- Checking OrchestratorRegistry ---")
    orchestrators = LazyOrchestratorMap(fleet)

    tgt_orch = "SignalBusOrchestrator"

    # Check if getattr works
    try:
        orch = getattr(orchestrators, tgt_orch)
        print(f"Successfully loaded {tgt_orch}: {orch}")
    except Exception as e:
        print(f"Failed to load {tgt_orch}: {e}")




if __name__ == "__main__":
    test_registry()
