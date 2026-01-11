#!/usr/bin/env python3
import logging
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.infrastructure.fleet.FleetManager import FleetManager
from src.logic.agents.system.MCPAgent import MCPAgent

def test_phase_16() -> None:
    """Validate MCP integration and service mesh synchronization."""
    logging.basicConfig(level=logging.INFO)
    workspace = os.getcwd()
    fleet = FleetManager(workspace)
    
    print("\n--- Phase 16: MCP Integration (Server Init) ---")
    mcp_agent = MCPAgent(str(Path(workspace) / "src/logic/agents/system/MCPAgent.py"))
    
    # We use 'python' to run our mock server
    res = mcp_agent.initialize_mcp_server("test_server", ["python", str(Path(workspace) / "mock_mcp_server.py")])
    print(f"Init Status: {res}")

    print("\n--- Phase 16: MCP Tool Call ---")
    res = mcp_agent.call_mcp_tool("test_server", "echo_tool", {"msg": "Hello MCP!"})
    print(f"Tool Call Response: {res}")

    print("\n--- Phase 16: Service Mesh Sync ---")
    fleet.register_remote_node("http://remote-node-1:8080", ["Analyzer"])
    fleet.mesh.sync_with_remote("http://remote-node-1:8080")
    status = fleet.mesh.get_mesh_status()
    print(f"Mesh Status: {status}")

    if "Echo: Hello MCP!" in res and status["remote_nodes"] > 0:
        print("\nMCP Service Mesh validation COMPLETED.")
    else:
        print("\nMCP Service Mesh validation FAILED.")

if __name__ == "__main__":
    test_phase_16()
