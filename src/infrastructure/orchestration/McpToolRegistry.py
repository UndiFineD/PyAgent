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

from __future__ import annotations
import logging
from typing import Any, Dict, List, TYPE_CHECKING
from .ToolRegistry import ToolRegistry

if TYPE_CHECKING:
    from ..fleet.FleetManager import FleetManager

class McpToolRegistry(ToolRegistry):
    """Registry specialized for Model Context Protocol (MCP) tools."""

    def __init__(self, fleet: FleetManager) -> None:
        super().__init__(fleet)
        self.server_proxies = {}

    def register_mcp_server(self, server_name: str, tools: list[dict[str, Any]], call_handler) -> None:
        """Dynamically registers tools from an MCP server."""
        logging.info(f"McpToolRegistry: Registering tools for server: {server_name}")
        
        for tool_def in tools:
            tool_name = tool_def.get("name")
            description = tool_def.get("description", "")
            
            # Create a proxy function that calls the handler
            def mcp_proxy_func(**kwargs):
                return call_handler(tool_name, **kwargs)
            
            mcp_proxy_func.__name__ = tool_name
            mcp_proxy_func.__doc__ = description
            
            self.register_tool(
                owner_name=f"mcp.{server_name}",
                func=mcp_proxy_func,
                category="mcp",
                priority=10 # Higher priority for external tools
            )

    async def call_mcp_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a tool and specifically handle MCP result formatting."""
        result = await self.call_tool(tool_name, **kwargs)
        if isinstance(result, dict) and "result" in result:
             return result["result"]
        return result