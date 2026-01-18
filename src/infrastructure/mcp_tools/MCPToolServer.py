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
from __future__ import annotations

import asyncio
import inspect
import hashlib
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

__all__ = [
    # Enums
    "MCPServerType",
    "ToolStatus",
    "SessionState",
    # Data Classes
    "MCPServerConfig",
    "ToolSchema",
    "ToolCall",
    "ToolResult",
    "MCPSession",
    # Main Classes
    "MCPToolServer",
    "SSEMCPServer",
    "LocalMCPServer",
    "MCPServerRegistry",
    "SchemaAdapter",
    "SessionManager",
    # Functions
    "discover_mcp_servers",
    "adapt_tool_schema",
    "create_mcp_session",
]


# ============================================================================
# Enums
# ============================================================================


class MCPServerType(Enum):
    """MCP server connection types."""

    SSE = "sse"  # Server-Sent Events
    STDIO = "stdio"  # Standard I/O
    WEBSOCKET = "websocket"
    HTTP = "http"
    LOCAL = "local"  # In-process


class ToolStatus(Enum):
    """Tool execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class SessionState(Enum):
    """MCP session state."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    READY = "ready"
    ERROR = "error"
    CLOSING = "closing"


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class MCPServerConfig:
    """MCP server configuration."""

    name: str
    server_type: MCPServerType
    url: Optional[str] = None
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: float = 30.0
    retry_attempts: int = 3
    namespace_filter: Optional[List[str]] = None
    capabilities: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "server_type": self.server_type.value,
            "url": self.url,
            "command": self.command,
            "args": self.args,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass
class ToolSchema:
    """Tool schema definition."""

    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    returns: Optional[Dict[str, Any]] = None
    namespace: Optional[str] = None
    server_name: Optional[str] = None
    is_streaming: bool = False
    is_async: bool = True

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.full_name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": self.required,
                },
            },
        }

    @property
    def full_name(self) -> str:
        """Get namespaced tool name."""
        if self.namespace:
            return f"{self.namespace}__{self.name}"
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "required": self.required,
            "namespace": self.namespace,
        }


@dataclass
class ToolCall:
    """Tool call request."""

    id: str
    name: str
    arguments: Dict[str, Any]
    server_name: Optional[str] = None
    timeout_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_openai_format(cls, data: Dict[str, Any]) -> "ToolCall":
        """Parse from OpenAI format."""
        func = data.get("function", {})
        args = func.get("arguments", "{}")
        if isinstance(args, str):
            args = json.loads(args)

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=func.get("name", ""),
            arguments=args,
        )


@dataclass
class ToolResult:
    """Tool execution result."""

    call_id: str
    name: str
    status: ToolStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI tool result format."""
        content = ""
        if self.status == ToolStatus.COMPLETED:
            if isinstance(self.result, str):
                content = self.result
            else:
                content = json.dumps(self.result)
        elif self.status == ToolStatus.FAILED:
            content = f"Error: {self.error}"

        return {
            "role": "tool",
            "tool_call_id": self.call_id,
            "content": content,
        }

    @property
    def is_success(self) -> bool:
        return self.status == ToolStatus.COMPLETED


@dataclass
class MCPSession:
    """MCP session information."""

    session_id: str
    server_name: str
    state: SessionState = SessionState.DISCONNECTED
    created_at: float = field(default_factory=time.time)
    connected_at: Optional[float] = None
    last_activity: Optional[float] = None
    tools: List[ToolSchema] = field(default_factory=list)
    capabilities: Set[str] = field(default_factory=set)
    error_message: Optional[str] = None

    @property
    def is_ready(self) -> bool:
        return self.state == SessionState.READY

    @property
    def uptime_seconds(self) -> float:
        if self.connected_at is None:
            return 0.0
        return time.time() - self.connected_at


# ============================================================================
# MCP Tool Server (Base)
# ============================================================================


class MCPToolServer(ABC):
    """
    Abstract base class for MCP tool servers.
    
    Provides unified interface for connecting to and executing
    tools on MCP-compatible servers.
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
        # Default implementation: non-streaming
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


# ============================================================================
# SSE MCP Server
# ============================================================================


