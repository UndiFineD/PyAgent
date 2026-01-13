import os
import sys
import logging
from pathlib import Path

# Add the workspace root to sys.path

from src.classes.fleet.AgentRegistry import AgentRegistry

def test_resilience():
    logging.basicConfig(level=logging.INFO)
    print("🧪 Testing Resilience of AgentRegistry...")
    
    workspace_root = Path(os.getcwd())
    agents = AgentRegistry.get_agent_map(workspace_root)
    
    print("\n--- Attempting to load BrokenImportAgent ---")
    broken_agent = agents.get("BrokenImport")
    
    if broken_agent:
        print(f"✅ Found agent: {type(broken_agent).__name__}")
        res = broken_agent.improve_content("test")
        print(f"✅ Mock response: {res}")
        
        if "ERROR: Component 'BrokenImport' failed to load" in res:
            print("✅ ResilientStub successfully handled the broken import.")
        else:
            print("❌ Stub did not return expected error message.")
    else:
        print("❌ Agent not found even with stub.")

    print("\n🏁 Resilience Verification Complete.")

if __name__ == "__main__":
    test_resilience()
