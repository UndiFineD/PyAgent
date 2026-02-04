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
Tests for Inter-Agent Communication Core
"""

import pytest

from src.core.base.logic.core.inter_agent_communication_core import (
    InterAgentCommunicationCore,
    AgentCard,
    AgentCapabilities,
    Message,
    Role,
    TextPart,
)


class TestInterAgentCommunicationCore:
    """Test suite for inter-agent communication core."""

    def test_agent_card_creation(self):
        """Test agent card creation and validation."""
        card = AgentCard(
            name="TestAgent",
            description="A test agent",
            version="1.0.0",
            protocol_version="0.2.6",
            url="http://localhost:3000",
            capabilities=AgentCapabilities(
                streaming=True,
                push_notifications=True
            ),
            default_input_modes=["text"],
            default_output_modes=["text"],
        )
        assert card.name == "TestAgent"
        assert card.capabilities.streaming is True
        assert card.capabilities.push_notifications is True

    def test_message_creation(self):
        """Test message creation and serialization."""
        message = Message(
            content=[
                TextPart(text="Hello, agent!")
            ],
            role=Role.USER,
        )
        assert len(message.content) == 1
        assert isinstance(message.content[0], TextPart)
        assert message.content[0].text == "Hello, agent!"
        assert message.role == Role.USER

    @pytest.mark.asyncio
    async def test_core_initialization(self):
        """Test core initialization."""
        comm_core = InterAgentCommunicationCore()
        try:
            assert comm_core.registered_agents == {}
            assert comm_core.active_tasks == {}
            assert comm_core.message_handlers == {}
            assert comm_core.security_schemes == {}
            assert comm_core.http_client is not None
        finally:
            await comm_core.cleanup()