class SSEMCPServer(MCPToolServer):
    """MCP server using Server-Sent Events."""

    def __init__(self, config: MCPServerConfig):
        if not config.url:
            raise ValueError("SSE server requires URL")
        super().__init__(config)
        self._client = None
        self._event_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self) -> MCPSession:
        """Connect via SSE."""
        self._session = self._create_session()

        try:
            # Initialize SSE connection
            await self._connect_sse()

            # Discover tools
            tools = await self.list_tools()
            self._session.tools = tools
            self._session.state = SessionState.READY
            self._session.connected_at = time.time()

            logger.info(
                f"Connected to SSE server {self.name} with {len(tools)} tools"
            )

        except Exception as e:
            self._session.state = SessionState.ERROR
            self._session.error_message = str(e)
            logger.error(f"Failed to connect to {self.name}: {e}")
            raise

        return self._session

    async def _connect_sse(self) -> None:
        """Establish SSE connection."""
        try:
            import aiohttp

            self._client = aiohttp.ClientSession()
            # Verify connection with a ping
            async with self._client.get(
                f"{self.config.url}/ping",
                timeout=aiohttp.ClientTimeout(total=5),
            ) as resp:
                if resp.status != 200:
                    raise ConnectionError(f"Server returned {resp.status}")
        except ImportError:
            # Fallback for testing without aiohttp
            logger.warning("aiohttp not available, using mock SSE connection")
            self._client = MockSSEClient(self.config.url)

    async def disconnect(self) -> None:
        """Disconnect SSE."""
        if self._session:
            self._session.state = SessionState.CLOSING

        if self._client:
            try:
                if hasattr(self._client, "close"):
                    await self._client.close()
            except Exception as e:
                logger.warning(f"Error closing SSE client: {e}")
            self._client = None

        if self._session:
            self._session.state = SessionState.DISCONNECTED

    async def list_tools(self) -> List[ToolSchema]:
        """List tools via SSE."""
        if not self._client:
            raise RuntimeError("Not connected")

        try:
            if hasattr(self._client, "get"):
                async with self._client.get(
                    f"{self.config.url}/tools",
                    timeout=self.config.timeout_seconds,
                ) as resp:
                    data = await resp.json()
            else:
                data = await self._client.list_tools()

            tools = []
            for tool_data in data.get("tools", []):
                schema = ToolSchema(
                    name=tool_data.get("name", ""),
                    description=tool_data.get("description", ""),
                    parameters=tool_data.get("inputSchema", {}).get("properties", {}),
                    required=tool_data.get("inputSchema", {}).get("required", []),
                    server_name=self.name,
                )
                tools.append(schema)
                self._tools[schema.name] = schema

            return self._apply_namespace_filter(tools)

        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            raise

    async def call_tool(self, call: ToolCall) -> ToolResult:
        """Execute tool via SSE."""
        if not self._client:
            raise RuntimeError("Not connected")

        start_time = time.time()

        try:
            if hasattr(self._client, "post"):
                async with self._client.post(
                    f"{self.config.url}/tools/{call.name}/call",
                    json={"arguments": call.arguments},
                    timeout=call.timeout_seconds or self.config.timeout_seconds,
                ) as resp:
                    data = await resp.json()
            else:
                data = await self._client.call_tool(call.name, call.arguments)

            duration_ms = (time.time() - start_time) * 1000

            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.COMPLETED,
                result=data.get("content"),
                duration_ms=duration_ms,
            )

        except asyncio.TimeoutError:
            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.TIMEOUT,
                error="Tool execution timed out",
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


# ============================================================================
# Local MCP Server (In-process)
# ============================================================================


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
            # Handle async handlers
            if inspect.iscoroutinefunction(handler):
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


# ============================================================================
# Mock SSE Client (for testing)
# ============================================================================


