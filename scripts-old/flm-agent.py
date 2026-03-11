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

"""Connect model with mcp tools in Python
# Run this python script
> pip install mcp openai
> python <this-script-path>.py
"""
from __future__ import annotations

import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Any, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI
from openai.types.chat import ResponseFormatText


class MCPClient:
    """Manages connections to multiple MCP servers and enables chatting with tools across those servers.

    This client supports multiple transport protocols (STDIO, SSE, HTTP) for connecting to MCP servers,
    maintains a registry of available tools, and orchestrates tool calls through an AI model.
    """

    def __init__(self):
        """Initialize MCPClient with empty server and tool mappings"""
        # Initialize session and client objects
        self._servers = {}
        self._tool_to_server_map = {}
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI(
            base_url="http://127.0.0.1:52625/v1/",
            api_key=os.environ.get("CUSTOM_OPENAI_API_KEY", "dummy"),
        )


    async def connect_stdio_server(
        self, server_id: str, command: str, args: list[str], env: Optional[dict[str, str]] = None
    ):
        """Connect to an MCP server using STDIO transport
        Args:
            server_id: Unique identifier for this server connection
            command: Command to run the MCP server
            args: Arguments for the command
            env: Optional environment variables
        """
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()
        # Register the server
        await self._register_server(server_id, session)


    async def connect_sse_server(self, server_id: str, url: str, headers: Optional[dict[str, str]] = None):
        """Connect to an MCP server using SSE transport

        Args:
            server_id: Unique identifier for this server connection
            url: URL of the SSE server
            headers: Optional HTTP headers

        """
        sse_context = await self.exit_stack.enter_async_context(sse_client(url=url, headers=headers))
        read, write = sse_context
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        # Register the server
        await self._register_server(server_id, session)


    async def connect_http_server(self, server_id: str, url: str, headers: Optional[dict[str, str]] = None):
        """Connect to an MCP server using HTTP transport
        Args:
            server_id: Unique identifier for this server connection
            url: URL of the HTTP server
            headers: Optional HTTP headers
        """
        http_context = await self.exit_stack.enter_async_context(streamablehttp_client(url=url, headers=headers))
        read, write, sessionId = http_context
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        # Register the server
        await self._register_server(server_id, session)


    async def _register_server(self, server_id: str, session: ClientSession):
        """Register a server and its tools in the client
        Args:
            server_id: Unique identifier for this server
            session: Connected ClientSession
        """
        # List available tools
        response = await session.list_tools()
        tools = response.tools
        # Store server connection info
        self._servers[server_id] = {
            "session": session,
            "tools": tools
        }
        # Update tool-to-server mapping
        for tool in tools:
            self._tool_to_server_map[tool.name] = server_id
        print(f"\nConnected to server '{server_id}' with tools:", [tool.name for tool in tools])


    async def chat_with_tools(self, messages: list[Any]) -> str | None:
        """Chat with model and using tools
        Args:
            messages: Messages to send to the model
        """
        if not self._servers:
            raise ValueError("No MCP servers connected. Connect to at least one server first.")
        # Collect tools from all connected servers
        available_tools = []
        for server_id, server_info in self._servers.items():
            for tool in server_info["tools"]:
                available_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    },
                })
        response_format = ResponseFormatText(type="text")
        while True:
            # Call model
            response = self.openai.chat.completions.create(
                messages=messages,
                model="qwen3-tk:4b",
                tools=available_tools,
                response_format=response_format,
                max_tokens=130000,
                extra_query={},
            )
            has_tool_call = response.choices[0].message.tool_calls
            if has_tool_call:
                for tool in has_tool_call:
                    tool_name = tool.function.name if hasattr(tool, 'function') else tool.get('function', {}).get('name')
                    tool_arguments = tool.function.arguments if hasattr(tool, 'function') else tool.get('function', {}).get('arguments')
                    tool_args = json.loads(tool_arguments)
                    messages.append({
                        "role": "assistant",
                        "tool_calls": [{
                            "id": tool.id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": tool.function.arguments,
                            }
                        }]
                    })
                    # Find the appropriate server for this tool
                    if tool_name in self._tool_to_server_map:
                        server_id = self._tool_to_server_map[tool_name]
                        server_session = self._servers[server_id]["session"]
                        # Execute tool call on the appropriate server
                        result = await server_session.call_tool(tool_name, tool_args)
                        print(f"[Server '{server_id}' call tool '{tool_name}' with args {tool_args}]: {result.content}")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool.id,
                            "content": result.content,
                        })
            else:
                messages.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })
                print(f"[Model Response]: {response.choices[0].message.content}")
                return response.choices[0].message.content


    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
        await asyncio.sleep(1)


async def main():
    """Example usage of MCPClient to connect to multiple servers and chat with tools"""
    client = MCPClient()
    messages = [
        {
            "role": "system",
            "content": " you are a helpful agent",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "hi",
                },
            ],
        },
    ]
    try:
        await client.connect_http_server(
            "TavilyMCP",
            "https://mcp.tavily.com/mcp",
            {
                "Authorization": "Bearer " + os.environ["YOUR_AUTH_TOKEN"],
            }
        )
        await client.connect_stdio_server(
            "markitdown-mm4igrov",
            "uvx",
            [
                "markitdown-mcp",
            ],
            {
            }
        )
        await client.connect_stdio_server(
            "memory-mm4ii8u0",
            "npx",
            [
                "-y",
                "@modelcontextprotocol/server-memory",
            ],
            {
                "MEMORY_FILE_PATH": os.environ["MEMORY_FILE_PATH"],
            }
        )
        await client.connect_stdio_server(
            "sequential-thinking-mm4illou",
            "npx",
            [
                "-y",
                "@modelcontextprotocol/server-sequential-thinking",
            ],
            {
            }
        )
        await client.connect_http_server(
            "MicrosoftLearnMCPserver",
            "https://learn.microsoft.com/api/mcp",
            {
            }
        )
        await client.chat_with_tools(messages)
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
