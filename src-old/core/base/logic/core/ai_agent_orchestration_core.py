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

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/ai_agent_orchestration_core.description.md

# ai_agent_orchestration_core

**File**: `src\\core\base\\logic\\core\ai_agent_orchestration_core.py`  
**Type**: Python Module  
**Summary**: 11 classes, 0 functions, 20 imports  
**Lines**: 721  
**Complexity**: 13 (moderate)

## Overview

AI Agent Orchestration Core

This core implements AI-powered app building patterns inspired by the Adorable repository.
It provides comprehensive AI agent orchestration with memory management, tool integration,
streaming chat interfaces, and collaborative development workflows.

Key Features:
- Mastra-inspired agent orchestration framework
- Vector-based memory management for conversation threading
- MCP (Model Context Protocol) tool integration
- Streaming chat with resumable conversations
- Code generation and patch-based editing workflows
- Sandboxed development environments
- Git-based version control for project state
- Real-time collaborative development support

## Classes (11)

### `MessagePart`

Represents a part of a message (text, image, file, etc.)

### `UIMessage`

UI message format compatible with AI SDK

### `ConversationThread`

Represents a conversation thread with memory

### `ToolDefinition`

MCP-compatible tool definition

### `AgentConfig`

Configuration for an AI agent

### `StreamingContext`

Context for streaming responses

### `MemoryProvider`

**Inherits from**: Protocol

Protocol for memory storage providers

### `ToolProvider`

**Inherits from**: Protocol

Protocol for tool execution providers

### `StreamingProvider`

**Inherits from**: Protocol

Protocol for streaming response providers

### `CodeExecutionProvider`

**Inherits from**: Protocol

Protocol for code execution environments

### `AIAgentOrchestrationCore`

**Inherits from**: BaseCore

AI Agent Orchestration Core

Provides comprehensive AI agent orchestration capabilities including:
- Memory management with vector storage
- Tool integration via extensible providers
- Streaming chat interfaces
- Code generation and execution
- Collaborative development workflows

**Methods** (13):
- `__init__(self, config)`
- `_initialize_core(self)`
- `_register_default_agents(self)`
- `_get_code_builder_prompt(self)`
- `_get_dev_assistant_prompt(self)`
- `_get_code_builder_tools(self)`
- `_get_dev_assistant_tools(self)`
- `_initialize_providers(self)`
- `_prepare_messages_for_ai(self, ui_messages, agent_config)`
- `set_memory_provider(self, provider)`
- ... and 3 more methods

## Dependencies

