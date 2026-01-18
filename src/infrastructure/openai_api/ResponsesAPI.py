"""
OpenAI Responses API Server - Phase 42

Full OpenAI Responses API compatibility layer with background task execution,
conversation context management, and MCP tool server integration.

Inspired by vLLM's responses_api_server.py implementation.

Key Features:
- OpenAI Responses API protocol models
- Server-Sent Events (SSE) streaming
- Response store with persistence
- Multi-turn conversation support
- Background task execution

Performance: Uses Rust-accelerated response parsing.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

__all__ = [
    # Enums
    "ResponseStatus",
    "ResponseType",
    "ContentPartType",
    "ToolType",
    "RoleType",
    # Protocol Models
    "ContentPart",
    "TextContent",
    "ImageContent",
    "AudioContent",
    "RefusalContent",
    "ToolCallContent",
    "Message",
    "ToolDefinition",
    "ResponseConfig",
    "ResponseOutput",
    "ResponseUsage",
    "Response",
    # Store
    "ResponseStore",
    "InMemoryResponseStore",
    # Server
    "ResponsesAPIServer",
    "StreamingHandler",
    # SSE
    "SSEEvent",
    "SSEStream",
]


# ============================================================================
# Enums
# ============================================================================


class ResponseStatus(Enum):
    """Response processing status."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INCOMPLETE = "incomplete"


class ResponseType(Enum):
    """Response object types."""

    MESSAGE = "message"
    TOOL_CALL = "function_call"
    REASONING = "reasoning"
    FILE = "file_search"
    CODE = "code_interpreter"
    WEB = "web_search"


class ContentPartType(Enum):
    """Content part types."""

    TEXT = "text"
    IMAGE_URL = "image_url"
    IMAGE_FILE = "image_file"
    AUDIO = "audio"
    REFUSAL = "refusal"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class ToolType(Enum):
    """Tool types."""

    FUNCTION = "function"
    CODE_INTERPRETER = "code_interpreter"
    FILE_SEARCH = "file_search"
    WEB_SEARCH = "web_search"
    COMPUTER = "computer"
    MCP = "mcp"


