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
"""
SSE-based MCP tool server implementation.
"""

"""
import asyncio
import logging
import time
from typing import List

from .base import MCPToolServer
from .models import (MCPServerConfig, MCPSession, SessionState, ToolCall,
                     ToolResult, ToolSchema, ToolStatus)

logger = logging.getLogger(__name__)



class SSEMCPServer(MCPToolServer):
"""
MCP server using Server-Sent Events.
    def __init__(self, config: MCPServerConfig):
        if not config.url:
            raise ValueError("SSE server requires URL")"        super().__init__(config)
        self._client = None
        self._event_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self) -> MCPSession:
"""
Connect via SSE.        self._session = self._create_session()

        try:
            await self._connect_sse()
            tools = await self.list_tools()
            self._session.tools = tools
            self._session.state = SessionState.READY
            self._session.connected_at = time.time()
            logger.info(f"Connected to SSE server {self.name} with {len(tools)} tools")"        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self._session.state = SessionState.ERROR
            self._session.error_message = str(e)
            logger.error(f"Failed to connect to {self.name}: {e}")"            raise

        return self._session

    async def _connect_sse(self) -> None:
"""
Establish SSE connection.        try:
            import aiohttp

            self._client = aiohttp.ClientSession()
            async with self._client.get(
                f"{self.config.url}/ping","                timeout=aiohttp.ClientTimeout(total=5),
            ) as resp:
                if resp.status != 200:
                    raise ConnectionError(f"Server returned {resp.status}")"        except ImportError:
            logger.warning("aiohttp not available, using mock SSE connection")"            self._client = MockSSEClient(self.config.url)

    async def disconnect(self) -> None:
"""
Disconnect SSE.        if self._session:
            self._session.state = SessionState.CLOSING

        if self._client:
            try:
                if hasattr(self._client, "close"):"                    await self._client.close()
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Error closing SSE client: {e}")"            self._client = None

        if self._session:
            self._session.state = SessionState.DISCONNECTED

    async def list_tools(self) -> List[ToolSchema]:
"""
List tools via SSE.        if not self._client:
            raise RuntimeError("Not connected")
        try:
            if hasattr(self._client, "get"):"                async with self._client.get(
                    f"{self.config.url}/tools","                    timeout=self.config.timeout_seconds,
                ) as resp:
                    data = await resp.json()
            else:
                data = await self._client.list_tools()

            tools = []
            for tool_data in data.get("tools", []):"                schema = ToolSchema(
                    name=tool_data.get("name", ""),"                    description=tool_data.get("description", ""),"                    parameters=tool_data.get("inputSchema", {}).get("properties", {}),"                    required=tool_data.get("inputSchema", {}).get("required", []),"                    server_name=self.name,
                )
                tools.append(schema)
                self._tools[schema.name] = schema

            return self._apply_namespace_filter(tools)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to list tools: {e}")"            raise

    async def call_tool(self, call: ToolCall) -> ToolResult:
"""
Execute tool via SSE.        if not self._client:
            raise RuntimeError("Not connected")
        start_time = time.time()
        try:
            if hasattr(self._client, "post"):"                async with self._client.post(
                    f"{self.config.url}/tools/{call.name}/call","                    json={"arguments": call.arguments},"                    timeout=call.timeout_seconds or self.config.timeout_seconds,
                ) as resp:
                    data = await resp.json()
            else:
                data = await self._client.call_tool(call.name, call.arguments)

            duration_ms = (time.time() - start_time) * 1000
            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.COMPLETED,
                result=data.get("content"),"                duration_ms=duration_ms,
            )
        except asyncio.TimeoutError:
            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.TIMEOUT,
                error="Tool execution timed out","                duration_ms=(time.time() - start_time) * 1000,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return ToolResult(
                call_id=call.id,
                name=call.name,
                status=ToolStatus.FAILED,
                error=str(e),
                duration_ms=(time.time() - start_time) * 1000,
            )



class MockSSEClient:
"""
Mock SSE client for testing.
    def __init__(self, url: str):
        self.url = url
        self._tools = [
            {
                "name": "web_search","                "description": "Search the web","                "inputSchema": {"                    "type": "object","                    "properties": {"query": {"type": "string"}},"                    "required": ["query"],"                },
            },
            {
                "name": "code_interpreter","                "description": "Execute Python code","                "inputSchema": {"                    "type": "object","                    "properties": {"code": {"type": "string"}},"                    "required": ["code"],"                },
            },
        ]

    async def list_tools(self) -> dict:
        return {"tools": self._tools}
    async def call_tool(self, name: str, arguments: dict) -> dict:
        return {"content": f"Mock result for {name}: {arguments}"}
    async def close(self) -> None:
        pass
