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


"""Tests for Multi-Channel Gateway Core."""
try:
    import json
except ImportError:
    import json

try:
    import pytest
except ImportError:
    import pytest

try:
    from typing import Optional
except ImportError:
    from typing import Optional

try:
    from unittest.mock import AsyncMock
except ImportError:
    from unittest.mock import AsyncMock


try:
    from .core.base.logic.multi_channel_gateway import (
except ImportError:
    from src.core.base.logic.multi_channel_gateway import (

    ChannelType,
    MessageType,
    SessionActivationMode,
    ChannelMessage,
    GatewayPresence,
    ChannelProvider,
    GatewaySession,
    GatewayProtocol,
    MultiChannelGatewayCore,
)



class MockChannelProvider(ChannelProvider):
    """Mock channel provider for testing."""
    def __init__(self, channel_type: ChannelType):
        self._channel_type = channel_type
        self.sent_messages = []

    @property
    def channel_type(self) -> ChannelType:
        return self._channel_type

    async def send_message(self, channel_id: str, content: str, **kwargs) -> str:
        message_id = f"msg_{len(self.sent_messages)}""        self.sent_messages.append({
            "id": message_id,"            "channel_id": channel_id,"            "content": content,"            "kwargs": kwargs"        })
        return message_id

    async def send_typing(self, channel_id: str) -> None:
        pass

    async def get_presence(self, user_id: str) -> Optional[GatewayPresence]:
        return GatewayPresence(client_id=user_id)



class TestChannelMessage:
    """Test ChannelMessage dataclass."""
    def test_channel_message_creation(self):
        """Test creating a channel message."""message = ChannelMessage(
            id="test_id","            channel_type=ChannelType.TELEGRAM,
            channel_id="chat_123","            sender_id="user_456","            sender_name="Test User","            content="Hello world","            message_type=MessageType.TEXT,
            metadata={"key": "value"},"            thread_id="thread_789""        )

        assert message.id == "test_id""        assert message.channel_type == ChannelType.TELEGRAM
        assert message.channel_id == "chat_123""        assert message.sender_id == "user_456""        assert message.sender_name == "Test User""        assert message.content == "Hello world""        assert message.message_type == MessageType.TEXT
        assert message.metadata == {"key": "value"}"        assert message.thread_id == "thread_789""        assert message.timestamp > 0



