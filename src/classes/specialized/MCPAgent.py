#!/usr/bin/env python3

"""Agent specializing in Model Context Protocol (MCP) integration.
Acts as a bridge between the PyAgent fleet and external MCP servers.
Inspired by mcp-server-spec-driven-development and awesome-mcp-servers.
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool
from src.classes.fleet.MCPConnector import MCPConnector

class MCPAgent(BaseAgent):
    """Enables the fleet to discover and utilize external tools via the MCP protocol."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = Path(self.file_path).parent.parent.parent
        self.connectors: Dict[str, MCPConnector] = {}
        self._system_prompt = (
            "You are the MCP Integration Agent. "
            "Your role is to manage connections to Model Context Protocol servers. "
            "You can list available MCP tools, call them, and register them with the fleet. "
            "Prioritize the 'tools' part of the MCP spec to expand fleet capabilities."
        )

    @as_tool
    def list_mcp_servers(self) -> str:
        """Discovers local MCP configuration files."""
        mcp_configs = list(self.workspace_root.rglob("mcp.json"))
        if not mcp_configs:
            # Fallback to a mock for demo purposes if no file found
            return "No local `mcp.json` configs found. Check common locations."
        
        report = ["## 🔌 Discovered MCP Servers"]
        for cfg in mcp_configs:
            try:
                with open(cfg, 'r') as f:
                    data = json.load(f)
                    for server_name, server_config in data.get("mjs_servers", {}).items():
                        report.append(f"- **{server_name}**: {server_config.get('command')}")
            except Exception as e:
                report.append(f"- Error reading `{cfg}`: {e}")
        return "\n".join(report)

    @as_tool
    def call_mcp_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Calls an MCP tool via the live connector."""
        if server_name not in self.connectors:
            # For this demo, we assume we can find the server config
            return f"Error: MCP Server '{server_name}' not initialized. Call 'initialize_mcp_server' first."
        
        # Intelligence Harvesting (Phase 108)
        if self.recorder:
            self.recorder.record_lesson("mcp_tool_call", {"server": server_name, "tool": tool_name})
            
        connector = self.connectors[server_name]
        response = connector.call("tools/call", {"name": tool_name, "arguments": arguments})
        
        if "error" in response:
            if self.recorder:
                self.recorder.record_lesson("mcp_tool_error", {"server": server_name, "tool": tool_name, "error": response["error"]})
            return f"MCP Error: {response['error']}"
        
        return json.dumps(response.get("result", {}), indent=2)

    @as_tool
    def initialize_mcp_server(self, name: str, command: List[str]) -> str:
        """Initializes and connects to a specific MCP server."""
        connector = MCPConnector(name, command)
        connector.start()
        if connector.is_running:
            self.connectors[name] = connector
            if self.recorder:
                self.recorder.record_lesson("mcp_server_init", {"name": name, "status": "success"})
            return f"Successfully started MCP server '{name}'"
        else:
            if self.recorder:
                self.recorder.record_lesson("mcp_server_init", {"name": name, "status": "failed"})
            return f"Failed to start MCP server '{name}'"

    def improve_content(self, prompt: str) -> str:
        """Handle MCP-related requests."""
        if "list" in prompt.lower():
            return self.list_mcp_servers()
        return "MCP Agent ready. Specify a tool call or server discovery task."
