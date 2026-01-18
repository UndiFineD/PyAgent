# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for MCP Tool Server Integration.
Delegates to modularized sub-packages in src/infrastructure/mcp_tools/.
"""

from __future__ import annotations

from .models import (
    MCPServerConfig,
    MCPServerType,
    ToolSchema,
    ToolCall,
    ToolResult,
    ToolStatus,
    SessionState,
    MCPSession,
)
from .base import MCPToolServer as MCPToolServerBase
from .sse import SSEMCPServer
from .local import LocalMCPServer
from .adapter import SchemaAdapter
from .registry import MCPServerRegistry, SessionManager

# For backward compatibility
MCPToolServer = MCPToolServerBase

__all__ = [
    "MCPServerConfig",
    "MCPServerType",
    "ToolSchema",
    "ToolCall",
    "ToolResult",
    "ToolStatus",
    "SessionState",
    "MCPSession",
    "MCPToolServer",
    "SSEMCPServer",
    "LocalMCPServer",
    "MCPServerRegistry",
    "SchemaAdapter",
    "SessionManager",
]
