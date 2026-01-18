# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for MCP Tool Server Integration.
Delegates to modularized sub-packages in src/infrastructure/mcp_tools/.
"""

from .models import (
    MCPServerConfig,
    MCPServerType,
    ToolStatus,
    SessionState,
    ToolSchema,
    ToolCall,
    ToolResult,
    MCPSession,
)
from .base import MCPToolServer
from .sse import SSEToolServer
from .local import LocalToolServer
from .adapter import SchemaAdapter
from .registry import MCPServerRegistry, SessionManager

# For backward compatibility mapping
ServerType = MCPServerType

__all__ = [
    "MCPServerConfig",
    "MCPServerType",
    "ServerType",
    "ToolStatus",
    "SessionState",
    "ToolSchema",
    "ToolCall",
    "ToolResult",
    "MCPSession",
    "MCPToolServer",
    "SSEToolServer",
    "LocalToolServer",
    "SchemaAdapter",
    "MCPServerRegistry",
    "SessionManager",
]
