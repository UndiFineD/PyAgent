"""
Phase 42: OpenAI Responses API Tests
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, AsyncMock


class TestResponseEnums:
    """Test response enums."""

    def test_response_status_values(self):
        """Test ResponseStatus enum values."""
        from src.infrastructure.openai_api.ResponsesAPI import ResponseStatus

        assert ResponseStatus.IN_PROGRESS.value == "in_progress"
        assert ResponseStatus.COMPLETED.value == "completed"
        assert ResponseStatus.CANCELLED.value == "cancelled"
        assert ResponseStatus.FAILED.value == "failed"

    def test_content_part_type_values(self):
        """Test ContentPartType enum values."""
        from src.infrastructure.openai_api.ResponsesAPI import ContentPartType

        assert ContentPartType.TEXT.value == "text"
        assert ContentPartType.REFUSAL.value == "refusal"
        assert ContentPartType.IMAGE_URL.value == "image_url"

    def test_role_type_values(self):
        """Test RoleType enum values."""
        from src.infrastructure.openai_api.ResponsesAPI import RoleType

        assert RoleType.SYSTEM.value == "system"
        assert RoleType.USER.value == "user"
        assert RoleType.ASSISTANT.value == "assistant"


class TestContentParts:
    """Test content part dataclasses."""

    def test_text_content_creation(self):
        """Test TextContent creation."""
        from src.infrastructure.openai_api.ResponsesAPI import TextContent

        part = TextContent(text="Hello world")
        assert part.text == "Hello world"

    def test_text_content_to_dict(self):
        """Test TextContent serialization."""
        from src.infrastructure.openai_api.ResponsesAPI import TextContent

        part = TextContent(text="Hello")
        data = part.to_dict()
        assert data["type"] == "text"
        assert data["text"] == "Hello"

    def test_refusal_content(self):
        """Test RefusalContent creation."""
        from src.infrastructure.openai_api.ResponsesAPI import RefusalContent

        part = RefusalContent(refusal="I cannot assist with that")
        assert part.refusal == "I cannot assist with that"

    def test_image_content(self):
        """Test ImageContent creation."""
        from src.infrastructure.openai_api.ResponsesAPI import ImageContent

        part = ImageContent(
            url="https://example.com/img.png",
            detail="high"
        )
        assert part.url == "https://example.com/img.png"
        assert part.detail == "high"


class TestMessage:
    """Test Message dataclass."""

    def test_message_creation(self):
        """Test creating a message."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            Message,
            RoleType,
        )

        msg = Message(
            role=RoleType.ASSISTANT,
            content="Hello!",
        )
        assert msg.role == RoleType.ASSISTANT

    def test_message_to_dict(self):
        """Test message serialization."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            Message,
            RoleType,
        )

        msg = Message(
            role=RoleType.ASSISTANT,
            content="Test",
        )
        data = msg.to_dict()
        assert data["role"] == "assistant"
        assert data["content"] == "Test"


class TestToolDefinition:
    """Test ToolDefinition dataclass."""

    def test_tool_definition_creation(self):
        """Test creating a tool definition."""
        from src.infrastructure.openai_api.ResponsesAPI import ToolDefinition, ToolType

        tool = ToolDefinition(
            type=ToolType.FUNCTION,
            name="get_weather",
            description="Get weather information",
            parameters={"type": "object", "properties": {}},
        )
        assert tool.name == "get_weather"

    def test_tool_definition_to_dict(self):
        """Test tool definition serialization."""
        from src.infrastructure.openai_api.ResponsesAPI import ToolDefinition, ToolType

        tool = ToolDefinition(
            type=ToolType.FUNCTION,
            name="search",
            description="Search the web",
            parameters={"type": "object", "properties": {}},
        )
        data = tool.to_dict()
        assert data["function"]["name"] == "search"


class TestResponse:
    """Test Response dataclass."""

    def test_response_creation(self):
        """Test creating a response."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            Response,
            ResponseStatus,
        )

        resp = Response(
            id="resp_123",
            status=ResponseStatus.COMPLETED,
        )
        assert resp.id == "resp_123"
        assert resp.status == ResponseStatus.COMPLETED

    def test_response_to_dict(self):
        """Test response serialization."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            Response,
            ResponseStatus,
        )

        resp = Response(
            id="resp_123",
            status=ResponseStatus.COMPLETED,
        )
        data = resp.to_dict()
        assert data["id"] == "resp_123"


class TestResponseConfig:
    """Test ResponseConfig dataclass."""

    def test_config_with_model(self):
        """Test configuration with model."""
        from src.infrastructure.openai_api.ResponsesAPI import ResponseConfig

        config = ResponseConfig(model="gpt-4o")
        assert config.model == "gpt-4o"

    def test_config_with_options(self):
        """Test configuration with options."""
        from src.infrastructure.openai_api.ResponsesAPI import ResponseConfig

        config = ResponseConfig(
            model="gpt-4-turbo",
            temperature=0.7,
            stream=True,
        )
        assert config.model == "gpt-4-turbo"
        assert config.stream is True


class TestSSEStream:
    """Test SSE stream implementation."""

    @pytest.mark.asyncio
    async def test_sse_stream_send_event(self):
        """Test SSE event sending."""
        from src.infrastructure.openai_api.ResponsesAPI import SSEStream

        stream = SSEStream(response_id="resp_123")
        event_data = {"type": "response.created", "response": {"id": "resp_123"}}
        await stream.send("response.created", event_data)
        
        assert not stream._closed

    @pytest.mark.asyncio
    async def test_sse_stream_close(self):
        """Test SSE stream closing."""
        from src.infrastructure.openai_api.ResponsesAPI import SSEStream

        stream = SSEStream(response_id="resp_123")
        await stream.close()
        assert stream._closed is True


class TestInMemoryResponseStore:
    """Test in-memory response storage."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        """Test storing and retrieving response."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            InMemoryResponseStore,
            Response,
            ResponseStatus,
        )

        store = InMemoryResponseStore()
        resp = Response(
            id="resp_123",
            status=ResponseStatus.COMPLETED,
        )
        await store.save(resp)
        retrieved = await store.get("resp_123")
        assert retrieved is not None
        assert retrieved.id == "resp_123"

    @pytest.mark.asyncio
    async def test_delete_response(self):
        """Test deleting response."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            InMemoryResponseStore,
            Response,
            ResponseStatus,
        )

        store = InMemoryResponseStore()
        resp = Response(
            id="resp_456",
            status=ResponseStatus.COMPLETED,
        )
        await store.save(resp)
        result = await store.delete("resp_456")
        assert result is True
        assert await store.get("resp_456") is None


class TestStreamingHandler:
    """Test streaming handler."""

    @pytest.mark.asyncio
    async def test_streaming_handler_init(self):
        """Test StreamingHandler initialization."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            StreamingHandler,
            Response,
            ResponseStatus,
            SSEStream,
        )

        response = Response(id="resp_123", status=ResponseStatus.IN_PROGRESS)
        stream = SSEStream(response_id="resp_123")
        handler = StreamingHandler(response=response, stream=stream)
        assert handler is not None
        assert handler.response == response


