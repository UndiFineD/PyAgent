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
Inter-Agent Communication System

This module implements Agent-to-Agent (A2A) communication patterns for multi-agent systems.
Provides structured communication protocols, agent discovery, and message routing.

Based on patterns from agentic_design_patterns repository.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable, Protocol
from enum import Enum

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of inter-agent messages."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    ERROR = "error"


class AgentCapability(Enum):
    """Standard agent capabilities."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DATA_ANALYSIS = "data_analysis"
    RESEARCH = "research"
    PLANNING = "planning"
    EXECUTION = "execution"
    VALIDATION = "validation"
    COMMUNICATION = "communication"


class AgentSkill(BaseModel):
    """Represents a specific skill an agent can perform."""
    id: str = Field(..., description="Unique skill identifier")
    name: str = Field(..., description="Human-readable skill name")
    description: str = Field(..., description="Detailed skill description")
    tags: List[str] = Field(default_factory=list, description="Skill tags for discovery")
    examples: List[str] = Field(default_factory=list, description="Example use cases")


class AgentCard(BaseModel):
    """Agent identity and capability card for A2A communication."""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    url: str = Field(..., description="Agent endpoint URL")
    version: str = Field(default="1.0.0", description="Agent version")
    default_input_modes: List[str] = Field(default_factory=lambda: ["text"], description="Supported input modes")
    default_output_modes: List[str] = Field(default_factory=lambda: ["text"], description="Supported output modes")
    capabilities: List[AgentCapability] = Field(default_factory=list, description="Agent capabilities")
    skills: List[AgentSkill] = Field(default_factory=list, description="Agent skills")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v


class AgentCapabilities(BaseModel):
    """Agent capability flags."""
    streaming: bool = Field(default=False, description="Supports streaming responses")
    async_execution: bool = Field(default=True, description="Supports async execution")
    batch_processing: bool = Field(default=False, description="Supports batch processing")


class A2AMessage(BaseModel):
    """Standard A2A message format."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique message ID")
    type: MessageType = Field(..., description="Message type")
    from_agent: str = Field(..., description="Sender agent ID")
    to_agent: Optional[str] = Field(default=None, description="Target agent ID (None for broadcasts)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Message payload")
    correlation_id: Optional[str] = Field(default=None, description="Correlation ID for request-response pairs")
    ttl: Optional[int] = Field(default=None, description="Time-to-live in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class A2AResponse(BaseModel):
    """Standard A2A response format."""
    message_id: str = Field(..., description="Original message ID")
    status: str = Field(..., description="Response status (success/error)")
    result: Any = Field(default=None, description="Response result")
    error: Optional[str] = Field(default=None, description="Error message if applicable")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentProtocol(Protocol):
    """Protocol that all agents must implement for A2A communication."""

    @property
    def agent_card(self) -> AgentCard:
        """Return the agent's identity card."""
        ...

    async def handle_message(self, message: A2AMessage) -> A2AResponse:
        """Handle incoming A2A messages."""
        ...

    async def send_message(self, message: A2AMessage) -> A2AResponse:
        """Send a message to another agent."""
        ...


class MessageRouter:
    """Routes messages between agents in the A2A network."""

    def __init__(self):
        self.agents: Dict[str, AgentProtocol] = {}
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.running = False
        self._routing_task: Optional[asyncio.Task] = None

    async def register_agent(self, agent: AgentProtocol) -> None:
        """Register an agent with the router."""
        agent_id = agent.agent_card.name
        self.agents[agent_id] = agent
        self.message_queues[agent_id] = asyncio.Queue()
        logger.info(f"Registered agent: {agent_id}")

    async def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent from the router."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.message_queues[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")

    async def route_message(self, message: A2AMessage) -> Optional[A2AResponse]:
        """Route a message to the appropriate agent."""
        if message.to_agent is None:
            # Broadcast message
            return await self._handle_broadcast(message)
        elif message.to_agent in self.agents:
            # Direct message
            return await self._handle_direct_message(message)
        else:
            # Agent not found
            logger.warning(f"Agent not found: {message.to_agent}")
            return A2AResponse(
                message_id=message.id,
                status="error",
                error=f"Agent not found: {message.to_agent}"
            )

    async def _handle_broadcast(self, message: A2AMessage) -> A2AResponse:
        """Handle broadcast messages to all agents."""
        responses = []
        for agent_id, agent in self.agents.items():
            if agent_id != message.from_agent:  # Don't send to self
                try:
                    response = await agent.handle_message(message)
                    responses.append({agent_id: response})
                except Exception as e:
                    logger.error(f"Error broadcasting to {agent_id}: {e}")
                    responses.append({agent_id: A2AResponse(
                        message_id=message.id,
                        status="error",
                        error=str(e)
                    )})

        return A2AResponse(
            message_id=message.id,
            status="success",
            result={"broadcast_responses": responses}
        )

    async def _handle_direct_message(self, message: A2AMessage) -> A2AResponse:
        """Handle direct messages to specific agents."""
        target_agent = self.agents[message.to_agent]
        try:
            response = await target_agent.handle_message(message)
            return response
        except Exception as e:
            logger.error(f"Error sending message to {message.to_agent}: {e}")
            return A2AResponse(
                message_id=message.id,
                status="error",
                error=str(e)
            )

    async def start_routing(self) -> None:
        """Start the message routing service."""
        if self.running:
            return

        self.running = True
        self._routing_task = asyncio.create_task(self._routing_loop())
        logger.info("Message routing service started")

    async def stop_routing(self) -> None:
        """Stop the message routing service."""
        self.running = False
        if self._routing_task:
            self._routing_task.cancel()
            try:
                await self._routing_task
            except asyncio.CancelledError:
                pass
        logger.info("Message routing service stopped")

    async def _routing_loop(self) -> None:
        """Main routing loop (placeholder for future enhancements)."""
        while self.running:
            await asyncio.sleep(1)  # Keep alive

    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent IDs."""
        return list(self.agents.keys())

    def get_agent_card(self, agent_id: str) -> Optional[AgentCard]:
        """Get an agent's card by ID."""
        agent = self.agents.get(agent_id)
        return agent.agent_card if agent else None