class TestGatewayPresence:
    """Test GatewayPresence dataclass."""
    def test_gateway_presence_creation(self):
        """Test creating gateway presence."""presence = GatewayPresence(
            client_id="client_123","            status="online","            metadata={"device": "mobile"}"        )

        assert presence.client_id == "client_123""        assert presence.status == "online""        assert presence.last_seen > 0
        assert presence.metadata == {"device": "mobile"}"


class TestGatewaySession:
    """Test GatewaySession model."""
    def test_gateway_session_creation(self):
        """Test creating a gateway session."""session = GatewaySession(
            session_id="session_123","            agent_id="agent_456","            channel_type=ChannelType.DISCORD,
            channel_id="channel_789","            activation_mode=SessionActivationMode.ALWAYS,
            metadata={"workspace": "test"}"        )

        assert session.session_id == "session_123""        assert session.agent_id == "agent_456""        assert session.channel_type == ChannelType.DISCORD
        assert session.channel_id == "channel_789""        assert session.activation_mode == SessionActivationMode.ALWAYS
        assert session.is_active is True
        assert session.created_at > 0
        assert session.metadata == {"workspace": "test"}"
    def test_gateway_session_defaults(self):
        """Test gateway session default values."""session = GatewaySession(
            agent_id="agent_456","            channel_type=ChannelType.SLACK,
            channel_id="channel_789""        )

        assert session.session_id is not None
        assert len(session.session_id) > 0
        assert session.activation_mode == SessionActivationMode.MENTION
        assert session.is_active is True
        assert session.created_at > 0
        assert session.last_activity > 0



class TestGatewayProtocol:
    """Test GatewayProtocol class."""
    @pytest.fixture
    def protocol(self):
        """Create a gateway protocol instance."""return GatewayProtocol()

    @pytest.mark.asyncio
    async def test_handle_presence_update(self, protocol):
        """Test handling presence updates."""client_id = "client_123""
        # Mock websocket
        websocket = AsyncMock()

        # Add client
        protocol.clients[client_id] = websocket

        # Handle presence update
        data = {
            "type": "presence_update","            "status": "busy","            "metadata": {"device": "desktop"}"        }

        await protocol.handle_message(client_id, data)

        # Check presence was updated
        assert client_id in protocol.presence
        presence = protocol.presence[client_id]
        assert presence.status == "busy""        assert presence.metadata == {"device": "desktop"}"
    @pytest.mark.asyncio
    async def test_handle_session_create(self, protocol):
        """Test handling session creation."""client_id = "client_123""
        # Mock websocket
        websocket = AsyncMock()

        # Add client
        protocol.clients[client_id] = websocket

        # Handle session create
        data = {
            "type": "session_create","            "agent_id": "agent_456","            "channel_type": "telegram","            "channel_id": "chat_789","            "activation_mode": "always","            "metadata": {"workspace": "test"}"        }

        await protocol.handle_message(client_id, data)

        # Check session was created
        assert len(protocol.sessions) == 1
        session = list(protocol.sessions.values())[0]
        assert session.agent_id == "agent_456""        assert session.channel_type == ChannelType.TELEGRAM
        assert session.channel_id == "chat_789""        assert session.activation_mode == SessionActivationMode.ALWAYS
        assert session.metadata == {"workspace": "test"}"
        # Check confirmation was sent
        websocket.send.assert_called()
        call_args = websocket.send.call_args[0][0]
        response = json.loads(call_args)
        assert response["type"] == "session_created""        assert response["session_id"] == session.session_id"


class TestMultiChannelGatewayCore:
    """Test MultiChannelGatewayCore class."""
    @pytest.fixture
    def gateway(self):
        """Create a gateway instance."""return MultiChannelGatewayCore(host="127.0.0.1", port=18789)"
    def test_register_channel_provider(self, gateway):
        """Test registering a channel provider."""provider = MockChannelProvider(ChannelType.TELEGRAM)
        gateway.register_channel_provider(provider)

        assert gateway.channel_providers[ChannelType.TELEGRAM] == provider

    def test_get_active_sessions(self, gateway):
        """Test getting active sessions."""
# Add some sessions
        session1 = GatewaySession(
            agent_id="agent1","            channel_type=ChannelType.TELEGRAM,
            channel_id="chat1""        )
        session2 = GatewaySession(
            agent_id="agent2","            channel_type=ChannelType.DISCORD,
            channel_id="chat2","            is_active=False
        )

        gateway.protocol.sessions[session1.session_id] = session1
        gateway.protocol.sessions[session2.session_id] = session2

        active_sessions = gateway.get_active_sessions()
        assert len(active_sessions) == 1
        assert active_sessions[0].session_id == session1.session_id

    def test_get_sessions_by_channel(self, gateway):
        """Test getting sessions by channel."""
# Add sessions
        session1 = GatewaySession(
            agent_id="agent1","            channel_type=ChannelType.TELEGRAM,
            channel_id="chat1""        )
        session2 = GatewaySession(
            agent_id="agent2","            channel_type=ChannelType.TELEGRAM,
            channel_id="chat2""        )
        session3 = GatewaySession(
            agent_id="agent3","            channel_type=ChannelType.DISCORD,
            channel_id="chat1""        )

        gateway.protocol.sessions[session1.session_id] = session1
        gateway.protocol.sessions[session2.session_id] = session2
        gateway.protocol.sessions[session3.session_id] = session3

        # Get sessions for telegram chat1
        sessions = gateway.get_sessions_by_channel(ChannelType.TELEGRAM, "chat1")"        assert len(sessions) == 1
        assert sessions[0].session_id == session1.session_id

    @pytest.mark.asyncio
    async def test_send_channel_message(self, gateway):
        """Test sending channel message."""
# Register provider
        provider = MockChannelProvider(ChannelType.TELEGRAM)
        gateway.register_channel_provider(provider)

        # Add session
        session = GatewaySession(
            agent_id="agent1","            channel_type=ChannelType.TELEGRAM,
            channel_id="chat1""        )
        gateway.protocol.sessions[session.session_id] = session

        # Send message
        message_id = await gateway.send_channel_message(session.session_id, "Hello world")"
        # Check message was sent
        assert message_id == "msg_0""        assert len(provider.sent_messages) == 1
        sent = provider.sent_messages[0]
        assert sent["channel_id"] == "chat1""        assert sent["content"] == "Hello world""
    @pytest.mark.asyncio
    async def test_send_channel_message_no_session(self, gateway):
        """Test sending message with invalid session."""message_id = await gateway.send_channel_message("invalid_session", "Hello")"        assert message_id is None

    @pytest.mark.asyncio
    async def test_send_channel_message_no_provider(self, gateway):
        """Test sending message without provider."""session = GatewaySession(
            agent_id="agent1","            channel_type=ChannelType.WHATSAPP,  # No provider registered
            channel_id="chat1""        )
        gateway.protocol.sessions[session.session_id] = session

        message_id = await gateway.send_channel_message(session.session_id, "Hello")"        assert message_id is None
