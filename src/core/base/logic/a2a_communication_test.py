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
Tests for the A2A Communication System.
"""

import asyncio
import pytest
import pytest_asyncio
from unittest.mock import Mock, AsyncMock
from src.core.base.logic.a2a_communication import (
    MessageRouter,
    A2ACommunicationMixin,
    AgentCard,
    AgentSkill,
    A2AMessage,
    A2AResponse,
    MessageType,
    AgentCapability,
    SimpleA2AAgent,
    create_a2a_network
)

class TestAgentCard:
    def test_valid_agent_card(self):
        card = AgentCard(
            name="test_agent",
            description="A test agent",
            url="http://localhost:8000/agents/test",
            capabilities=[AgentCapability.CODE_GENERATION]
        )
        assert card.name == "test_agent"
        assert card.description == "A test agent"
        assert card.version == "1.0.0"
        assert AgentCapability.CODE_GENERATION in card.capabilities
    def test_invalid_url(self):
        with pytest.raises(ValueError):
            AgentCard(
                name="test_agent",
                description="A test agent",
                url="invalid-url"
            )

class TestA2AMessage:
    def test_message_creation(self):
        message = A2AMessage(
            type=MessageType.REQUEST,
            from_agent="sender",
            to_agent="receiver",
            payload={"action": "test"}
        )
        assert message.type == MessageType.REQUEST
        assert message.from_agent == "sender"
        assert message.to_agent == "receiver"
        assert message.payload == {"action": "test"}
        assert message.id is not None
        assert message.correlation_id is None
    def test_message_with_correlation(self):
        message = A2AMessage(
            type=MessageType.RESPONSE,
            from_agent="response_agent",
            correlation_id="corr-123",
            payload={"result": "success"}
        )
        assert message.correlation_id == "corr-123"

class TestMessageRouter:
    @pytest_asyncio.fixture
    async def router(self):
        router = MessageRouter()
        yield router
        await router.stop_routing()
    @pytest.mark.asyncio
    async def test_register_agent(self, router):
        agent = Mock()
        agent.agent_card = AgentCard(
            name="test_agent",
            description="Test",
            url="http://localhost:8000"
        )
        await router.register_agent(agent)
        assert "test_agent" in router.agents
        assert "test_agent" in router.message_queues
    @pytest.mark.asyncio
    async def test_unregister_agent(self, router):
        agent = Mock()
        agent.agent_card = AgentCard(
            name="test_agent",
            description="Test",
            url="http://localhost:8000"
        )
        await router.register_agent(agent)
        await router.unregister_agent("test_agent")
        assert "test_agent" not in router.agents
        assert "test_agent" not in router.message_queues
    @pytest.mark.asyncio
    async def test_route_to_unknown_agent(self, router):
        message = A2AMessage(
            type=MessageType.REQUEST,
            from_agent="sender",
            to_agent="unknown",
            payload={"test": "data"}
        )
        response = await router.route_message(message)
        assert response.status == "error"
        assert "Agent not found" in response.error
    @pytest.mark.asyncio
    async def test_broadcast_message(self, router):
        agent1 = Mock()
        agent1.agent_card = AgentCard(name="agent1", description="Test", url="http://localhost:8001")
        agent1.handle_message = AsyncMock(return_value=A2AResponse(
            message_id="test", status="success", result="response1"
        ))
        agent2 = Mock()
        agent2.agent_card = AgentCard(name="agent2", description="Test", url="http://localhost:8002")
        agent2.handle_message = AsyncMock(return_value=A2AResponse(
            message_id="test", status="success", result="response2"
        ))
        await router.register_agent(agent1)
        await router.register_agent(agent2)
        message = A2AMessage(
            type=MessageType.BROADCAST,
            from_agent="broadcaster",
            payload={"broadcast": "test"}
        )
        response = await router.route_message(message)
        assert response.status == "success"
        assert "broadcast_responses" in response.result
        assert len(response.result["broadcast_responses"]) == 2

class TestA2ACommunicationMixin:
    @pytest.fixture
    def agent(self):
        class TestAgent(A2ACommunicationMixin):
            def __init__(self):
                card = AgentCard(
                    name="test_agent",
                    description="Test agent",
                    url="http://localhost:8000"
                )
                super().__init__(card)
        return TestAgent()
    def test_initialization(self, agent):
        assert agent._agent_card.name == "test_agent"
        assert agent._router is None
    def test_register_with_router(self, agent):
        router = MessageRouter()
        asyncio.run(agent.register_with_router(router))
        assert agent._router is router
        assert "test_agent" in router.agents
    def test_send_request_without_router(self, agent):
        with pytest.raises(RuntimeError):
            asyncio.run(agent.send_request("other_agent", {"test": "data"}))
    def test_broadcast_without_router(self, agent):
        with pytest.raises(RuntimeError):
            asyncio.run(agent.broadcast_message({"test": "data"}))

class TestSimpleA2AAgent:
    @pytest.fixture
    def agent(self):
        return SimpleA2AAgent(
            name="simple_agent",
            description="A simple test agent",
            capabilities=[AgentCapability.CODE_GENERATION]
        )
    def test_agent_creation(self, agent):
        assert agent._agent_card.name == "simple_agent"
        assert AgentCapability.CODE_GENERATION in agent._agent_card.capabilities
    def test_handle_greet(self, agent):
        message = A2AMessage(
            type=MessageType.REQUEST,
            from_agent="sender",
            to_agent="simple_agent",
            payload={"action": "greet", "name": "World"}
        )
        response = asyncio.run(agent.handle_message(message))
        assert response.status == "success"
        assert response.result == "Hello, World! I'm simple_agent."
    def test_handle_compute_add(self, agent):
        message = A2AMessage(
            type=MessageType.REQUEST,
            from_agent="sender",
            to_agent="simple_agent",
            payload={"action": "compute", "operation": "add", "a": 5, "b": 3}
        )
        response = asyncio.run(agent.handle_message(message))
        assert response.status == "success"
        assert response.result == 8
    def test_handle_unknown_action(self, agent):
        message = A2AMessage(
            type=MessageType.REQUEST,
            from_agent="sender",
            to_agent="simple_agent",
            payload={"action": "unknown"}
        )
        response = asyncio.run(agent.handle_message(message))
        assert response.status == "error"
        assert "Unknown action: unknown" in response.error
    def test_handle_notification(self, agent):
        message = A2AMessage(
            type=MessageType.NOTIFICATION,
            from_agent="sender",
            to_agent="simple_agent",
            payload={"message": "test notification"}
        )
        response = asyncio.run(agent.handle_message(message))
        assert response.status == "success"
        assert response.result == "Message acknowledged"

class TestA2ANetwork:
    @pytest.mark.asyncio
    async def test_create_network(self):
        agent1 = SimpleA2AAgent("agent1", "Agent 1")
        agent2 = SimpleA2AAgent("agent2", "Agent 2")
        router = await create_a2a_network([agent1, agent2])
        assert "agent1" in router.agents
        assert "agent2" in router.agents
        assert router.running is True
        await router.stop_routing()
    @pytest.mark.asyncio
    async def test_agent_communication(self):
        agent1 = SimpleA2AAgent("agent1", "Agent 1")
        agent2 = SimpleA2AAgent("agent2", "Agent 2")
        router = await create_a2a_network([agent1, agent2])
        response = await agent1.send_request("agent2", {"action": "greet", "name": "Agent1"})
        assert response.status == "success"
        assert "Hello, Agent1!" in response.result
        await router.stop_routing()

class TestAgentSkill:
    def test_skill_creation(self):
        skill = AgentSkill(
            id="code_gen",
            name="Code Generation",
            description="Generate code from specifications",
            tags=["coding", "ai"],
            examples=["Write a function to calculate factorial"]
        )
        assert skill.id == "code_gen"
        assert skill.name == "Code Generation"
        assert "coding" in skill.tags
        assert len(skill.examples) == 1
