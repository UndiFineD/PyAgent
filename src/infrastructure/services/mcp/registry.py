# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Registry for MCP tool servers and session management.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, List, Optional

from .models import MCPSession, ToolSchema, ToolCall, ToolResult, ToolStatus
from .base import MCPToolServer

logger = logging.getLogger(__name__)


class MCPServerRegistry:
    """Registry for MCP servers."""

    _instance: Optional["MCPServerRegistry"] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._servers = {}
            cls._instance._sessions = {}
        return cls._instance

    @property
    def servers(self) -> Dict[str, MCPToolServer]:
        return self._servers

    def register(self, server: MCPToolServer) -> None:
        """Register a server."""
        self._servers[server.name] = server

    def unregister(self, name: str) -> None:
        """Unregister a server."""
        self._servers.pop(name, None)

    def get(self, name: str) -> Optional[MCPToolServer]:
        """Get server by name."""
        return self._servers.get(name)

    async def connect_all(self) -> Dict[str, MCPSession]:
        """Connect to all registered servers."""
        sessions = {}
        for name, server in self._servers.items():
            try:
                session = await server.connect()
                sessions[name] = session
                self._sessions[name] = session
            except Exception as e:
                logger.error(f"Failed to connect to {name}: {e}")
        return sessions

    async def disconnect_all(self) -> None:
        """Disconnect from all servers."""
        for server in self._servers.values():
            try:
                await server.disconnect()
            except Exception as e:
                logger.warning(f"Error disconnecting {server.name}: {e}")
        self._sessions.clear()

    def get_all_tools(self) -> List[ToolSchema]:
        """Get all tools from all servers."""
        tools = []
        for server in self._servers.values():
            tools.extend(server.tools)
        return tools

    async def call_tool(self, call: ToolCall) -> ToolResult:
        """Route tool call to appropriate server."""
        for server in self._servers.values():
            if server.get_tool(call.name):
                return await server.call_tool(call)

        return ToolResult(
            call_id=call.id,
            name=call.name,
            status=ToolStatus.FAILED,
            error=f"No server found for tool: {call.name}",
        )


class SessionManager:
    """Manage MCP sessions."""

    def __init__(self, registry: Optional[MCPServerRegistry] = None):
        self.registry = registry or MCPServerRegistry()
        self._active_sessions: Dict[str, MCPSession] = {}

    async def create_session(self, server_name: str) -> Optional[MCPSession]:
        """Create session for a server."""
        server = self.registry.get(server_name)
        if not server:
            return None

        session = await server.connect()
        self._active_sessions[session.session_id] = session
        return session

    async def close_session(self, session_id: str) -> bool:
        """Close a session."""
        session = self._active_sessions.pop(session_id, None)
        if not session:
            return False

        server = self.registry.get(session.server_name)
        if server:
            await server.disconnect()
        return True

    def get_session(self, session_id: str) -> Optional[MCPSession]:
        """Get session by ID."""
        return self._active_sessions.get(session_id)

    @property
    def active_sessions(self) -> List[MCPSession]:
        return list(self._active_sessions.values())
