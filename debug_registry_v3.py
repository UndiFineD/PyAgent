
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
        self._capability_hints = {



            "synthetic_data": "SyntheticDataAgent"
        }



from src.infrastructure.fleet.AgentRegistry import LazyAgentMap



def test_registry():
    logging.basicConfig(level=logging.INFO)
    fleet = MockFleet()

    # Check Agents




    print("\n--- Checking AgentRegistry ---")
    agents = LazyAgentMap(fleet.workspace_root, fleet_instance=fleet)

    targets = ["FeatureStoreAgent", "SyntheticDataAgent"]
    for tgt in targets:
        if tgt in agents:
            print(f"'{tgt}' FOUND in agents.")
            try:
                inst = agents[tgt]
                print(f"Successfully loaded {tgt}: {inst}")
            except Exception as e:
                print(f"Failed to instantiate {tgt}: {e}")
        else:
            print(f"'{tgt}' NOT FOUND in agents.")




if __name__ == "__main__":
    test_registry()
