#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for MCP Tool Server Integration.
Delegates to modularized sub-packages in src/infrastructure/mcp_tools/.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .adapter import SchemaAdapter
from .base import MCPToolServer as MCPToolServerBase
from .local import LocalMCPServer
from .models import (MCPServerConfig, MCPServerType, MCPSession, SessionState,
                     ToolCall, ToolResult, ToolSchema, ToolStatus)
from .registry import MCPServerRegistry, SessionManager
from .sse import SSEMCPServer

# For backward compatibility mapping
MCPToolServer = MCPToolServerBase
ServerType = MCPServerType


def adapt_tool_schema(schema: ToolSchema | List[ToolSchema]) -> List[Dict[str, Any]]:
    """Legacy helper for adaptation."""
    if isinstance(schema, ToolSchema):
        return [schema.to_openai_format()]
    return SchemaAdapter.to_openai(schema)


async def create_mcp_session(server_name: str) -> Optional[MCPSession]:
    """Legacy helper for session creation."""
    return await SessionManager().create_session(server_name)


def discover_mcp_servers() -> List[str]:
    """Legacy helper for server discovery."""
    return list(MCPServerRegistry().servers.keys())


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
    "SSEMCPServer",
    "LocalMCPServer",
    "SchemaAdapter",
    "MCPServerRegistry",
    "SessionManager",
    "adapt_tool_schema",
    "create_mcp_session",
    "discover_mcp_servers",
]
