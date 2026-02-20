#!/usr/bin/env python3
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Model Context Protocol (MCP) Tool Integration.
"""

try:
    from .adapter import SchemaAdapter  # noqa: F401
except ImportError:
    from .adapter import SchemaAdapter # noqa: F401

try:
    from .base import MCPToolServer  # noqa: F401
except ImportError:
    from .base import MCPToolServer # noqa: F401

try:
    from .local import LocalMCPServer  # noqa: F401
except ImportError:
    from .local import LocalMCPServer # noqa: F401

try:
    from .mcp_tool_server import (adapt_tool_schema, create_mcp_session,  # noqa: F401
except ImportError:
    from .mcp_tool_server import (adapt_tool_schema, create_mcp_session, # noqa: F401

                              discover_mcp_servers)
try:
    from .models import (MCPServerConfig, MCPServerType, MCPSession, SessionState,  # noqa: F401
except ImportError:
    from .models import (MCPServerConfig, MCPServerType, MCPSession, SessionState, # noqa: F401

                     ToolCall, ToolResult, ToolSchema, ToolStatus)
try:
    from .registry import MCPServerRegistry, SessionManager  # noqa: F401
except ImportError:
    from .registry import MCPServerRegistry, SessionManager # noqa: F401

try:
    from .sse import SSEMCPServer  # noqa: F401
except ImportError:
    from .sse import SSEMCPServer # noqa: F401


__all__ = [
    "MCPServerConfig","    "MCPServerType","    "ToolSchema","    "ToolCall","    "ToolResult","    "ToolStatus","    "SessionState","    "MCPSession","    "MCPToolServer","    "SSEMCPServer","    "LocalMCPServer","    "SchemaAdapter","    "MCPServerRegistry","    "SessionManager","    "adapt_tool_schema","    "create_mcp_session","    "discover_mcp_servers","]
