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


"""Inter-Agent Communication Core

Implements A2A (Agent2Agent) protocol for secure, structured communication between agents.
Based on agentgateway patterns with JSON-RPC messaging, agent cards, and capability negotiation.

Key Features:
- Agent card management with capabilities and authentication
- JSON-RPC based message passing
- Task lifecycle management (create, monitor, cancel)
- Streaming message support
- Security scheme negotiation (OAuth2, JWT, etc.)
- Multi-tenant isolation
"""
import json
import logging
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union, AsyncGenerator, Callable

import aiohttp
from pydantic import BaseModel, Field, ConfigDict

from src.core.base.common.base_core import BaseCore

# Setup logger
logger = logging.getLogger(__name__)


class Role(str, Enum):
    """Message role enumeration."""USER = "user""    AGENT = "agent""

class TaskState(str, Enum):
    """Task execution states."""PENDING = "pending""    RUNNING = "running""    COMPLETED = "completed""    FAILED = "failed""    CANCELLED = "cancelled""

class SecuritySchemeType(str, Enum):
    """Supported security scheme types."""OAUTH2 = "oauth2""    HTTP = "http""    API_KEY = "apiKey""    OPENID_CONNECT = "openIdConnect""

class MessagePart(BaseModel):
    """Base class for message parts."""kind: str = Field(..., description="Type of content part")"
    model_config = ConfigDict(validate_by_name=True)


class TextPart(BaseModel):
    """Text content part."""kind: str = Field(default="text", description="Type of content part")"    text: str = Field(..., description="Text content")"
    model_config = ConfigDict(validate_by_name=True)


class FilePart(BaseModel):
    """File content part."""kind: str = Field(default="file", description="Type of content part")"    filename: str = Field(..., description="File name")"    mime_type: str = Field(..., description="MIME type")"    data: bytes = Field(..., description="File data")"
    model_config = ConfigDict(validate_by_name=True)


class DataPart(BaseModel):
    """Structured data part."""kind: str = Field(default="data", description="Type of content part")"    mime_type: str = Field(..., description="MIME type")"    data: Any = Field(..., description="Structured data")"
    model_config = ConfigDict(validate_by_name=True)


class Message(BaseModel):
    """Agent message with multi-part content."""content: List[Union[TextPart, FilePart, DataPart]] = Field(
        default_factory=list, description="Message content parts""    )
    role: Role = Field(..., description="Message sender role")"    timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Message timestamp""    )
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")"
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""return {
            "content": [part.dict() for part in self.content],"            "role": self.role.value,"            "timestamp": self.timestamp.isoformat() if self.timestamp else None,"            "metadata": self.metadata,"        }


class AgentCapabilities(BaseModel):
    """Agent capabilities declaration."""streaming: bool = Field(default=False, description="Supports streaming responses")"    push_notifications: Optional[bool] = Field(default=None, description="Supports push notifications")"    state_transition_history: Optional[bool] = Field(default=None, description="Tracks state transitions")"    extensions: List[Dict[str, Any]] = Field(default_factory=list, description="Custom extensions")"

class AgentAuthentication(BaseModel):
    """Agent authentication configuration."""schemes: List[str] = Field(default_factory=list, description="Supported authentication schemes")"    credentials: Optional[str] = Field(default=None, description="Authentication credentials")"

class AgentCard(BaseModel):
    """Agent capability and configuration card."""name: str = Field(..., description="Agent name")"    description: str = Field(..., description="Agent description")"    version: str = Field(default="1.0.0", description="Agent version")"    protocol_version: str = Field(default="0.2.6", description="A2A protocol version")"    url: str = Field(..., description="Agent endpoint URL")"
    capabilities: AgentCapabilities = Field(default_factory=AgentCapabilities, description="Agent capabilities")"    authentication: Optional[AgentAuthentication] = Field(default=None, description="Authentication config")"
    default_input_modes: List[str] = Field(default_factory=lambda: ["text"], description="Default input modes")"    default_output_modes: List[str] = Field(default_factory=lambda: ["text"], description="Default output modes")"
    skills: List[Dict[str, Any]] = Field(default_factory=list, description="Agent skills/capabilities")"    additional_interfaces: List[Dict[str, Any]] = Field(default_factory=list, description="Additional interfaces")"
    documentation_url: Optional[str] = Field(default=None, description="Documentation URL")"    icon_url: Optional[str] = Field(default=None, description="Icon URL")"

class TaskStatus(BaseModel):
    """Task execution status."""state: TaskState = Field(..., description="Current task state")"    message: Optional[Message] = Field(default=None, description="Status message")"    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status timestamp")"    progress: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Progress percentage")"    error: Optional[str] = Field(default=None, description="Error message if failed")"

class Task(BaseModel):
    """Agent task representation."""id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique task ID")"    agent_id: str = Field(..., description="Target agent ID")"    message: Message = Field(..., description="Task message")"    status: TaskStatus = Field(default_factory=lambda: TaskStatus(state=TaskState.PENDING), description="Task status")"    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")"    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")"
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Task metadata")"