class A2ACommunicationMixin:
    """Mixin class that adds A2A communication capabilities to agents."""

    def __init__(self, agent_card: AgentCard, router: Optional[MessageRouter] = None):
        self._agent_card = agent_card
        self._router = router
        self._message_handlers: Dict[str, Callable] = {}
        self._pending_requests: Dict[str, asyncio.Future] = {}

    @property
    def agent_card(self) -> AgentCard:
        """Return the agent's identity card."""
        return self._agent_card

    async def register_with_router(self, router: MessageRouter) -> None:
        """Register this agent with a message router."""
        self._router = router
        await router.register_agent(self)

    async def send_request(
        self,
        to_agent: str,
        payload: Dict[str, Any],
        timeout: float = 30.0
    ) -> A2AResponse:
        """Send a request to another agent and wait for response."""
        if not self._router:
            raise RuntimeError("Agent not registered with a router")

        message = A2AMessage(
            type=MessageType.REQUEST,
            from_agent=self._agent_card.name,
            to_agent=to_agent,
            payload=payload
        )

        # Create a future for the response
        future = asyncio.Future()
        self._pending_requests[message.id] = future

        try:
            # Send the message
            response = await self._router.route_message(message)

            # For direct routing, the response is returned immediately
            # The pending request future is not used in this case
            if response and response.status == "success":
                # Response already received from direct routing
                pass
            else:
                # Try to wait for async response if direct routing failed
                try:
                    async_response = await asyncio.wait_for(future, timeout=timeout)
                    response = async_response
                except asyncio.TimeoutError:
                    response = response or A2AResponse(
                        message_id=message.id,
                        status="error",
                        error=f"Request timeout after {timeout} seconds"
                    )

        except asyncio.TimeoutError:
            response = A2AResponse(
                message_id=message.id,
                status="error",
                error=f"Request timeout after {timeout} seconds"
            )
        finally:
            # Clean up pending request
            self._pending_requests.pop(message.id, None)

        return response

    async def send_notification(self, to_agent: str, payload: Dict[str, Any]) -> None:
        """Send a notification to another agent (fire and forget)."""
        if not self._router:
            raise RuntimeError("Agent not registered with a router")

        message = A2AMessage(
            type=MessageType.NOTIFICATION,
            from_agent=self._agent_card.name,
            to_agent=to_agent,
            payload=payload
        )

        await self._router.route_message(message)

    async def broadcast_message(self, payload: Dict[str, Any]) -> A2AResponse:
        """Broadcast a message to all registered agents."""
        if not self._router:
            raise RuntimeError("Agent not registered with a router")

        message = A2AMessage(
            type=MessageType.BROADCAST,
            from_agent=self._agent_card.name,
            payload=payload
        )

        return await self._router.route_message(message)

    def register_message_handler(self, message_type: str, handler: Callable) -> None:
        """Register a handler for specific message types."""
        self._message_handlers[message_type] = handler

    async def handle_message(self, message: A2AMessage) -> A2AResponse:
        """Handle incoming messages (to be implemented by subclasses)."""
        try:
            # Check for registered handlers
            handler = self._message_handlers.get(message.type.value)
            if handler:
                result = await handler(message)
                return A2AResponse(
                    message_id=message.id,
                    status="success",
                    result=result
                )
            else:
                # Default handling
                return await self._default_message_handler(message)

        except Exception as e:
            logger.error(f"Error handling message {message.id}: {e}")
            return A2AResponse(
                message_id=message.id,
                status="error",
                error=str(e)
            )

    async def _default_message_handler(self, message: A2AMessage) -> A2AResponse:
        """Default message handler - override in subclasses."""
        if message.type == MessageType.REQUEST:
            return A2AResponse(
                message_id=message.id,
                status="error",
                error=f"No handler for request type: {message.payload.get('action', 'unknown')}"
            )
        else:
            # For notifications and broadcasts, just acknowledge
            return A2AResponse(
                message_id=message.id,
                status="success",
                result="Message acknowledged"
            )

    async def respond_to_request(self, original_message: A2AMessage, result: Any = None, error: str = None) -> None:
        """Send a response to a request message."""
        if not self._router:
            raise RuntimeError("Agent not registered with a router")

        response = A2AResponse(
            message_id=original_message.id,
            status="success" if error is None else "error",
            result=result,
            error=error
        )

        # Resolve pending request if this agent initiated it
        future = self._pending_requests.get(original_message.id)
        if future and not future.done():
            future.set_result(response)


