#!/usr/bin/env python3

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
Base MCP tool server abstraction.
"""


from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, List, Optional

from .models import (MCPServerConfig, MCPSession, SessionState, ToolCall,
                     ToolResult, ToolSchema)

logger = logging.getLogger(__name__)




class MCPToolServer(ABC):
        Abstract base class for MCP tool servers.
    
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
        """Connect to the server.        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the server.        ...

    @abstractmethod
    async def list_tools(self) -> List[ToolSchema]:
        """List available tools.        ...

    @abstractmethod
    async def call_tool(self, call: ToolCall) -> ToolResult:
        """Execute a tool call.        ...

    async def call_tool_streaming(
        self,
        call: ToolCall,
    ) -> AsyncIterator[str]:
        """Execute a tool call with streaming output.        result = await self.call_tool(call)
        if result.is_success:
            yield str(result.result)

    def get_tool(self, name: str) -> Optional[ToolSchema]:
        """Get tool by name.        return self._tools.get(name)

    def _apply_namespace_filter(self, tools: List[ToolSchema]) -> List[ToolSchema]:
        """Apply namespace filter to tools.        if not self.config.namespace_filter:
            return tools

        return [t for t in tools if t.namespace is None or t.namespace in self.config.namespace_filter]

    def _create_session(self) -> MCPSession:
        """Create a new session.        return MCPSession(
            session_id=str(uuid.uuid4()),
            server_name=self.name,
            state=SessionState.CONNECTING,
        )
