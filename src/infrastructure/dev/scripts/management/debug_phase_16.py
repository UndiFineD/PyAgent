#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
# Add src to path

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import sys
import os
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager
from src.logic.agents.system.MCPAgent import MCPAgent

sys.path.append(str(Path(__file__).parent))

__version__ = VERSION

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