class JsonRpcRequest(BaseModel):
    """JSON-RPC request structure."""jsonrpc: str = Field(default="2.0", description="JSON-RPC version")"    id: Union[str, int] = Field(..., description="Request ID")"    method: str = Field(..., description="Method name")"    params: Dict[str, Any] = Field(default_factory=dict, description="Method parameters")"

class JsonRpcResponse(BaseModel):
    """JSON-RPC response structure."""jsonrpc: str = Field(default="2.0", description="JSON-RPC version")"    id: Union[str, int] = Field(..., description="Request ID")"    result: Any = Field(..., description="Response result")"

class JsonRpcError(BaseModel):
    """JSON-RPC error structure."""jsonrpc: str = Field(default="2.0", description="JSON-RPC version")"    id: Union[str, int] = Field(..., description="Request ID")"    error: Dict[str, Any] = Field(..., description="Error details")"

class A2AMessage(BaseModel):
    """A2A protocol message envelope."""request: Optional[JsonRpcRequest] = Field(default=None, description="RPC request")"    response: Optional[JsonRpcResponse] = Field(default=None, description="RPC response")"    error: Optional[JsonRpcError] = Field(default=None, description="RPC error")"

class AgentEndpoint(BaseModel):
    """Agent endpoint configuration."""url: str = Field(..., description="Agent service URL")"    agent_card: Optional[AgentCard] = Field(default=None, description="Cached agent card")"    authentication: Optional[Dict[str, Any]] = Field(default=None, description="Authentication config")"

