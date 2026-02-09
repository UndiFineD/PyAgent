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
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Union, Callable, cast
from concurrent.futures import ThreadPoolExecutor
import threading

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
    handler: Callable[..., Any]
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
        self,
        thread_id: str,
        resource_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Create a new conversation thread"""
        ...

    async def save_messages(
        self,
        messages: List[UIMessage],
        thread_id: Optional[str] = None,
        resource_id: Optional[str] = None
    ) -> None:
        """Save messages to memory"""
        ...

    async def query_messages(self, thread_id: str, resource_id: str, limit: int = 100) -> List[UIMessage]:
        """Query messages from memory"""
        ...

    async def search_similar(
        self,
        query: str,
        thread_id: Optional[str] = None,
        limit: int = 10
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

    async def create_environment(self, template: str, config: Optional[Dict[str, Any]] = None) -> str:
        """Create a new code execution environment"""
        ...

    async def execute_code(self, environment_id: str, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code in the environment"""
        ...

    async def get_file_system(self, environment_id: str) -> Any:
        """Get file system access for the environment"""
        ...

    async def destroy_environment(self, environment_id: str) -> None:
        """Destroy the code execution environment"""
        ...


class AIAgentOrchestrationCore(BaseCore):
    """
    AI Agent Orchestration Core

    Provides comprehensive AI agent orchestration capabilities including:
    - Memory management with vector storage
    - Tool integration via extensible providers
    - Streaming chat interfaces
    - Code generation and execution
    - Collaborative development workflows
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
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
                "inspired_by": "Adorable/builder.ts"
            }
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
                "capabilities": ["code_review", "debugging", "documentation"]
            }
        )

        self.agents[code_builder.name] = code_builder
        self.agents[dev_assistant.name] = dev_assistant

    def _get_code_builder_prompt(self) -> str:
        """Get the system prompt for the code builder agent"""
        return """You are an AI app builder. Create and modify applications as the user requests.

The first thing you should always do when creating a new app is change the home page to a placeholder so that the user
can see that something is happening. Then you should explore the project structure and see what has already been
provided to you to build the app. Check if there's a README_AI.md file for more instructions on how to use the template.

All of the code you will be editing is in the global /template directory.

When building a feature, build the UI for that feature first and show the user that UI using placeholder data.
Prefer building UI incrementally and in small pieces so that the user can see the results as quickly as possible.
However, don't make so many small updates that it takes way longer to create the app. It's about balance.
Build the application logic/backend logic after the UI is built. Then connect the UI to the logic.

When you need to change a file, prefer editing it rather than writing a new file in it's place.
Please make a commit after you finish a task, even if you have more to build.

Don't try and generate raster images like pngs or jpegs. That's not possible.

Try to be concise and clear in your responses. If you need to ask the user for more information, do so in a way
that is easy to understand. If you need to ask the user to try something, explain why they should try it and
what you expect to happen.

Frequently run the linting tools so you can fix issues as you go and the user doesn't have to the user doesn't
have to just stare at an error screen for a long time.

Before you ever ask the user to try something, try curling the page yourself to ensure it's not just an error page.
You shouldn't have to rely on the user to tell you when something is obviously broken.

Sometimes if the user tells you something is broken, they might be wrong. Don't be afraid to ask them to reload
the page and try again if you think the issue they're describing doesn't make sense.

It's common that users won't bother to read everything you write, so if there's something important you want
them to do, make sure to put it last and make it as big as possible.

Tips for games:
- for games that navigate via arrow keys, you likely want to set the body to overflow hidden so that the page
  doesn't scroll.
- for games that are computationally intensive to render, you should probably use canvas rather than html.
- it's good to have a way to start the game using the keyboard. it's even better if the keys that you use to
  control the game can be used to start the game. like if you use WASD to control the game, pressing W should
  start the game. this doesn't work in all scenarios, but it's a good rule of thumb.
- if you use arrow keys to navigate, generally it's good to support WASD as well.
- insure you understand the game mechanics before you start building the game. If you don't understand the game,
  ask the user to explain it to you in detail.
- make the games full screen. don't make them in a small box with a title about it or something.

