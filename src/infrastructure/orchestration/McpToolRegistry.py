#!/usr/bin/env python3

"""Registry specialized for Model Context Protocol (MCP) tools."""

from __future__ import annotations

import json
import logging
from typing import Dict, List, Any, Optional
from .ToolRegistry import ToolRegistry
from .ToolCore import ToolMetadata

class McpToolRegistry(ToolRegistry):
    """
    Extends ToolRegistry to handle dynamically discovered MCP tools.
    Supports tool execution via MCPConnector.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.mcp_servers: Dict[str, Any] = {} # server_name -> connector

    def register_mcp_server(self, name: str, connector: Any) -> None:
        """Link an active MCP connector to the registry."""
        self.mcp_servers[name] = connector
        logging.info(f"MCP Server '{name}' registered with ToolRegistry.")

    def register_mcp_tools(self, server_name: str, tools_list: List[Dict[str, Any]]) -> None:
        """Registers a list of tools from an MCP server."""
        for tool in tools_list:
            tool_name = tool.get("name")
            description = tool.get("description", "No description")
            params = tool.get("inputSchema", {}).get("properties", {})
            
            # Create a proxy function that calls the MCP tool
            def mcp_proxy_func(**kwargs: Any) -> Any:
                connector = self.mcp_servers.get(server_name)
                if not connector:
                    raise RuntimeError(f"MCP Server '{server_name}' not found for tool '{tool_name}'")
                return connector.call("tools/call", {"name": tool_name, "arguments": kwargs})

            # Override name to match registry expectations
            mcp_proxy_func.__name__ = tool_name
            mcp_proxy_func.__doc__ = description
            
            self.register_tool(
                owner_name=f"mcp.{server_name}",
                func=mcp_proxy_func,
                category="mcp",
                priority=10 # Higher priority for external tools
            )

    def call_mcp_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a tool and specifically handle MCP result formatting."""
        result = self.call_tool(tool_name, **kwargs)
        if isinstance(result, dict) and "result" in result:
             return result["result"]
        return result