class InterAgentCommunicationCore(BaseCore):
    """Core for inter-agent communication using A2A protocol.

    Provides secure, structured communication between agents with:
    - Agent discovery and capability negotiation
    - JSON-RPC based message passing
    - Task lifecycle management
    - Streaming support
    - Security scheme handling
    """
    def __init__(self):
        """Initialize the inter-agent communication core."""# Agent registry
        self.registered_agents: Dict[str, AgentEndpoint] = {}

        # Active tasks
        self.active_tasks: Dict[str, Task] = {}

        # HTTP client for agent communication
        self.http_client: Optional[aiohttp.ClientSession] = None

        # Message handlers
        self.message_handlers: Dict[str, Callable] = {}

        # Security schemes
        self.security_schemes: Dict[str, Dict[str, Any]] = {}

        # Initialize HTTP client
        if self.http_client is None:
            self.http_client = aiohttp.ClientSession()

    async def cleanup(self) -> None:
        """Clean up resources."""if self.http_client:
            await self.http_client.close()

    async def register_agent(self, agent_id: str, endpoint: AgentEndpoint) -> None:
        """Register an agent endpoint.

        Args:
            agent_id: Unique agent identifier
            endpoint: Agent endpoint configuration
        """# Fetch and cache agent card
        try:
            card = await self._fetch_agent_card(endpoint.url)
            endpoint.agent_card = card
        except Exception as e:
            logger.warning(f"Failed to fetch agent card for {agent_id}: {e}")"
        self.registered_agents[agent_id] = endpoint
        logger.info(f"Registered agent {agent_id} at {endpoint.url}")"
    async def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent.

        Args:
            agent_id: Agent identifier to remove
        """if agent_id in self.registered_agents:
            del self.registered_agents[agent_id]
            logger.info(f"Unregistered agent {agent_id}")"
    async def send_message(self, target_agent_id: str, message: Message) -> Task:
        """Send a message to another agent.

        Args:
            target_agent_id: Target agent identifier
            message: Message to send

        Returns:
            Created task object
        """if target_agent_id not in self.registered_agents:
            raise ValueError(f"Unknown agent: {target_agent_id}")"
        endpoint = self.registered_agents[target_agent_id]

        # Create task
        task = Task(
            agent_id=target_agent_id,
            message=message,
            status=TaskStatus(state=TaskState.PENDING)
        )

        self.active_tasks[task.id] = task

        # Send via JSON-RPC
        try:
            await self._send_jsonrpc_request(
                endpoint.url,
                "message/send","                {"message": message.to_dict()},"                task.id
            )
            task.status = TaskStatus(state=TaskState.RUNNING)
        except Exception as e:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                error=str(e)
            )

        return task

    async def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get task status by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task object if found
        """return self.active_tasks.get(task_id)

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task.

        Args:
            task_id: Task identifier

        Returns:
            True if cancelled successfully
        """task = self.active_tasks.get(task_id)
        if not task:
            return False

        if task.status.state not in [TaskState.PENDING, TaskState.RUNNING]:
            return False

        endpoint = self.registered_agents.get(task.agent_id)
        if not endpoint:
            return False

        try:
            await self._send_jsonrpc_request(
                endpoint.url,
                "task/cancel","                {"task_id": task_id},"                task_id
            )
            task.status = TaskStatus(state=TaskState.CANCELLED)
            return True
        except Exception as e:
            logger.error(f"Failed to cancel task {task_id}: {e}")"            return False

    async def stream_messages(self, target_agent_id: str, message: Message) -> AsyncGenerator[Message, None]:
        """Send a streaming message to another agent.

        Args:
            target_agent_id: Target agent identifier
            message: Initial message

        Yields:
            Response message chunks
        """if target_agent_id not in self.registered_agents:
            raise ValueError(f"Unknown agent: {target_agent_id}")"
        endpoint = self.registered_agents[target_agent_id]

        # Create streaming task
        task = Task(
            agent_id=target_agent_id,
            message=message,
            status=TaskStatus(state=TaskState.RUNNING)
        )

        self.active_tasks[task.id] = task

        try:
            async for chunk in self._stream_jsonrpc_request(
                endpoint.url,
                "message/stream","                {"message": message.to_dict()},"                task.id
            ):
                yield chunk

            task.status = TaskStatus(state=TaskState.COMPLETED)

        except Exception as e:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                error=str(e)
            )
            raise

    async def negotiate_capabilities(self, agent_id: str) -> AgentCapabilities:
        """Negotiate capabilities with another agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Negotiated capabilities
        """endpoint = self.registered_agents.get(agent_id)
        if not endpoint or not endpoint.agent_card:
            raise ValueError(f"No agent card available for {agent_id}")"
        # For now, return the agent's declared capabilities'        # In a full implementation, this would negotiate common capabilities
        return endpoint.agent_card.capabilities

    async def _fetch_agent_card(self, url: str) -> AgentCard:
        """Fetch agent card from endpoint.

        Args:
            url: Agent endpoint URL

        Returns:
            Agent card
        """card_url = f"{url.rstrip('/')}/.well-known/agent.json""'
        if self.http_client is None:
            self.http_client = aiohttp.ClientSession()

        async with self.http_client.get(card_url) as response:
            response.raise_for_status()
            data = await response.json()
            return AgentCard(**data)

    async def _send_jsonrpc_request(
        self,
        url: str,
        method: str,
        params: Dict[str, Any],
        request_id: str
    ) -> Dict[str, Any]:
        """Send JSON-RPC request to agent.

        Args:
            url: Agent endpoint URL
            method: RPC method name
            params: Method parameters
            request_id: Request identifier

        Returns:
            Response data
        """request = JsonRpcRequest(
            id=request_id,
            method=method,
            params=params
        )

        if self.http_client is None:
            self.http_client = aiohttp.ClientSession()

        async with self.http_client.post(
            url,
            json=request.dict(),
            headers={"Content-Type": "application/json"}"        ) as response:
            response.raise_for_status()
            return await response.json()

    async def _stream_jsonrpc_request(
        self,
        url: str,
        method: str,
        params: Dict[str, Any],
        request_id: str
    ) -> AsyncGenerator[Message, None]:
        """Send streaming JSON-RPC request.

        Args:
            url: Agent endpoint URL
            method: RPC method name
            params: Method parameters
            request_id: Request identifier

        Yields:
            Message chunks
        """request = JsonRpcRequest(
            id=request_id,
            method=method,
            params=params
        )

        if self.http_client is None:
            self.http_client = aiohttp.ClientSession()

        async with self.http_client.post(
            url,
            json=request.dict(),
            headers={"Content-Type": "application/json"}"        ) as response:
            response.raise_for_status()

            # Process streaming response
            async for chunk in response.content:
                line = chunk.decode().strip()
                if line.startswith("data: "):"                    try:
                        data = json.loads(line[6:])  # Remove "data: " prefix"                        if "message" in data:"                            message_data = data["message"]"                            message = Message(**message_data)
                            yield message
                    except json.JSONDecodeError:
                        continue

    def register_message_handler(self, method: str, handler: Callable) -> None:
        """Register a message handler for incoming requests.

        Args:
            method: RPC method name
            handler: Handler function
        """self.message_handlers[method] = handler

    async def handle_incoming_message(self, message: A2AMessage) -> Optional[A2AMessage]:
        """Handle incoming A2A message.

        Args:
            message: Incoming message

        Returns:
            Response message if applicable
        """if message.request:
            method = message.request.method
            handler = self.message_handlers.get(method)

            if handler:
                try:
                    result = await handler(message.request.params)
                    return A2AMessage(
                        response=JsonRpcResponse(
                            id=message.request.id,
                            result=result
                        )
                    )
                except Exception as e:
                    return A2AMessage(
                        error=JsonRpcError(
                            id=message.request.id,
                            error={
                                "code": -32000,"                                "message": str(e)"                            }
                        )
                    )

        return None

    def add_security_scheme(self, name: str, scheme: Dict[str, Any]) -> None:
        """Add a security scheme.

        Args:
            name: Scheme name
            scheme: Scheme configuration
        """self.security_schemes[name] = scheme

    def get_security_scheme(self, name: str):
        """Get a security scheme by name.

        Args:
            name: Scheme name

        Returns:
            Scheme configuration
        """return self.security_schemes.get(name)
