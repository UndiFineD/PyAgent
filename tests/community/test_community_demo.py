#!/usr/bin/env python3
import sys
import logging
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path('.').resolve()))

from src.infrastructure.fleet.AgentRegistry import AgentRegistry
from src.core.base.version import SDK_VERSION

def test_community_demo():
    print(f"--- Running Community Demo Test (SDK {SDK_VERSION}) ---")
    workspace = Path('.').resolve()
    
    agents = AgentRegistry.get_agent_map(workspace)
    
    print("Loading CommunityDemo Agent...")
    try:
        agent = agents["CommunityDemo"]
        print(f"Agent Type: {type(agent).__name__}")
        
        test_input = "Hello PyAgent World!"
        result = agent.run(test_input)
        print(f"Input: {test_input}")
        print(f"Output: {result}")
    except KeyError as e:
        print(f"CommunityDemo agent not found in registry: {e}")
    except Exception as e:
        print(f"Error loading agent: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_community_demo()
