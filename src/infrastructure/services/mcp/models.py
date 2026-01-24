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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
MCP-related data models and enums.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


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
