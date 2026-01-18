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


"""Agent specializing in Model Context Protocol (MCP) integration.
Acts as a bridge between the PyAgent fleet and external MCP servers.
Inspired by mcp-server-spec-driven-development and awesome-mcp-servers.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import json
import asyncio
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool
from src.infrastructure.fleet.MCPConnector import MCPConnector

__version__ = VERSION


class MCPAgent(BaseAgent):
    """Enables the fleet to discover and utilize external tools via the MCP protocol."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = Path(self.file_path).parent.parent.parent
        self.connectors: dict[str, MCPConnector] = {}
        self._system_prompt = (
            "You are the MCP Integration Agent. "
            "Your role is to manage connections to Model Context Protocol servers. "
            "You can list available MCP tools, call them, and register them with the fleet. "
            "Prioritize the 'tools' part of the MCP spec to expand fleet capabilities."
        )

    @as_tool
    async def list_mcp_servers(self) -> str:
        """Discovers local MCP configuration files."""

        def discover() -> str:
            mcp_configs = list(self.workspace_root.rglob("mcp.json"))
            if not mcp_configs:
                return "No local `mcp.json` configs found. Check common locations."

            report = ["## 🔌 Discovered MCP Servers"]
            for cfg in mcp_configs:
                try:
                    with open(cfg) as f:
                        data = json.load(f)
                        for server_name, server_config in data.get(
                            "mjs_servers", {}
                        ).items():
                            report.append(
                                f"- **{server_name}**: {server_config.get('command')}"
                            )
                except Exception as e:
                    report.append(f"- Error reading `{cfg}`: {e}")
            return "\n".join(report)

        return await asyncio.to_thread(discover)

    @as_tool
    async def call_mcp_tool(
        self, server_name: str, tool_name: str, arguments: dict[str, Any]
    ) -> str:
        """Calls an MCP tool via the live connector."""
        if server_name not in self.connectors:
            return f"Error: MCP Server '{server_name}' not initialized. Call 'initialize_mcp_server' first."

        # Intelligence Harvesting (Phase 108)
        if hasattr(self, "recorder") and self.recorder:
            self.recorder.record_lesson(
                "mcp_tool_call", {"server": server_name, "tool": tool_name}
            )

        connector = self.connectors[server_name]
        # MCPConnector might be sync, so wrap in thread
        response = await asyncio.to_thread(
            connector.call, "tools/call", {"name": tool_name, "arguments": arguments}
        )

        if "error" in response:
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_lesson(
                    "mcp_tool_error",
                    {
                        "server": server_name,
                        "tool": tool_name,
                        "error": response["error"],
                    },
                )
            return f"MCP Error: {response['error']}"

        return json.dumps(response.get("result", {}), indent=2)

    @as_tool
    async def initialize_mcp_server(self, name: str, command: list[str]) -> str:
        """Initializes and connects to a specific MCP server."""
        connector = MCPConnector(name, command)
        await asyncio.to_thread(connector.start)
        if connector.is_running:
            self.connectors[name] = connector
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_lesson(
                    "mcp_server_init", {"name": name, "status": "success"}
                )
            return f"Successfully started MCP server '{name}'"
        else:
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_lesson(
                    "mcp_server_init", {"name": name, "status": "failed"}
                )
            return f"Failed to start MCP server '{name}'"

    async def improve_content(self, prompt: str) -> str:
        """Handle MCP-related requests."""
        if "list" in prompt.lower():
            return await self.list_mcp_servers()
        # Fallback to base logic if needed
        return await super().improve_content(prompt)
