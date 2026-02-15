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
Phase 42: MCP Tool Server Tests

Tests for the MCP tool server infrastructure.
"""


# Import from the package
from src.infrastructure.services.mcp import (
    LocalMCPServer,
    MCPServerConfig,
    MCPServerRegistry,
    MCPServerType,
    MCPSession,
    MCPToolServer,
    SSEMCPServer,
    SchemaAdapter,
    SessionManager,
    SessionState,
    ToolCall,
    ToolResult,
    ToolSchema,
    ToolStatus,
    adapt_tool_schema,
    create_mcp_session,
    discover_mcp_servers,
)


class TestMCPServerType:
    """Test MCPServerType enum."""

    def test_server_type_values(self):
        """Test MCPServerType enum values."""
        assert MCPServerType.LOCAL.value == "local"
        assert MCPServerType.SSE.value == "sse"
        assert MCPServerType.STDIO.value == "stdio"


class TestSessionState:
    """Test SessionState enum."""

    def test_session_state_values(self):
        """Test SessionState enum values."""
        assert SessionState.CONNECTED.value == "connected"
        assert SessionState.DISCONNECTED.value == "disconnected"
        assert SessionState.CONNECTING.value == "connecting"


class TestToolStatus:
    """Test ToolStatus enum."""

    def test_tool_status_values(self):
        """Test ToolStatus enum values."""
        assert ToolStatus.COMPLETED.value == "completed"
        assert ToolStatus.FAILED.value == "failed"
        assert ToolStatus.PENDING.value == "pending"


class TestToolSchema:
    """Test ToolSchema dataclass."""

    def test_tool_schema_creation(self):
        """Test creating ToolSchema."""
        schema = ToolSchema(
            name="search",
            description="Search for information",
        )
        assert schema.name == "search"
        assert schema.description == "Search for information"

    def test_tool_schema_with_parameters(self):
        """Test ToolSchema with parameters."""
        schema = ToolSchema(
            name="get_weather",
            description="Get weather info",
            parameters={"location": {"type": "string"}},
            required=["location"],
        )
        assert "location" in schema.parameters
        assert "location" in schema.required


class TestToolCall:
    """Test ToolCall dataclass."""

    def test_tool_call_creation(self):
        """Test creating ToolCall."""
        call = ToolCall(
            id="call_123",
            name="search",
            arguments={"query": "test"},
        )
        assert call.id == "call_123"
        assert call.name == "search"
        assert call.arguments["query"] == "test"


class TestToolResult:
    """Test ToolResult dataclass."""

    def test_tool_result_success(self):
        """Test successful ToolResult."""
        result = ToolResult(
            call_id="call_123",
            name="search",
            status=ToolStatus.COMPLETED,
            result={"data": "found"},
        )
        assert result.status == ToolStatus.COMPLETED
        assert result.result["data"] == "found"

    def test_tool_result_error(self):
        """Test error ToolResult."""
        result = ToolResult(
            call_id="call_456",
            name="search",
            status=ToolStatus.FAILED,
            error="Tool not found",
        )
        assert result.status == ToolStatus.FAILED
        assert result.error == "Tool not found"


class TestMCPSession:
    """Test MCPSession dataclass."""

    def test_mcp_session_creation(self):
        """Test creating MCPSession."""
        session = MCPSession(
            session_id="sess_123",
            server_name="local_server",
        )
        assert session.session_id == "sess_123"
        assert session.server_name == "local_server"

    def test_mcp_session_state(self):
        """Test MCPSession state."""
        session = MCPSession(
            session_id="sess_456",
            server_name="test_server",
            state=SessionState.CONNECTED,
        )
        assert session.state == SessionState.CONNECTED


class TestMCPServerConfig:
    """Test MCPServerConfig dataclass."""

    def test_server_config_creation(self):
        """Test creating MCPServerConfig."""
        config = MCPServerConfig(
            name="test_server",
            server_type=MCPServerType.LOCAL,
        )
        assert config.name == "test_server"


class TestSchemaAdapter:
    """Test SchemaAdapter class."""

    def test_schema_adapter_creation(self):
        """Test creating SchemaAdapter."""
        adapter = SchemaAdapter()
        assert adapter is not None


class TestSessionManager:
    """Test SessionManager class."""

    def test_session_manager_creation(self):
        """Test creating SessionManager."""
        manager = SessionManager()
        assert manager is not None


class TestMCPServerRegistry:
    """Test MCPServerRegistry class."""

    def test_registry_creation(self):
        """Test creating MCPServerRegistry."""
        registry = MCPServerRegistry()
        assert registry is not None


class TestLocalMCPServer:
    """Test LocalMCPServer class."""

    def test_local_server_creation(self):
        """Test creating LocalMCPServer."""
        config = MCPServerConfig(name="test_local", server_type=MCPServerType.LOCAL)
        server = LocalMCPServer(config=config)
        assert server is not None


class TestSSEMCPServer:
    """Test SSEMCPServer class."""

    def test_sse_server_creation(self):
        """Test creating SSEMCPServer."""
        config = MCPServerConfig(
            name="test_sse",
            server_type=MCPServerType.SSE,
            url="http://localhost:8080",
        )
        server = SSEMCPServer(config=config)
        assert server is not None


class TestMCPToolServer:
    """Test MCPToolServer abstract class."""

    def test_mcp_tool_server_exists(self):
        """Test MCPToolServer class exists."""
        assert MCPToolServer is not None


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_adapt_tool_schema_exists(self):
        """Test adapt_tool_schema function exists."""
        assert callable(adapt_tool_schema)

    def test_create_mcp_session_exists(self):
        """Test create_mcp_session function exists."""
        assert callable(create_mcp_session)

    def test_discover_mcp_servers_exists(self):
        """Test discover_mcp_servers function exists."""
        assert callable(discover_mcp_servers)