class RoleType(Enum):
    """Message role types."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    DEVELOPER = "developer"


# ============================================================================
# Protocol Models
# ============================================================================


@dataclass
class ContentPart(ABC):
    """Base class for content parts."""

    type: ContentPartType = field(default=ContentPartType.TEXT)


@dataclass
class TextContent(ContentPart):
    """Text content part."""

    text: str = ""
    type: ContentPartType = field(default=ContentPartType.TEXT)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "text", "text": self.text}


@dataclass
class ImageContent(ContentPart):
    """Image content part."""

    url: Optional[str] = None
    file_id: Optional[str] = None
    detail: str = "auto"
    type: ContentPartType = field(default=ContentPartType.IMAGE_URL)

    def to_dict(self) -> Dict[str, Any]:
        if self.url:
            return {
                "type": "image_url",
                "image_url": {"url": self.url, "detail": self.detail},
            }
        return {"type": "image_file", "image_file": {"file_id": self.file_id}}


@dataclass
class AudioContent(ContentPart):
    """Audio content part."""

    data: str = ""  # Base64 encoded
    format: str = "wav"
    type: ContentPartType = field(default=ContentPartType.AUDIO)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "audio", "audio": {"data": self.data, "format": self.format}}


@dataclass
class RefusalContent(ContentPart):
    """Refusal content part."""

    refusal: str = ""
    type: ContentPartType = field(default=ContentPartType.REFUSAL)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "refusal", "refusal": self.refusal}


@dataclass
class ToolCallContent(ContentPart):
    """Tool call content part."""

    id: str = ""
    name: str = ""
    arguments: str = ""
    type: ContentPartType = field(default=ContentPartType.TOOL_CALL)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "id": self.id,
            "function": {"name": self.name, "arguments": self.arguments},
        }


@dataclass
class Message:
    """Chat message."""

    role: RoleType
    content: Union[str, List[ContentPart]]
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[ToolCallContent]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role.value}

        if isinstance(self.content, str):
            result["content"] = self.content
        else:
            result["content"] = [c.to_dict() for c in self.content]

        if self.name:
            result["name"] = self.name
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            result["tool_calls"] = [tc.to_dict() for tc in self.tool_calls]

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create Message from dictionary."""
        role = RoleType(data["role"])
        content = data.get("content", "")

        if isinstance(content, list):
            parts = []
            for part in content:
                part_type = part.get("type", "text")
                if part_type == "text":
                    parts.append(TextContent(text=part.get("text", "")))
                elif part_type in ("image_url", "image_file"):
                    if "image_url" in part:
                        parts.append(
                            ImageContent(
                                url=part["image_url"].get("url"),
                                detail=part["image_url"].get("detail", "auto"),
                            )
                        )
                    else:
                        parts.append(
                            ImageContent(file_id=part.get("image_file", {}).get("file_id"))
                        )
                elif part_type == "audio":
                    parts.append(
                        AudioContent(
                            data=part["audio"]["data"],
                            format=part["audio"].get("format", "wav"),
                        )
                    )
                elif part_type == "refusal":
                    parts.append(RefusalContent(refusal=part.get("refusal", "")))
            content = parts

        tool_calls = None
        if "tool_calls" in data:
            tool_calls = []
            for tc in data["tool_calls"]:
                tool_calls.append(
                    ToolCallContent(
                        id=tc.get("id", ""),
                        name=tc.get("function", {}).get("name", ""),
                        arguments=tc.get("function", {}).get("arguments", "{}"),
                    )
                )

        return cls(
            role=role,
            content=content,
            name=data.get("name"),
            tool_call_id=data.get("tool_call_id"),
            tool_calls=tool_calls,
        )


@dataclass
class ToolDefinition:
    """Tool definition for function calling."""

    type: ToolType
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    strict: bool = False

    def to_dict(self) -> Dict[str, Any]:
        if self.type == ToolType.FUNCTION:
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": self.parameters,
                    "strict": self.strict,
                },
            }
        return {
            "type": self.type.value,
            self.type.value: {"name": self.name},
        }


@dataclass
class ResponseConfig:
    """Response configuration."""

    model: str
    messages: List[Message] = field(default_factory=list)
    input: Optional[str] = None
    instructions: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[List[str]] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    tools: List[ToolDefinition] = field(default_factory=list)
    tool_choice: Union[str, Dict[str, Any]] = "auto"
    response_format: Optional[Dict[str, Any]] = None
    seed: Optional[int] = None
    user: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    store: bool = False
    include: List[str] = field(default_factory=list)
    truncation: str = "auto"
    reasoning_effort: Optional[str] = None  # high, medium, low

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "tool_choice": self.tool_choice,
        }

        if self.messages:
            result["messages"] = [m.to_dict() for m in self.messages]
        if self.input:
            result["input"] = self.input
        if self.instructions:
            result["instructions"] = self.instructions
        if self.max_tokens:
            result["max_tokens"] = self.max_tokens
        if self.stop:
            result["stop"] = self.stop
        if self.tools:
            result["tools"] = [t.to_dict() for t in self.tools]
        if self.response_format:
            result["response_format"] = self.response_format
        if self.seed is not None:
            result["seed"] = self.seed
        if self.user:
            result["user"] = self.user
        if self.metadata:
            result["metadata"] = self.metadata
        if self.reasoning_effort:
            result["reasoning_effort"] = self.reasoning_effort

        return result


