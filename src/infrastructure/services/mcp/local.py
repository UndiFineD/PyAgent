# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Local (in-process) MCP tool server implementation.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional

from .models import (
    MCPServerConfig,
    MCPSession,
    ToolSchema,
    ToolCall,
    ToolResult,
    ToolStatus,
    SessionState,
)
from .base import MCPToolServer


class LocalMCPServer(MCPToolServer):
    """In-process MCP server for local tool execution."""

    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self._tool_handlers: Dict[str, Callable] = {}

    def register_tool(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register a local tool."""
        schema = ToolSchema(
            name=name,
            description=description,
            parameters=parameters or {},
            server_name=self.name,
        )
        self._tools[name] = schema
        self._tool_handlers[name] = handler

    async def connect(self) -> MCPSession:
        """Local connection is always ready."""
        self._session = self._create_session()
        self._session.state = SessionState.READY
        self._session.connected_at = time.time()
        self._session.tools = list(self._tools.values())
        return self._session

    async def disconnect(self) -> None:
        """Local disconnect."""
        if self._session:
            self._session.state = SessionState.DISCONNECTED

    async def list_tools(self) -> List[ToolSchema]:
        """List registered tools."""
        return self._apply_namespace_filter(list(self._tools.values()))

    async def call_tool(self, call: ToolCall) -> ToolResult:
        """Execute local tool."""
        start_time = time.time()
        handler = self._tool_handlers.get(call.name)
        if not handler:
            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.FAILED,
                error=f"Unknown tool: {call.name}",
            )

        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**call.arguments)
            else:
                result = handler(**call.arguments)

            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.COMPLETED,
                result=result,
                duration_ms=(time.time() - start_time) * 1000,
            )
        except Exception as e:
            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.FAILED,
                error=str(e),
                duration_ms=(time.time() - start_time) * 1000,
            )