class MockSSEClient:
    """Mock SSE client for testing."""

    def __init__(self, url: str):
        self.url = url
        self._tools = [
            {
                "name": "web_search",
                "description": "Search the web",
                "inputSchema": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
            {
                "name": "code_interpreter",
                "description": "Execute Python code",
                "inputSchema": {
                    "type": "object",
                    "properties": {"code": {"type": "string"}},
                    "required": ["code"],
                },
            },
        ]

    async def list_tools(self) -> Dict[str, Any]:
        return {"tools": self._tools}

    async def call_tool(
        self,
        name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {"content": f"Mock result for {name}: {arguments}"}

    async def close(self) -> None:
        pass


# ============================================================================
# MCP Server Registry
# ============================================================================


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
        # Find server by tool name
        for server in self._servers.values():
            if server.get_tool(call.name):
                return await server.call_tool(call)

        return ToolResult(
            call_id=call.id,
            name=call.name,
            status=ToolStatus.FAILED,
            error=f"No server found for tool: {call.name}",
        )


# ============================================================================
# Schema Adapter
# ============================================================================


class SchemaAdapter:
    """Adapt tool schemas between formats."""

    @staticmethod
    def to_openai(schemas: List[ToolSchema]) -> List[Dict[str, Any]]:
        """Convert to OpenAI tool format."""
        return [s.to_openai_format() for s in schemas]

    @staticmethod
    def from_openai(tools: List[Dict[str, Any]]) -> List[ToolSchema]:
        """Convert from OpenAI tool format."""
        schemas = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                params = func.get("parameters", {})
                schemas.append(
                    ToolSchema(
                        name=func.get("name", ""),
                        description=func.get("description", ""),
                        parameters=params.get("properties", {}),
                        required=params.get("required", []),
                    )
                )
        return schemas

    @staticmethod
    def to_mcp(schemas: List[ToolSchema]) -> List[Dict[str, Any]]:
        """Convert to MCP format."""
        return [
            {
                "name": s.name,
                "description": s.description,
                "inputSchema": {
                    "type": "object",
                    "properties": s.parameters,
                    "required": s.required,
                },
            }
            for s in schemas
        ]

    @staticmethod
    def from_mcp(tools: List[Dict[str, Any]]) -> List[ToolSchema]:
        """Convert from MCP format."""
        schemas = []
        for tool in tools:
            schema = tool.get("inputSchema", {})
            schemas.append(
                ToolSchema(
                    name=tool.get("name", ""),
                    description=tool.get("description", ""),
                    parameters=schema.get("properties", {}),
                    required=schema.get("required", []),
                )
            )
        return schemas


# ============================================================================
# Session Manager
# ============================================================================


class SessionManager:
    """Manage MCP sessions."""

    def __init__(self, registry: Optional[MCPServerRegistry] = None):
        self.registry = registry or MCPServerRegistry()
        self._active_sessions: Dict[str, MCPSession] = {}

    async def create_session(
        self,
        server_name: str,
    ) -> Optional[MCPSession]:
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


# ============================================================================
# Convenience Functions
# ============================================================================


async def discover_mcp_servers(
    config_path: Optional[str] = None,
    env_prefix: str = "MCP_SERVER_",
) -> List[MCPServerConfig]:
    """
    Discover MCP servers from config or environment.
    
    Args:
        config_path: Path to MCP config file
        env_prefix: Environment variable prefix
        
    Returns:
        List of discovered server configs
    """
    import os

    configs = []

    # Check environment variables
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            name = key[len(env_prefix):].lower()
            configs.append(
                MCPServerConfig(
                    name=name,
                    server_type=MCPServerType.SSE,
                    url=value,
                )
            )

    # Load from config file
    if config_path:
        try:
            with open(config_path) as f:
                data = json.load(f)

            for server_data in data.get("mcpServers", []):
                configs.append(
                    MCPServerConfig(
                        name=server_data.get("name", ""),
                        server_type=MCPServerType(
                            server_data.get("type", "sse")
                        ),
                        url=server_data.get("url"),
                        command=server_data.get("command"),
                        args=server_data.get("args", []),
                    )
                )
        except FileNotFoundError:
            pass

    return configs


def adapt_tool_schema(
    schema: ToolSchema,
    format: str = "openai",
) -> Dict[str, Any]:
    """
    Adapt tool schema to target format.
    
    Args:
        schema: Tool schema
        format: Target format (openai, mcp)
        
    Returns:
        Schema in target format
    """
    if format == "openai":
        return schema.to_openai_format()
    elif format == "mcp":
        return SchemaAdapter.to_mcp([schema])[0]
    else:
        return schema.to_dict()


async def create_mcp_session(
    server_config: MCPServerConfig,
) -> MCPSession:
    """
    Create and connect MCP session.
    
    Args:
        server_config: Server configuration
        
    Returns:
        Connected session
    """
    if server_config.server_type == MCPServerType.SSE:
        server = SSEMCPServer(server_config)
    elif server_config.server_type == MCPServerType.LOCAL:
        server = LocalMCPServer(server_config)
    else:
        raise ValueError(f"Unsupported server type: {server_config.server_type}")

    return await server.connect()


# ============================================================================
# Rust Acceleration Integration
# ============================================================================


def _try_rust_validate_schema(schema: Dict[str, Any]) -> Optional[bool]:
    """Try Rust-accelerated schema validation."""
    try:
        from rust_core import validate_mcp_schema_rust

        return validate_mcp_schema_rust(schema)
    except ImportError:
        return None


def _try_rust_parse_tool_call(data: str) -> Optional[Dict[str, Any]]:
    """Try Rust-accelerated tool call parsing."""
    try:
        from rust_core import parse_mcp_tool_call_rust

        return parse_mcp_tool_call_rust(data)
    except ImportError:
        return None