**Imports** (20):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.state.agent_state_manager.StateTransaction`
- `threading`
- `typing.Any`
- `typing.Dict`
- ... and 5 more

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/ai_agent_orchestration_core.improvements.md

# Improvements for ai_agent_orchestration_core

**File**: `src\\core\base\\logic\\core\ai_agent_orchestration_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 721 lines (large)  
**Complexity**: 13 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ai_agent_orchestration_core_test.py` with pytest tests

### Code Organization
- [TIP] **11 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (721 lines) - Consider refactoring

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
AI Agent Orchestration Core

This core implements AI-powered app building patterns inspired by the Adorable repository.
It provides comprehensive AI agent orchestration with memory management, tool integration,
streaming chat interfaces, and collaborative development workflows.

Key Features:
- Mastra-inspired agent orchestration framework
- Vector-based memory management for conversation threading
- MCP (Model Context Protocol) tool integration
- Streaming chat with resumable conversations
- Code generation and patch-based editing workflows
- Sandboxed development environments
- Git-based version control for project state
- Real-time collaborative development support
"""

import asyncio
import logging
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Union

from src.core.base.common.base_core import BaseCore
from src.core.base.common.models.communication_models import CascadeContext

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class MessagePart:
    """Represents a part of a message (text, image, file, etc.)"""

    type: str  # "text", "image", "file", etc.
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UIMessage:
    """UI message format compatible with AI SDK"""

    id: str
    role: str  # "user", "assistant", "system", "tool"
    parts: List[MessagePart]
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationThread:
    """Represents a conversation thread with memory"""

    thread_id: str
    resource_id: str
    messages: List[UIMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ToolDefinition:
    """MCP-compatible tool definition"""

    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: callable
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentConfig:
    """Configuration for an AI agent"""

    name: str
    system_prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: List[ToolDefinition] = field(default_factory=list)
    memory_enabled: bool = True
    streaming_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamingContext:
    """Context for streaming responses"""

    session_id: str
    is_active: bool = False
    abort_signal: threading.Event = field(default_factory=threading.Event)
    keep_alive_timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemoryProvider(Protocol):
    """Protocol for memory storage providers"""

    async def create_thread(
        self, thread_id: str, resource_id: str, metadata: Dict[str, Any] = None
    ) -> None:
        """Create a new conversation thread"""
        ...

    async def save_messages(
        self, messages: List[UIMessage], thread_id: str = None, resource_id: str = None
    ) -> None:
        """Save messages to memory"""
        ...

    async def query_messages(
        self, thread_id: str, resource_id: str, limit: int = 100
    ) -> List[UIMessage]:
        """Query messages from memory"""
        ...

    async def search_similar(
        self, query: str, thread_id: str = None, limit: int = 10
    ) -> List[UIMessage]:
        """Search for similar messages using vector similarity"""
        ...


class ToolProvider(Protocol):
    """Protocol for tool execution providers"""

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool with given parameters"""
        ...

    async def get_available_tools(self) -> List[ToolDefinition]:
        """Get list of available tools"""
        ...

    async def register_tool(self, tool: ToolDefinition) -> None:
        """Register a new tool"""
        ...


class StreamingProvider(Protocol):
    """Protocol for streaming response providers"""

    async def create_stream(self, context: StreamingContext) -> Any:
        """Create a new streaming context"""
        ...

    async def send_chunk(self, context: StreamingContext, chunk: str) -> None:
        """Send a chunk of data through the stream"""
        ...

    async def close_stream(self, context: StreamingContext) -> None:
        """Close the streaming context"""
        ...

    async def resume_stream(self, session_id: str) -> StreamingContext:
        """Resume an existing stream"""
        ...


class CodeExecutionProvider(Protocol):
    """Protocol for code execution environments"""

    async def create_environment(
        self, template: str, config: Dict[str, Any] = None
    ) -> str:
        """Create a new code execution environment"""
        ...

    async def execute_code(
        self, environment_id: str, code: str, language: str = "python"
    ) -> Dict[str, Any]:
        """Execute code in the environment"""
        ...

    async def get_file_system(self, environment_id: str) -> Any:
        """Get file system access for the environment"""
        ...

    async def destroy_environment(self, environment_id: str) -> None:
        """Destroy the code execution environment"""
        ...


class AIAgentOrchestrationCore(BaseCore):
    """AI Agent Orchestration Core

    Provides comprehensive AI agent orchestration capabilities including:
    - Memory management with vector storage
    - Tool integration via extensible providers
    - Streaming chat interfaces
    - Code generation and execution
    - Collaborative development workflows
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config or {})

        # Core components
        self.memory_provider: Optional[MemoryProvider] = None
        self.tool_provider: Optional[ToolProvider] = None
        self.streaming_provider: Optional[StreamingProvider] = None
        self.code_provider: Optional[CodeExecutionProvider] = None

        # Agent registry
        self.agents: Dict[str, AgentConfig] = {}

        # Active streaming contexts
        self.streaming_contexts: Dict[str, StreamingContext] = {}

        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Initialize core
        self._initialize_core()

    def _initialize_core(self) -> None:
        """Initialize the core components"""
        logger.info("Initializing AI Agent Orchestration Core")

        # Register default agents
        self._register_default_agents()

        # Initialize providers (will be set by external configuration)
        self._initialize_providers()

    def _register_default_agents(self) -> None:
        """Register default AI agents"""
        # Code Builder Agent (inspired by Adorable's builder agent)
        code_builder = AgentConfig(
            name="code_builder",
            system_prompt=self._get_code_builder_prompt(),
            model="gpt-4-turbo",
            temperature=0.1,
            tools=self._get_code_builder_tools(),
            memory_enabled=True,
            streaming_enabled=True,
            metadata={
                "purpose": "AI-powered code generation and editing",
                "inspired_by": "Adorable/builder.ts",
            },
        )

        # Development Assistant Agent
        dev_assistant = AgentConfig(
            name="dev_assistant",
            system_prompt=self._get_dev_assistant_prompt(),
            model="gpt-4",
            temperature=0.7,
            tools=self._get_dev_assistant_tools(),
            memory_enabled=True,
            streaming_enabled=True,
            metadata={
                "purpose": "General development assistance and guidance",
                "capabilities": ["code_review", "debugging", "documentation"],
            },
        )

        self.agents[code_builder.name] = code_builder
        self.agents[dev_assistant.name] = dev_assistant

    def _get_code_builder_prompt(self) -> str:
        """Get the system prompt for the code builder agent"""
        return """You are an AI app builder. Create and modify applications as the user requests.

The first thing you should always do when creating a new app is change the home page to a placeholder so that the user can see that something is happening. Then you should explore the project structure and see what has already been provided to you to build the app. Check if there's a README_AI.md file for more instructions on how to use the template.

All of the code you will be editing is in the global /template directory.

When building a feature, build the UI for that feature first and show the user that UI using placeholder data. Prefer building UI incrementally and in small pieces so that the user can see the results as quickly as possible. However, don't make so many small updates that it takes way longer to create the app. It's about balance. Build the application logic/backend logic after the UI is built. Then connect the UI to the logic.

When you need to change a file, prefer editing it rather than writing a new file in it's place. Please make a commit after you finish a task, even if you have more to build.

Don't try and generate raster images like pngs or jpegs. That's not possible.

Try to be concise and clear in your responses. If you need to ask the user for more information, do so in a way that is easy to understand. If you need to ask the user to try something, explain why they should try it and what you expect to happen.

Frequently run the linting tools so you can fix issues as you go and the user doesn't have to the user doesn't have to just stare at an error screen for a long time.

Before you ever ask the user to try something, try curling the page yourself to ensure it's not just an error page. You shouldn't have to rely on the user to tell you when something is obviously broken.

Sometimes if the user tells you something is broken, they might be wrong. Don't be afraid to ask them to reload the page and try again if you think the issue they're describing doesn't make sense.

It's common that users won't bother to read everything you write, so if there's something important you want them to do, make sure to put it last and make it as big as possible.

Tips for games:
- for games that navigate via arrow keys, you likely want to set the body to overflow hidden so that the page doesn't scroll.
- for games that are computationally intensive to render, you should probably use canvas rather than html.
- it's good to have a way to start the game using the keyboard. it's even better if the keys that you use to control the game can be used to start the game. like if you use WASD to control the game, pressing W should start the game. this doesn't work in all scenarios, but it's a good rule of thumb.
- if you use arrow keys to navigate, generally it's good to support WASD as well.
- insure you understand the game mechanics before you start building the game. If you don't understand the game, ask the user to explain it to you in detail.
- make the games full screen. don't make them in a small box with a title about it or something.

NextJS tips:
- Don't forget to put "use client" at the top of all the files that need it, otherwise the page will just error.
"""
    def _get_dev_assistant_prompt(self) -> str:
        """
        """