NextJS tips:
- Don't forget to put "use client" at the top of all the files that need it, otherwise the page will just error.
"""

    def _get_dev_assistant_prompt(self) -> str:
        """Get the system prompt for the development assistant agent"""
        return """You are a development assistant. Help developers with coding tasks, debugging, code review, and technical guidance.

Your capabilities include:
- Code review and improvement suggestions
- Debugging assistance and problem solving
- Documentation writing and improvement
- Architecture and design guidance
- Best practices and coding standards
- Technology selection and recommendations

Always be helpful, accurate, and provide actionable advice. When reviewing code, focus on:
- Code correctness and functionality
- Performance and efficiency
- Security considerations
- Maintainability and readability
- Following established patterns and conventions

Be concise but thorough in your responses. Use examples when helpful."""

    def _get_code_builder_tools(self) -> List[ToolDefinition]:
        """Get tools for the code builder agent"""
        return [
            ToolDefinition(
                name="edit_file",
                description="Edit an existing file with patch-based changes",
                input_schema={
                    "type": "object",
                    "properties": {
                        "target_file": {"type": "string", "description": "File to edit"},
                        "instructions": {"type": "string", "description": "Edit instructions"},
                        "code_edit": {"type": "string", "description": "Code changes with context"}
                    },
                    "required": ["target_file", "instructions", "code_edit"]
                },
                handler=self._handle_file_edit
            ),
            ToolDefinition(
                name="create_file",
                description="Create a new file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path for new file"},
                        "content": {"type": "string", "description": "File content"}
                    },
                    "required": ["file_path", "content"]
                },
                handler=self._handle_file_create
            ),
            ToolDefinition(
                name="run_command",
                description="Run a terminal command",
                input_schema={
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to run"},
                        "working_directory": {"type": "string", "description": "Working directory"}
                    },
                    "required": ["command"]
                },
                handler=self._handle_run_command
            ),
            ToolDefinition(
                name="read_file",
                description="Read file contents",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "File to read"},
                        "start_line": {"type": "integer", "description": "Start line (optional)"},
                        "end_line": {"type": "integer", "description": "End line (optional)"}
                    },
                    "required": ["file_path"]
                },
                handler=self._handle_read_file
            )
        ]

    def _get_dev_assistant_tools(self) -> List[ToolDefinition]:
        """Get tools for the development assistant agent"""
        return [
            ToolDefinition(
                name="analyze_code",
                description="Analyze code for issues and improvements",
                input_schema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Code to analyze"},
                        "language": {"type": "string", "description": "Programming language"}
                    },
                    "required": ["code", "language"]
                },
                handler=self._handle_code_analysis
            ),
            ToolDefinition(
                name="search_documentation",
                description="Search for documentation and examples",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "category": {"type": "string", "description": "Documentation category"}
                    },
                    "required": ["query"]
                },
                handler=self._handle_doc_search
            )
        ]

    def _initialize_providers(self) -> None:
        """Initialize external providers"""
        # This would be configured externally in a real implementation
        pass

    async def create_conversation_thread(self, resource_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a new conversation thread"""
        thread_id = str(uuid.uuid4())

        if self.memory_provider:
            await self.memory_provider.create_thread(thread_id, resource_id, metadata or {})

        logger.info(f"Created conversation thread {thread_id} for resource {resource_id}")
        return thread_id

    async def send_message(
        self,
        agent_name: str,
        message: UIMessage,
        thread_id: Optional[str] = None,
        streaming: bool = True,
        context: Optional[CascadeContext] = None
    ) -> Union[str, StreamingContext]:
        """Send a message to an AI agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")

        agent_config = self.agents[agent_name]

        # Create thread if not provided
        actual_thread_id = thread_id
        if not actual_thread_id:
            actual_thread_id = await self.create_conversation_thread(f"agent_{agent_name}")

        # Save user message to memory
        if self.memory_provider and agent_config.memory_enabled:
            await self.memory_provider.save_messages([message], actual_thread_id, f"agent_{agent_name}")

        # Get conversation history
        conversation_history = []
        if self.memory_provider and agent_config.memory_enabled:
            conversation_history = await self.memory_provider.query_messages(
                actual_thread_id, f"agent_{agent_name}")

        # Prepare messages for AI
        messages = self._prepare_messages_for_ai(conversation_history + [message], agent_config)

        # Create streaming context if needed
        streaming_context = None
        if streaming and self.streaming_provider and agent_config.streaming_enabled:
            streaming_context = StreamingContext(session_id=str(uuid.uuid4()))
            self.streaming_contexts[streaming_context.session_id] = streaming_context

        # Generate response
        try:
            response = await self._generate_ai_response(
                agent_config,
                messages,
                streaming_context,
                context
            )

            # Save AI response to memory
            if self.memory_provider and agent_config.memory_enabled:
                ai_message = UIMessage(
                    id=str(uuid.uuid4()),
                    role="assistant",
                    parts=[MessagePart(type="text", content=response)]
                )
                await self.memory_provider.save_messages(
                    [ai_message], actual_thread_id, f"agent_{agent_name}")

            return streaming_context if streaming_context else response

        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            if streaming_context:
                streaming_context.abort_signal.set()
            raise

    async def _generate_ai_response(
        self,
        agent_config: AgentConfig,
        messages: List[Dict[str, Any]],
        streaming_context: Optional[StreamingContext] = None,
        context: Optional[CascadeContext] = None
    ) -> str:
        """Generate AI response (placeholder - would integrate with actual AI provider)"""
        # This is a placeholder implementation
        # In a real implementation, this would call an AI service like OpenAI, Anthropic, etc.

        # Simulate AI response generation
        await asyncio.sleep(0.1)  # Simulate processing time

        # For now, return a simple response
        return (
            "This is a placeholder AI response. The actual implementation would integrate with "
            "AI providers like OpenAI, Anthropic, or local models."
        )

    def _prepare_messages_for_ai(self, ui_messages: List[UIMessage], agent_config: AgentConfig) -> List[Dict[str, Any]]:
        """Convert UI messages to AI provider format"""
        messages = []

        # Add system prompt
        messages.append({
            "role": "system",
            "content": agent_config.system_prompt
        })

        # Convert UI messages
        for ui_msg in ui_messages:
            role = ui_msg.role
            if role == "tool":
                role = "assistant"

            content = ""
            for part in ui_msg.parts:
                if part.type == "text":
                    content += part.content
                # Handle other part types as needed

            messages.append({
                "role": role,
                "content": content
            })

        return messages

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[CascadeContext] = None
    ) -> Any:
        """Execute a tool"""
        if not self.tool_provider:
            raise ValueError("No tool provider configured")

        return await self.tool_provider.execute_tool(tool_name, parameters)

    async def create_development_environment(self, template: str, config: Optional[Dict[str, Any]] = None) -> str:
        """Create a development environment"""
        if not self.code_provider:
            raise ValueError("No code execution provider configured")

        return await self.code_provider.create_environment(template, config or {})

    async def execute_code_in_environment(
        self,
        environment_id: str,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """Execute code in a development environment"""
        if not self.code_provider:
            raise ValueError("No code execution provider configured")

        return await self.code_provider.execute_code(environment_id, code, language)

    async def register_agent(self, config: AgentConfig) -> None:
        """Register a new AI agent"""
        self.agents[config.name] = config
        logger.info(f"Registered agent: {config.name}")

    async def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get an agent configuration"""
        return self.agents.get(name)

    async def list_agents(self) -> List[str]:
        """List available agents"""
        return list(self.agents.keys())

    async def get_conversation_history(self, thread_id: str, resource_id: str, limit: int = 100) -> List[UIMessage]:
        """Get conversation history"""
        if not self.memory_provider:
            return []

        return await self.memory_provider.query_messages(thread_id, resource_id, limit)

    async def search_conversations(
        self,
        query: str,
        thread_id: Optional[str] = None,
        limit: int = 10
    ) -> List[UIMessage]:
        """Search conversations using semantic similarity"""
        if not self.memory_provider:
            return []

        return await self.memory_provider.search_similar(query, thread_id, limit)

    # Tool handlers (placeholders - would be implemented based on actual tools)
    async def _handle_file_edit(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file editing tool"""
        # Placeholder implementation
        return {"status": "success", "message": "File edit tool not yet implemented"}

    async def _handle_file_create(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file creation tool"""
        # Placeholder implementation
        return {"status": "success", "message": "File creation tool not yet implemented"}

    async def _handle_run_command(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle command execution tool"""
        # Placeholder implementation
        return {"status": "success", "message": "Command execution tool not yet implemented"}

    async def _handle_read_file(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file reading tool"""
        # Placeholder implementation
        return {"status": "success", "message": "File reading tool not yet implemented"}

    async def _handle_code_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle code analysis tool"""
        # Placeholder implementation
        return {"status": "success", "message": "Code analysis tool not yet implemented"}

    async def _handle_doc_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle documentation search tool"""
        # Placeholder implementation
        return {"status": "success", "message": "Documentation search tool not yet implemented"}

    # Provider setters
    def set_memory_provider(self, provider: MemoryProvider) -> None:
        """Set the memory provider"""
        self.memory_provider = provider

    def set_tool_provider(self, provider: ToolProvider) -> None:
        """Set the tool provider"""
        self.tool_provider = provider

    def set_streaming_provider(self, provider: StreamingProvider) -> None:
        """Set the streaming provider"""
        self.streaming_provider = provider

    def set_code_provider(self, provider: CodeExecutionProvider) -> None:
        """Set the code execution provider"""
        self.code_provider = provider

    async def cleanup(self) -> None:
        """Cleanup resources"""
        # Close active streams
        for context in self.streaming_contexts.values():
            context.abort_signal.set()

        # Shutdown executor
        self.executor.shutdown(wait=True)

        logger.info("AI Agent Orchestration Core cleaned up")

    # BaseCore interface implementation
    async def initialize(self, context: Optional[CascadeContext] = None) -> bool:
        """Initialize the core"""
        try:
            self._initialize_core()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize AI Agent Orchestration Core: {e}")
            return False

    async def shutdown(self, context: Optional[CascadeContext] = None) -> bool:
        """Shutdown the core"""
        try:
            await self.cleanup()
            return True
        except Exception as e:
            logger.error(f"Failed to shutdown AI Agent Orchestration Core: {e}")
            return False

    async def health_check(self, context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Health check for the core"""
        return {
            "status": "healthy" if len(self.agents) > 0 else "degraded",
            "agents_registered": len(self.agents),
            "providers_configured": {
                "memory": self.memory_provider is not None,
                "tool": self.tool_provider is not None,
                "streaming": self.streaming_provider is not None,
                "code": self.code_provider is not None
            },
            "active_streams": len(self.streaming_contexts)
        }

    async def get_metrics(self, context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Get core metrics"""
        return {
            "agents": len(self.agents),
            "conversations": 0,  # Would track actual conversation count
            "tools_executed": 0,  # Would track tool execution count
            "environments_created": 0,  # Would track environment creation count
            "uptime": 0  # Would track uptime
        }

    async def process_task(
        self,
        task_data: Dict[str, Any],
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Process a task through the orchestration core"""
        task_type = task_data.get("type", "unknown")

        if task_type == "send_message":
            agent_name = cast(str, task_data.get("agent", "code_builder"))
            message_content = cast(str, task_data.get("message", ""))
            thread_id = cast(Optional[str], task_data.get("thread_id"))

            message = UIMessage(
                id=str(uuid.uuid4()),
                role="user",
                parts=[MessagePart(type="text", content=message_content)]
            )

            response = await self.send_message(agent_name, message, thread_id, context=context)

            # Convert response to dict if it's a StreamingContext
            resp_data: Any = response
            if isinstance(response, StreamingContext):
                resp_data = {
                    "session_id": response.session_id,
                    "is_active": response.is_active
                }

            return {"response": resp_data, "thread_id": thread_id}

        elif task_type == "create_environment":
            template = cast(str, task_data.get("template", "python"))
            config = cast(Optional[Dict[str, Any]], task_data.get("config", {}))
            env_id = await self.create_development_environment(template, config)
            return {"environment_id": env_id}

        elif task_type == "execute_code":
            env_id = cast(str, task_data.get("environment_id", ""))
            code = cast(str, task_data.get("code", ""))
            language = cast(str, task_data.get("language", "python"))
            result = await self.execute_code_in_environment(env_id, code, language)
            return {"result": result}

        else:
            raise ValueError(f"Unknown task type: {task_type}")