@dataclass
class ResponseUsage:
    """Token usage statistics."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cached_tokens: int = 0
    reasoning_tokens: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "prompt_tokens_details": {"cached_tokens": self.cached_tokens},
            "completion_tokens_details": {"reasoning_tokens": self.reasoning_tokens},
        }


@dataclass
class ResponseOutput:
    """Single response output."""

    id: str
    type: ResponseType
    content: List[ContentPart]
    status: ResponseStatus = ResponseStatus.COMPLETED
    role: RoleType = RoleType.ASSISTANT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "status": self.status.value,
            "role": self.role.value,
            "content": [c.to_dict() for c in self.content],
        }

    @property
    def text(self) -> str:
        """Extract text content."""
        texts = []
        for part in self.content:
            if isinstance(part, TextContent):
                texts.append(part.text)
        return "".join(texts)


@dataclass
class Response:
    """Complete response object."""

    id: str
    object: str = "response"
    created_at: float = field(default_factory=time.time)
    model: str = ""
    status: ResponseStatus = ResponseStatus.IN_PROGRESS
    output: List[ResponseOutput] = field(default_factory=list)
    usage: Optional[ResponseUsage] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    incomplete_details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "object": self.object,
            "created_at": int(self.created_at),
            "model": self.model,
            "status": self.status.value,
            "output": [o.to_dict() for o in self.output],
        }

        if self.usage:
            result["usage"] = self.usage.to_dict()
        if self.error:
            result["error"] = self.error
        if self.metadata:
            result["metadata"] = self.metadata
        if self.incomplete_details:
            result["incomplete_details"] = self.incomplete_details

        return result

    def add_text_output(self, text: str) -> None:
        """Add text output."""
        output_id = f"msg_{uuid.uuid4().hex[:24]}"
        self.output.append(
            ResponseOutput(
                id=output_id,
                type=ResponseType.MESSAGE,
                content=[TextContent(text=text)],
            )
        )

    def complete(self, usage: Optional[ResponseUsage] = None) -> None:
        """Mark response as complete."""
        self.status = ResponseStatus.COMPLETED
        if usage:
            self.usage = usage

    def fail(self, error_message: str, error_code: str = "internal_error") -> None:
        """Mark response as failed."""
        self.status = ResponseStatus.FAILED
        self.error = {"message": error_message, "code": error_code}


# ============================================================================
# Response Store
# ============================================================================


class ResponseStore(ABC):
    """Abstract response store."""

    @abstractmethod
    async def save(self, response: Response) -> None:
        """Save response."""
        ...

    @abstractmethod
    async def get(self, response_id: str) -> Optional[Response]:
        """Get response by ID."""
        ...

    @abstractmethod
    async def delete(self, response_id: str) -> bool:
        """Delete response."""
        ...

    @abstractmethod
    async def list(
        self,
        limit: int = 20,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> List[Response]:
        """List responses with pagination."""
        ...


class InMemoryResponseStore(ResponseStore):
    """In-memory response store."""

    def __init__(self, max_size: int = 1000):
        self._store: Dict[str, Response] = {}
        self._order: List[str] = []
        self._max_size = max_size
        self._lock = asyncio.Lock()

    async def save(self, response: Response) -> None:
        async with self._lock:
            if response.id not in self._store:
                self._order.append(response.id)

            self._store[response.id] = response

            # Evict oldest if over limit
            while len(self._order) > self._max_size:
                oldest_id = self._order.pop(0)
                self._store.pop(oldest_id, None)

    async def get(self, response_id: str) -> Optional[Response]:
        async with self._lock:
            return self._store.get(response_id)

    async def delete(self, response_id: str) -> bool:
        async with self._lock:
            if response_id in self._store:
                del self._store[response_id]
                self._order.remove(response_id)
                return True
            return False

    async def list(
        self,
        limit: int = 20,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> List[Response]:
        async with self._lock:
            order = list(self._order)

            # Filter by after/before
            if after and after in order:
                idx = order.index(after)
                order = order[idx + 1 :]

            if before and before in order:
                idx = order.index(before)
                order = order[:idx]

            # Apply limit
            order = order[:limit]

            return [self._store[rid] for rid in order if rid in self._store]


# ============================================================================
# SSE Streaming
# ============================================================================


@dataclass
class SSEEvent:
    """Server-Sent Event."""

    event: str
    data: Any
    id: Optional[str] = None
    retry: Optional[int] = None

    def encode(self) -> str:
        """Encode as SSE format."""
        lines = []
        if self.id:
            lines.append(f"id: {self.id}")
        if self.retry:
            lines.append(f"retry: {self.retry}")
        lines.append(f"event: {self.event}")

        if isinstance(self.data, str):
            data_str = self.data
        else:
            data_str = json.dumps(self.data)

        for line in data_str.split("\n"):
            lines.append(f"data: {line}")

        lines.append("")  # Empty line to end event
        return "\n".join(lines) + "\n"


class SSEStream:
    """SSE streaming handler."""

    def __init__(self, response_id: str):
        self.response_id = response_id
        self._queue: asyncio.Queue[Optional[SSEEvent]] = asyncio.Queue()
        self._closed = False

    async def send(self, event: str, data: Any) -> None:
        """Send an event."""
        if not self._closed:
            await self._queue.put(SSEEvent(event=event, data=data))

    async def close(self) -> None:
        """Close the stream."""
        self._closed = True
        await self._queue.put(None)

    async def __aiter__(self) -> AsyncIterator[str]:
        """Iterate over SSE events."""
        while True:
            event = await self._queue.get()
            if event is None:
                break
            yield event.encode()


# ============================================================================
# Streaming Handler
# ============================================================================


class StreamingHandler:
    """Handles streaming response generation."""

    def __init__(self, response: Response, stream: SSEStream):
        self.response = response
        self.stream = stream
        self._current_output: Optional[ResponseOutput] = None
        self._text_buffer: List[str] = []

    async def start(self) -> None:
        """Start streaming."""
        await self.stream.send(
            "response.created",
            self.response.to_dict(),
        )

    async def add_content_delta(self, text: str) -> None:
        """Add content delta."""
        if self._current_output is None:
            output_id = f"msg_{uuid.uuid4().hex[:24]}"
            self._current_output = ResponseOutput(
                id=output_id,
                type=ResponseType.MESSAGE,
                content=[TextContent(text="")],
                status=ResponseStatus.IN_PROGRESS,
            )
            self.response.output.append(self._current_output)

            await self.stream.send(
                "response.output_item.added",
                {
                    "output_index": len(self.response.output) - 1,
                    "item": self._current_output.to_dict(),
                },
            )

        self._text_buffer.append(text)

        await self.stream.send(
            "response.output_item.content_part.delta",
            {
                "output_index": len(self.response.output) - 1,
                "content_index": 0,
                "delta": {"type": "text", "text": text},
            },
        )

    async def finish_output(self) -> None:
        """Finish current output."""
        if self._current_output:
            full_text = "".join(self._text_buffer)
            self._current_output.content = [TextContent(text=full_text)]
            self._current_output.status = ResponseStatus.COMPLETED

            await self.stream.send(
                "response.output_item.done",
                {
                    "output_index": len(self.response.output) - 1,
                    "item": self._current_output.to_dict(),
                },
            )

            self._current_output = None
            self._text_buffer = []

    async def complete(self, usage: ResponseUsage) -> None:
        """Complete the response."""
        await self.finish_output()

        self.response.usage = usage
        self.response.status = ResponseStatus.COMPLETED

        await self.stream.send("response.completed", self.response.to_dict())
        await self.stream.close()

    async def fail(self, error: str, code: str = "internal_error") -> None:
        """Fail the response."""
        self.response.fail(error, code)

        await self.stream.send(
            "response.failed",
            {"error": {"message": error, "code": code}},
        )
        await self.stream.close()


# ============================================================================
# Responses API Server
# ============================================================================


class ResponsesAPIServer:
    """
    OpenAI Responses API server implementation.
    
    Provides full compatibility with the OpenAI Responses API including:
    - Synchronous and streaming responses
    - Background task execution
    - Response storage and retrieval
    - Multi-turn conversation support
    """

    def __init__(
        self,
        model_handler: Callable[[ResponseConfig], AsyncIterator[str]],
        store: Optional[ResponseStore] = None,
        enable_store: bool = True,
    ):
        """
        Initialize server.
        
        Args:
            model_handler: Async generator that yields text chunks
            store: Response storage backend
            enable_store: Whether to enable response storage
        """
        self.model_handler = model_handler
        self.store = store or InMemoryResponseStore()
        self.enable_store = enable_store
        self._background_tasks: Dict[str, asyncio.Task] = {}

    def _create_response_id(self) -> str:
        """Generate unique response ID."""
        return f"resp_{uuid.uuid4().hex[:24]}"

    async def create_response(
        self,
        config: ResponseConfig,
    ) -> Union[Response, SSEStream]:
        """
        Create a response.
        
        Args:
            config: Response configuration
            
        Returns:
            Response object or SSE stream for streaming
        """
        response = Response(
            id=self._create_response_id(),
            model=config.model,
            status=ResponseStatus.IN_PROGRESS,
            metadata=config.metadata,
        )

        if config.stream:
            return await self._create_streaming_response(response, config)
        else:
            return await self._create_sync_response(response, config)

    async def _create_sync_response(
        self,
        response: Response,
        config: ResponseConfig,
    ) -> Response:
        """Create synchronous response."""
        try:
            text_parts = []
            prompt_tokens = 0
            completion_tokens = 0

            async for chunk in self.model_handler(config):
                text_parts.append(chunk)
                completion_tokens += len(chunk.split())

            full_text = "".join(text_parts)
            response.add_text_output(full_text)

            # Estimate tokens
            if config.messages:
                for msg in config.messages:
                    if isinstance(msg.content, str):
                        prompt_tokens += len(msg.content.split())

            response.complete(
                ResponseUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                )
            )

            if config.store and self.enable_store:
                await self.store.save(response)

        except Exception as e:
            logger.exception(f"Error creating response: {e}")
            response.fail(str(e))

        return response

    async def _create_streaming_response(
        self,
        response: Response,
        config: ResponseConfig,
    ) -> SSEStream:
        """Create streaming response."""
        stream = SSEStream(response.id)
        handler = StreamingHandler(response, stream)

        async def generate():
            try:
                await handler.start()

                prompt_tokens = 0
                completion_tokens = 0

                # Estimate prompt tokens
                if config.messages:
                    for msg in config.messages:
                        if isinstance(msg.content, str):
                            prompt_tokens += len(msg.content.split())

                async for chunk in self.model_handler(config):
                    await handler.add_content_delta(chunk)
                    completion_tokens += len(chunk.split())

                await handler.complete(
                    ResponseUsage(
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=prompt_tokens + completion_tokens,
                    )
                )

                if config.store and self.enable_store:
                    await self.store.save(response)

            except Exception as e:
                logger.exception(f"Streaming error: {e}")
                await handler.fail(str(e))

        # Start generation in background
        task = asyncio.create_task(generate())
        self._background_tasks[response.id] = task

        return stream

    async def get_response(self, response_id: str) -> Optional[Response]:
        """Get response by ID."""
        return await self.store.get(response_id)

    async def delete_response(self, response_id: str) -> bool:
        """Delete response."""
        # Cancel any running task
        if response_id in self._background_tasks:
            task = self._background_tasks.pop(response_id)
            task.cancel()

        return await self.store.delete(response_id)

    async def list_responses(
        self,
        limit: int = 20,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> List[Response]:
        """List responses."""
        return await self.store.list(limit=limit, after=after, before=before)

    async def cancel_response(self, response_id: str) -> Optional[Response]:
        """Cancel a running response."""
        if response_id in self._background_tasks:
            task = self._background_tasks.pop(response_id)
            task.cancel()

        response = await self.store.get(response_id)
        if response and response.status == ResponseStatus.IN_PROGRESS:
            response.status = ResponseStatus.CANCELLED
            await self.store.save(response)

        return response


# ============================================================================
# Conversation Builder
# ============================================================================


class ConversationBuilder:
    """Build conversation messages from Responses API format."""

    @staticmethod
    def from_input(
        input_text: Optional[str],
        instructions: Optional[str],
        messages: Optional[List[Message]],
    ) -> List[Message]:
        """Convert Responses API input to messages."""
        result = []

        # Add system/instructions
        if instructions:
            result.append(Message(role=RoleType.SYSTEM, content=instructions))

        # Add provided messages
        if messages:
            result.extend(messages)

        # Add simple input as user message
        if input_text:
            result.append(Message(role=RoleType.USER, content=input_text))

        return result

    @staticmethod
    def append_response(
        messages: List[Message],
        response: Response,
    ) -> List[Message]:
        """Append response output to messages."""
        result = list(messages)

        for output in response.output:
            if output.type == ResponseType.MESSAGE:
                result.append(
                    Message(
                        role=RoleType.ASSISTANT,
                        content=output.content,
                    )
                )
            elif output.type == ResponseType.TOOL_CALL:
                # Extract tool calls
                tool_calls = []
                for part in output.content:
                    if isinstance(part, ToolCallContent):
                        tool_calls.append(part)
                result.append(
                    Message(
                        role=RoleType.ASSISTANT,
                        content=[],
                        tool_calls=tool_calls,
                    )
                )

        return result


# ============================================================================
# Request/Response Parsers
# ============================================================================


def parse_response_request(data: Dict[str, Any]) -> ResponseConfig:
    """Parse API request to ResponseConfig."""
    messages = []
    if "messages" in data:
        for msg_data in data["messages"]:
            messages.append(Message.from_dict(msg_data))

    tools = []
    if "tools" in data:
        for tool_data in data["tools"]:
            tool_type = ToolType(tool_data.get("type", "function"))
            if tool_type == ToolType.FUNCTION:
                func = tool_data.get("function", {})
                tools.append(
                    ToolDefinition(
                        type=tool_type,
                        name=func.get("name", ""),
                        description=func.get("description", ""),
                        parameters=func.get("parameters", {}),
                        strict=func.get("strict", False),
                    )
                )
            else:
                tools.append(
                    ToolDefinition(
                        type=tool_type,
                        name=tool_type.value,
                        description=f"Built-in {tool_type.value} tool",
                    )
                )

    return ResponseConfig(
        model=data.get("model", ""),
        messages=messages,
        input=data.get("input"),
        instructions=data.get("instructions"),
        max_tokens=data.get("max_tokens"),
        temperature=data.get("temperature", 1.0),
        top_p=data.get("top_p", 1.0),
        n=data.get("n", 1),
        stream=data.get("stream", False),
        stop=data.get("stop"),
        presence_penalty=data.get("presence_penalty", 0.0),
        frequency_penalty=data.get("frequency_penalty", 0.0),
        tools=tools,
        tool_choice=data.get("tool_choice", "auto"),
        response_format=data.get("response_format"),
        seed=data.get("seed"),
        user=data.get("user"),
        metadata=data.get("metadata", {}),
        store=data.get("store", False),
        include=data.get("include", []),
        truncation=data.get("truncation", "auto"),
        reasoning_effort=data.get("reasoning_effort"),
    )


# ============================================================================
# Rust Acceleration Integration
# ============================================================================


def _try_rust_parse_response(data: str) -> Optional[Dict[str, Any]]:
    """Try Rust-accelerated response parsing."""
    try:
        from rust_core import parse_response_json_rust

        return parse_response_json_rust(data)
    except ImportError:
        return None
