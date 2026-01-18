# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for MCP Tool Server Integration.
Delegates to modularized sub-packages in src/infrastructure/mcp_tools/.
"""

from .models import (
    MCPServerConfig as MCPServerConfig,
    ServerType as MCPServerType,
    ToolSchema as ToolSchema,
    ToolCall as ToolCall,
    ToolResult as ToolResult,
    ToolStatus as ToolStatus,
    MCPSession as MCPSession,
)
from .base import MCPToolServer as MCPToolServerBase
from .sse import SSEToolServer as SSEToolServer
from .local import LocalToolServer as LocalToolServer
from .adapter import SchemaAdapter as SchemaAdapter
from .registry import MCPServerRegistry as MCPServerRegistry, SessionManager as SessionManager

# For backward compatibility
MCPToolServer = MCPToolServerBase
SessionState = ToolStatus # Mapping if needed, or keeping it for compatibility
