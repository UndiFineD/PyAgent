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

"""
PyAgent MCP Server Ecosystem Integration.

Based on awesome-mcp-servers repository with 500+ MCP servers.
Implements standardized protocol abstraction for 10x tool expansion.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp

from src.core.base.common.models.communication_models import CascadeContext

logger = logging.getLogger("pyagent.tools.mcp")


class MCPServerType(Enum):
    """Types of MCP servers."""
    LOCAL = "local"
    REMOTE = "remote"
    DOCKER = "docker"
    NATIVE = "native"


class MCPCategory(Enum):
    """MCP server categories."""
    DATABASE = "database"
    API = "api"
    FILESYSTEM = "filesystem"
    BROWSER = "browser"
    COMMUNICATION = "communication"
    DEVELOPMENT = "development"
    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MULTIMEDIA = "multimedia"
    OTHER = "other"


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""
    name: str
    description: str
    category: MCPCategory
    server_type: MCPServerType
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    url: Optional[str] = None
    docker_image: Optional[str] = None
    capabilities: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    version: str = "latest"
    enabled: bool = True
    security_level: str = "medium"  # low, medium, high
    timeout: int = 30  # seconds


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    server_name: str
    category: str
    tags: List[str] = field(default_factory=list)


class MCPServerRegistry:
    """
    Registry of available MCP servers.

    Manages discovery, configuration, and lifecycle of MCP servers.
    """

    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or Path(__file__).parent / "registry.json"
        self.servers: Dict[str, MCPServerConfig] = {}
        self.active_servers: Dict[str, 'MCPServerInstance'] = {}
        self.logger = logging.getLogger("pyagent.tools.mcp.registry")

        # Load registry
        self._load_registry()

    def _load_registry(self):
        """Load server registry from file."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)
                    for name, config_data in data.items():
                        config_data['category'] = MCPCategory(config_data['category'])
                        config_data['server_type'] = MCPServerType(config_data['server_type'])
                        self.servers[name] = MCPServerConfig(**config_data)
                self.logger.info(f"Loaded {len(self.servers)} MCP servers from registry")
            except Exception as e:
                self.logger.error(f"Failed to load registry: {e}")
        else:
            self._create_default_registry()

    def _create_default_registry(self):
        """Create default registry with essential MCP servers."""
        default_servers = {
            "filesystem": MCPServerConfig(
                name="filesystem",
                description="Local filesystem operations",
                category=MCPCategory.FILESYSTEM,
                server_type=MCPServerType.NATIVE,
                capabilities=["read", "write", "list", "search"],
                security_level="high"
            ),
            "git": MCPServerConfig(
                name="git",
                description="Git repository operations",
                category=MCPCategory.DEVELOPMENT,
                server_type=MCPServerType.NATIVE,
                capabilities=["status", "commit", "push", "pull", "diff"],
                security_level="medium"
            ),
            "browser": MCPServerConfig(
                name="browser",
                description="Web browser automation",
                category=MCPCategory.BROWSER,
                server_type=MCPServerType.DOCKER,
                docker_image="mcp/browser:latest",
                capabilities=["navigate", "screenshot", "extract", "click"],
                security_level="medium"
            ),
            "sqlite": MCPServerConfig(
                name="sqlite",
                description="SQLite database operations",
                category=MCPCategory.DATABASE,
                server_type=MCPServerType.NATIVE,
                capabilities=["query", "insert", "update", "delete"],
                security_level="high"
            ),
            "http": MCPServerConfig(
                name="http",
                description="HTTP client operations",
                category=MCPCategory.API,
                server_type=MCPServerType.NATIVE,
                capabilities=["get", "post", "put", "delete"],
                security_level="medium"
            )
        }

        self.servers.update(default_servers)
        self._save_registry()

    def _save_registry(self):
        """Save server registry to file."""
        try:
            data = {}
            for name, config in self.servers.items():
                config_dict = {
                    'name': config.name,
                    'description': config.description,
                    'category': config.category.value,
                    'server_type': config.server_type.value,
                    'command': config.command,
                    'args': config.args,
                    'env': config.env,
                    'url': config.url,
                    'docker_image': config.docker_image,
                    'capabilities': config.capabilities,
                    'requirements': config.requirements,
                    'version': config.version,
                    'enabled': config.enabled,
                    'security_level': config.security_level,
                    'timeout': config.timeout
                }
                data[name] = config_dict

            with open(self.registry_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to save registry: {e}")

    def register_server(self, config: MCPServerConfig):
        """Register a new MCP server."""
        self.servers[config.name] = config
        self._save_registry()
        self.logger.info(f"Registered MCP server: {config.name}")

    def unregister_server(self, name: str):
        """Unregister an MCP server."""
        if name in self.servers:
            del self.servers[name]
            if name in self.active_servers:
                self.active_servers[name].stop()
                del self.active_servers[name]
            self._save_registry()
            self.logger.info(f"Unregistered MCP server: {name}")

    def get_servers_by_category(self, category: MCPCategory) -> List[MCPServerConfig]:
        """Get all servers in a category."""
        return [config for config in self.servers.values()
                if config.category == category and config.enabled]

    def get_servers_by_capability(self, capability: str) -> List[MCPServerConfig]:
        """Get all servers with a specific capability."""
        return [config for config in self.servers.values()
                if capability in config.capabilities and config.enabled]

    async def discover_servers(self) -> List[MCPServerConfig]:
        """
        Discover available MCP servers from external sources.

        This integrates with awesome-mcp-servers via the ecosystem populator.
        """
        from .ecosystem_populator import get_expanded_ecosystem
        
        discovered = get_expanded_ecosystem()
        
        for config in discovered:
            if config.name not in self.servers:
                # Ensure category and server_type are Enums if they were stored as strings
                if isinstance(config.category, str):
                    config.category = MCPCategory(config.category)
                if isinstance(config.server_type, str):
                    config.server_type = MCPServerType(config.server_type)
                
                self.servers[config.name] = config
        
        self._save_registry()
        self.logger.info(f"Ecosystem expanded to {len(self.servers)} MCP servers")
        return discovered


class MCPServerInstance:
    """
    Instance of a running MCP server.

    Manages the lifecycle of an MCP server process.
    """

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(f"pyagent.tools.mcp.instance.{config.name}")
        self.tools: List[MCPTool] = []

    async def start(self) -> bool:
        """Start the MCP server."""
        try:
            if self.config.server_type == MCPServerType.DOCKER:
                await self._start_docker_server()
            elif self.config.server_type == MCPServerType.LOCAL:
                await self._start_local_server()
            elif self.config.server_type == MCPServerType.REMOTE:
                await self._connect_remote_server()
            else:
                await self._start_native_server()

            # Initialize tools
            await self._initialize_tools()

            self.logger.info(f"Started MCP server: {self.config.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start MCP server {self.config.name}: {e}")
            return False

    async def stop(self):
        """Stop the MCP server."""
        try:
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                self.process = None

            if self.session:
                await self.session.close()
                self.session = None

            self.logger.info(f"Stopped MCP server: {self.config.name}")

        except Exception as e:
            self.logger.error(f"Error stopping MCP server {self.config.name}: {e}")

    async def _start_docker_server(self):
        """Start a Docker-based MCP server."""
        if not self.config.docker_image:
            raise ValueError("Docker image not specified")

        cmd = [
            "docker", "run", "--rm",
            "-p", "3000:3000",  # Example port mapping
            self.config.docker_image
        ]

        if self.config.args:
            cmd.extend(self.config.args)

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, **self.config.env}
        )

        # Wait for server to be ready
        await asyncio.sleep(2)

    async def _start_local_server(self):
        """Start a local MCP server."""
        if not self.config.command:
            raise ValueError("Command not specified")

        cmd = [self.config.command] + self.config.args

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, **self.config.env}
        )

        # Wait for server to be ready
        await asyncio.sleep(1)

    async def _connect_remote_server(self):
        """Connect to a remote MCP server."""
        if not self.config.url:
            raise ValueError("URL not specified")

        self.session = aiohttp.ClientSession()

    async def _start_native_server(self):
        """Start a native (built-in) MCP server."""
        # For native servers, we don't start external processes
        # They would be implemented as Python classes
        pass

    async def _initialize_tools(self):
        """Initialize available tools from the server."""
        try:
            # Query server for available tools
            tools_data = await self._query_tools()

            for tool_data in tools_data:
                tool = MCPTool(
                    name=tool_data['name'],
                    description=tool_data['description'],
                    input_schema=tool_data['inputSchema'],
                    server_name=self.config.name,
                    category=self.config.category.value,
                    tags=self.config.capabilities
                )
                self.tools.append(tool)

        except Exception as e:
            self.logger.error(f"Failed to initialize tools for {self.config.name}: {e}")

    async def _query_tools(self) -> List[Dict[str, Any]]:
        """Query the server for available tools."""
        # This would implement the MCP protocol to query tools
        # Placeholder implementation
        return [
            {
                'name': f"{self.config.name}_tool",
                'description': f"Tool from {self.config.name} server",
                'inputSchema': {
                    'type': 'object',
                    'properties': {}
                }
            }
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on this server."""
        try:
            # Find the tool
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if not tool:
                raise ValueError(f"Tool {tool_name} not found")

            # Call the tool via MCP protocol
            result = await self._execute_tool_call(tool, arguments)
            return result

        except Exception as e:
            self.logger.error(f"Tool call failed: {e}")
            raise

    async def _execute_tool_call(self, tool: MCPTool, arguments: Dict[str, Any]) -> Any:
        """Execute a tool call via MCP protocol."""
        # Placeholder for MCP protocol implementation
        # This would send JSON-RPC requests to the server
        return {"result": "Tool executed successfully"}


class MCPBridge:
    """
    MCP Protocol Bridge.

    Provides standardized interface for external services through MCP servers.
    """

    def __init__(self, registry: MCPServerRegistry):
        self.registry = registry
        self.active_servers: Dict[str, MCPServerInstance] = {}
        self.logger = logging.getLogger("pyagent.tools.mcp.bridge")

    async def initialize(self):
        """Initialize the MCP bridge."""
        # Start essential servers
        essential_servers = ["filesystem", "git"]

        for server_name in essential_servers:
            if server_name in self.registry.servers:
                await self.start_server(server_name)

    async def start_server(self, server_name: str) -> bool:
        """Start an MCP server."""
        if server_name not in self.registry.servers:
            self.logger.error(f"Server {server_name} not found in registry")
            return False

        if server_name in self.active_servers:
            self.logger.warning(f"Server {server_name} already running")
            return True

        config = self.registry.servers[server_name]
        instance = MCPServerInstance(config)

        if await instance.start():
            self.active_servers[server_name] = instance
            return True
        else:
            return False

    async def stop_server(self, server_name: str):
        """Stop an MCP server."""
        if server_name in self.active_servers:
            await self.active_servers[server_name].stop()
            del self.active_servers[server_name]

    def get_available_tools(self) -> List[MCPTool]:
        """Get all available tools from active servers."""
        tools = []
        for server in self.active_servers.values():
            tools.extend(server.tools)
        return tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any],
                        context: Optional[CascadeContext] = None) -> Any:
        """
        Call an MCP tool.

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            context: Optional cascade context

        Returns:
            Tool execution result
        """
        # Find which server has this tool
        for server_name, server in self.active_servers.items():
            tool = next((t for t in server.tools if t.name == tool_name), None)
            if tool:
                try:
                    result = await server.call_tool(tool_name, arguments)

                    # Log in cascade context if provided
                    if context:
                        context.add_log_entry(
                            f"MCP Tool Call: {tool_name}",
                            {"server": server_name, "arguments": arguments, "result": result}
                        )

                    return result

                except Exception as e:
                    self.logger.error(f"MCP tool call failed: {e}")
                    raise

        raise ValueError(f"Tool {tool_name} not found in any active server")

    def get_servers_by_category(self, category: str) -> List[str]:
        """Get server names by category."""
        return [name for name, config in self.registry.servers.items()
                if config.category.value == category and config.enabled]

    def get_servers_by_capability(self, capability: str) -> List[str]:
        """Get server names by capability."""
        return [name for name, config in self.registry.servers.items()
                if capability in config.capabilities and config.enabled]


class MCPToolOrchestrator:
    """
    Intelligent tool selection and orchestration.

    Uses AI to select the best MCP tools for a given task.
    """

    def __init__(self, mcp_bridge: MCPBridge, inference_engine):
        self.mcp_bridge = mcp_bridge
        self.inference_engine = inference_engine
        self.logger = logging.getLogger("pyagent.tools.mcp.orchestrator")

    async def select_tools(self, task_description: str, max_tools: int = 3) -> List[MCPTool]:
        """
        Select the most appropriate MCP tools for a task.

        Args:
            task_description: Description of the task
            max_tools: Maximum number of tools to select

        Returns:
            List of selected tools
        """
        available_tools = self.mcp_bridge.get_available_tools()

        if not available_tools:
            return []

        # Create tool selection prompt
        tools_list = "\n".join([
            f"- {tool.name}: {tool.description} (Category: {tool.category}, Tags: {', '.join(tool.tags)})"
            for tool in available_tools
        ])

        prompt = f"""Given this task: "{task_description}"

Select the most appropriate tools from this list:

{tools_list}

Return only the tool names, one per line, in order of relevance.
Select at most {max_tools} tools."""

        try:
            response = await self.inference_engine.generate(
                prompt=prompt,
                temperature=0.1,  # Low temperature for consistent selection
                max_tokens=100
            )

            selected_names = [
                line.strip() for line in response.split('\n')
                if line.strip()
            ][:max_tools]

            selected_tools = []
            for name in selected_names:
                tool = next((t for t in available_tools if t.name == name), None)
                if tool:
                    selected_tools.append(tool)

            return selected_tools

        except Exception as e:
            self.logger.error(f"Tool selection failed: {e}")
            # Fallback: return first max_tools tools
            return available_tools[:max_tools]

    async def orchestrate_tools(self, task_description: str,
                                context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """
        Orchestrate tool execution for a complex task.

        Args:
            task_description: Description of the task
            context: Optional cascade context

        Returns:
            Orchestration result
        """
        # Select appropriate tools
        selected_tools = await self.select_tools(task_description)

        if not selected_tools:
            return {"error": "No suitable tools found"}

        # Execute tools in sequence
        results = {}
        for tool in selected_tools:
            try:
                # For now, use empty arguments - in production this would be more sophisticated
                result = await self.mcp_bridge.call_tool(tool.name, {}, context)
                results[tool.name] = result
            except Exception as e:
                results[tool.name] = {"error": str(e)}

        return {
            "task": task_description,
            "selected_tools": [tool.name for tool in selected_tools],
            "results": results
        }
