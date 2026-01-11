#!/usr/bin/env python3
import sys
import logging
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path('.').resolve()))

from src.infrastructure.fleet.AgentRegistry import AgentRegistry

def test_broken_community_plugin() -> None:
    print(f"--- Running Broken Plugin Resilience Test ---")
    workspace = Path('.').resolve()
    agents = AgentRegistry.get_agent_map(workspace)
    
    print("Attempting to load BrokenCommunity...")
    try:
        agent = agents["BrokenCommunity"]
        print(f"Agent Type: {type(agent).__name__}")
        
        # This should fail gracefully or show it's a stub
        from src.infrastructure.fleet.ResilientStubs import ResilientStub
        if isinstance(agent, ResilientStub):
            print("Successfully caught broken plugin and returned ResilientStub!")
            # Use get_status() to see the real error since __getattr__ traps other field access
            status = agent.get_status()
            print(f"Stub Error Detail: {status['error']}")
        else:
            print("Wait, it loaded? (Unexpected)")
            
    except Exception as e:
        print(f"Script crashed (Unexpected): {e}")

    print("\nVerifying that other agents still work...")
    try:
        demo = agents["CommunityDemo"]
        print(f"CommunityDemo still works: {demo.run('test')}")
    except Exception as e:
        print(f"CommunityDemo failed because of broken plugin: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    test_broken_community_plugin()
