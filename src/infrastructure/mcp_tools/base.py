# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Base MCP tool server abstraction.
"""

from __future__ import annotations

import logging
import uuid
import time
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional

from .models import (
    MCPServerConfig,
    MCPSession,
    ToolSchema,
    ToolCall,
    ToolResult,
    SessionState,
)

logger = logging.getLogger(__name__)


class MCPToolServer(ABC):
    """
    Abstract base class for MCP tool servers.
    """

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self._session: Optional[MCPSession] = None
        self._tools: Dict[str, ToolSchema] = {}

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def session(self) -> Optional[MCPSession]:
        return self._session

    @property
    def tools(self) -> List[ToolSchema]:
        return list(self._tools.values())

    @abstractmethod
    async def connect(self) -> MCPSession:
        """Connect to the server."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the server."""
        ...

    @abstractmethod
    async def list_tools(self) -> List[ToolSchema]:
        """List available tools."""
        ...

    @abstractmethod
    async def call_tool(self, call: ToolCall) -> ToolResult:
        """Execute a tool call."""
        ...

    async def call_tool_streaming(
        self,
        call: ToolCall,
    ) -> AsyncIterator[str]:
        """Execute a tool call with streaming output."""
        result = await self.call_tool(call)
        if result.is_success:
            yield str(result.result)

    def get_tool(self, name: str) -> Optional[ToolSchema]:
        """Get tool by name."""
        return self._tools.get(name)

    def _apply_namespace_filter(self, tools: List[ToolSchema]) -> List[ToolSchema]:
        """Apply namespace filter to tools."""
        if not self.config.namespace_filter:
            return tools

        return [
            t for t in tools
            if t.namespace is None or t.namespace in self.config.namespace_filter
        ]

    def _create_session(self) -> MCPSession:
        """Create a new session."""
        return MCPSession(
            session_id=str(uuid.uuid4()),
            server_name=self.name,
            state=SessionState.CONNECTING,
        )