class TestResponsesAPIServer:
    """Test ResponsesAPI server."""

    def test_server_creation(self):
        """Test server creation with mock handler."""
        from src.infrastructure.openai_api.ResponsesAPI import ResponsesAPIServer

        mock_handler = MagicMock()
        server = ResponsesAPIServer(model_handler=mock_handler)
        assert server is not None

    def test_server_has_handler(self):
        """Test server has model handler."""
        from src.infrastructure.openai_api.ResponsesAPI import ResponsesAPIServer

        mock_handler = MagicMock()
        server = ResponsesAPIServer(model_handler=mock_handler)
        assert server.model_handler is not None


class TestConversationBuilder:
    """Test ConversationBuilder utility."""

    def test_conversation_builder_from_input(self):
        """Test building a conversation from input."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            ConversationBuilder,
            Message,
            RoleType,
        )

        messages = ConversationBuilder.from_input(
            input_text="Hello",
            instructions="You are helpful",
            messages=None,
        )
        
        assert len(messages) == 2
        assert messages[0].role == RoleType.SYSTEM
        assert messages[1].role == RoleType.USER

    def test_conversation_with_messages(self):
        """Test conversation with provided messages."""
        from src.infrastructure.openai_api.ResponsesAPI import (
            ConversationBuilder,
            Message,
            RoleType,
        )

        existing_messages = [
            Message(role=RoleType.USER, content="Hi"),
        ]
        messages = ConversationBuilder.from_input(
            input_text=None,
            instructions=None,
            messages=existing_messages,
        )
        
        assert len(messages) == 1


class TestParseResponseRequest:
    """Test parse_response_request function."""

    def test_parse_simple_request(self):
        """Test parsing simple request."""
        from src.infrastructure.openai_api.ResponsesAPI import parse_response_request

        request = {
            "model": "gpt-4",
            "input": "Hello",
        }
        result = parse_response_request(request)
        assert result is not None

    def test_parse_request_with_messages(self):
        """Test parsing request with messages."""
        from src.infrastructure.openai_api.ResponsesAPI import parse_response_request

        request = {
            "model": "gpt-4",
            "input": [
                {"role": "user", "content": "Hello"},
            ],
        }
        result = parse_response_request(request)
        assert result is not None