# Example implementations

class SimpleA2AAgent(A2ACommunicationMixin):
    """Simple example agent that can respond to basic requests."""

    def __init__(self, name: str, description: str, capabilities: List[AgentCapability] = None):
        agent_card = AgentCard(
            name=name,
            description=description,
            url=f"http://localhost:8000/agents/{name}",
            capabilities=capabilities or []
        )
        super().__init__(agent_card)

        # Register default handlers for REQUEST messages
        self.register_message_handler(MessageType.REQUEST.value, self._handle_request)

    async def _handle_request(self, message: A2AMessage) -> Any:
        """Handle REQUEST messages by dispatching based on action."""
        action = message.payload.get("action")
        if action == "greet":
            return await self._handle_greet(message)
        elif action == "compute":
            return await self._handle_compute(message)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def _handle_greet(self, message: A2AMessage) -> str:
        """Handle greeting requests."""
        name = message.payload.get("name", "World")
        return f"Hello, {name}! I'm {self._agent_card.name}."

    async def _handle_compute(self, message: A2AMessage) -> Any:
        """Handle simple computation requests."""
        operation = message.payload.get("operation")
        a = message.payload.get("a", 0)
        b = message.payload.get("b", 0)

        if operation == "add":
            return a + b
        elif operation == "multiply":
            return a * b
        else:
            raise ValueError(f"Unknown operation: {operation}")


# Utility functions

async def create_a2a_network(agents: List[A2ACommunicationMixin]) -> MessageRouter:
    """Create and initialize an A2A communication network."""
    router = MessageRouter()

    for agent in agents:
        await agent.register_with_router(router)

    await router.start_routing()
    return router


def create_agent_card_from_dict(data: Dict[str, Any]) -> AgentCard:
    """Create an AgentCard from a dictionary."""
    return AgentCard(**data)
