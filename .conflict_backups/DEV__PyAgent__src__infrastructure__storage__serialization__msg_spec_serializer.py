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

MsgSpec Serializers
====================

Phase 21: High-performance serialization using msgspec.
Provides fast JSON/MessagePack encoding/decoding with schema validation.

Features:
- 10-50x faster than stdlib json
- Automatic type coercion and validation
- Struct-based schemas for zero-copy decoding
- MessagePack binary format support
- Streaming encoder for large datasets

Dependencies:
- msgspec (0.18.0+)
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Generic, Iterator, Sequence, Type, TypeVar

try:
    from msgspec import Struct
    from msgspec import json as msgspec_json
    from msgspec import msgpack as msgspec_msgpack

    MSGSPEC_AVAILABLE = True
except ImportError:
    MSGSPEC_AVAILABLE = False


# =============================================================================
# Type Variables
# =============================================================================

T = TypeVar("T")
StructT = TypeVar("StructT", bound="Struct" if MSGSPEC_AVAILABLE else object)


# =============================================================================
# Availability Check
# =============================================================================


def is_msgspec_available() -> bool:
    """Check if msgspec is available."""
    return MSGSPEC_AVAILABLE


def require_msgspec() -> None:
    """Raise ImportError if msgspec is not available."""
    if not MSGSPEC_AVAILABLE:
        raise ImportError("msgspec is required for high-performance serialization. Install with: pip install msgspec")


# =============================================================================
# Chat Message Schemas (LM Studio Compatible)
# =============================================================================

if MSGSPEC_AVAILABLE:

    class Role(str, Enum):
        """Chat message roles."""

        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"
        TOOL = "tool"

    class ChatMessage(Struct, frozen=True, gc=False):
        """Chat message structure for LLM APIs."""

        role: Role
        content: str
        name: str | None = None
        tool_call_id: str | None = None

    class ToolCall(Struct, frozen=True):
        """Tool/function call from assistant."""

        id: str
        type: str  # "function"
        function: "FunctionCall"

    class FunctionCall(Struct, frozen=True):
        """Function call details."""

        name: str
        arguments: str  # JSON string

    class ChatCompletionRequest(Struct):
        """OpenAI-compatible chat completion request."""

        model: str
        messages: list[ChatMessage]
        temperature: float = 0.7
        max_tokens: int | None = None
        top_p: float = 1.0
        stream: bool = False
        stop: list[str] | None = None
        tools: list["ToolDefinition"] | None = None

    class ToolDefinition(Struct):
        """Tool definition for function calling."""

        type: str  # "function"
        function: "FunctionDefinition"

    class FunctionDefinition(Struct):
        """Function definition."""

        name: str
        description: str = ""
        parameters: dict[str, Any] | None = None

    class ChatChoice(Struct):
        """Single completion choice."""

        index: int
        message: ChatMessage
        finish_reason: str | None = None

    class Usage(Struct):
        """Token usage statistics."""

        prompt_tokens: int
        completion_tokens: int
        total_tokens: int

    class ChatCompletionResponse(Struct):
        """OpenAI-compatible chat completion response."""

        id: str
        object: str  # "chat.completion"
        created: int
        model: str
        choices: list[ChatChoice]
        usage: Usage | None = None

    class StreamDelta(Struct):
        """Streaming delta content."""

        role: Role | None = None
        content: str | None = None

    class StreamChoice(Struct):
        """Streaming choice."""

        index: int
        delta: StreamDelta
        finish_reason: str | None = None

    class ChatCompletionChunk(Struct):
        """Streaming chat completion chunk."""

        id: str
        object: str  # "chat.completion.chunk"
        created: int
        model: str
        choices: list[StreamChoice]

    # Embedding structures
    class EmbeddingData(Struct):
        """Single embedding result."""

        object: str  # "embedding"
        embedding: list[float]
        index: int

    class EmbeddingRequest(Struct):
        """Embedding request."""

        model: str
        input: str | list[str]

    class EmbeddingResponse(Struct):
        """Embedding response."""

        object: str  # "list"
        data: list[EmbeddingData]
        model: str
        usage: Usage


# =============================================================================
# High-Performance Encoders
# =============================================================================



class JSONEncoder:
    """
    High-performance JSON encoder using msgspec.

    Features:
    - 10-50x faster than stdlib json
    - Automatic datetime/enum handling
    - Custom type hooks
    """

    def __init__(
        self,
        *,
        enc_hook: Callable[[Any], Any] | None = None,
        _decimal_format: str = "string",
        _order: str | None = None,
    ):
        """
        Initialize JSON encoder.

        Args:
            enc_hook: Custom encoding hook for unsupported types
            _decimal_format: How to encode decimals ("string" or "number")
            _order: Key ordering ("deterministic" or None)
        """
        require_msgspec()

        self._enc_hook = enc_hook or self._default_enc_hook
        self._encoder = msgspec_json.Encoder(enc_hook=self._enc_hook)
        self._decoder = msgspec_json.Decoder()

    @staticmethod
    def _default_enc_hook(obj: Any) -> Any:
        """Default encoding hook for common types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            import base64

            return base64.b64encode(obj).decode("ascii")
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        raise TypeError(f"Cannot encode {type(obj)}")

    def encode(self, obj: Any) -> bytes:
        """Encode object to JSON bytes."""
        return self._encoder.encode(obj)

    def encode_str(self, obj: Any) -> str:
        """Encode object to JSON string."""
        return self._encoder.encode(obj).decode("utf-8")

    def decode(self, data: bytes | str, type_: Type[T] | None = None) -> T:
        """
        Decode JSON to object.

        Args:
            data: JSON bytes or string
            type_: Optional type for validation

        Returns:
            Decoded object
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if type_ is not None:
            decoder = msgspec_json.Decoder(type_)
            return decoder.decode(data)

        return self._decoder.decode(data)

    def decode_lines(self, data: bytes | str) -> Iterator[Any]:
        """Decode newline-delimited JSON."""
        if isinstance(data, str):
            data = data.encode("utf-8")

        for line in data.split(b"\n"):
            line = line.strip()
            if line:
                yield self._decoder.decode(line)



class MsgPackEncoder:
    """
    High-performance MessagePack encoder using msgspec.

    Features:
    - Binary format, smaller than JSON
    - Faster than JSON for large payloads
    - Native datetime/bytes support
    """

    def __init__(
        self,
        *,
        enc_hook: Callable[[Any], Any] | None = None,
    ):
        """Initialize MessagePack encoder."""
        require_msgspec()

        self._enc_hook = enc_hook or self._default_enc_hook
        self._encoder = msgspec_msgpack.Encoder(enc_hook=self._enc_hook)
        self._decoder = msgspec_msgpack.Decoder()

    @staticmethod
    def _default_enc_hook(obj: Any) -> Any:
        """Default encoding hook."""
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        raise TypeError(f"Cannot encode {type(obj)}")

    def encode(self, obj: Any) -> bytes:
        """Encode object to MessagePack bytes."""
        return self._encoder.encode(obj)

    def decode(self, data: bytes, type_: Type[T] | None = None) -> T:
        """
        Decode MessagePack to object.

        Args:
            data: MessagePack bytes
            type_: Optional type for validation

        Returns:
            Decoded object
        """
        if type_ is not None:
            decoder = msgspec_msgpack.Decoder(type_)
            return decoder.decode(data)

        return self._decoder.decode(data)


# =============================================================================
# Typed Serializers
# =============================================================================



class TypedSerializer(Generic[T]):
    """
    Type-safe serializer with schema validation.

    Example:
        >>> from msgspec import Struct
        >>>
        >>> class User(Struct):
        ...     name: str
        ...     age: int
        >>>
        >>> serializer = TypedSerializer(User)
        >>> data = serializer.encode(User(name="Alice", age=30))
        >>> user = serializer.decode(data)
    """

    def __init__(
        self,
        type_: Type[T],
        serialization_format: str = "json",
    ):
        """
        Initialize typed serializer.

        Args:
            type_: Schema type (Struct or standard type)
            serialization_format: Serialization format ("json" or "msgpack")
        """
        require_msgspec()

        self._type = type_
        self._format = serialization_format

        if serialization_format == "json":
            self._encoder = msgspec_json.Encoder()
            self._decoder = msgspec_json.Decoder(type_)
        elif serialization_format == "msgpack":
            self._encoder = msgspec_msgpack.Encoder()
            self._decoder = msgspec_msgpack.Decoder(type_)
        else:
            raise ValueError(f"Unknown format: {serialization_format}")

    def encode(self, obj: T) -> bytes:
        """Encode typed object."""
        return self._encoder.encode(obj)

    def decode(self, data: bytes | str) -> T:
        """Decode to typed object with validation."""
        if isinstance(data, str):
            data = data.encode("utf-8")
        return self._decoder.decode(data)

    def encode_many(self, objects: Sequence[T]) -> bytes:
        """Encode multiple objects as array."""
        return self._encoder.encode(list(objects))

    def decode_many(self, data: bytes | str) -> list[T]:
        """Decode array to typed objects."""
        if isinstance(data, str):
            data = data.encode("utf-8")

        # Create list decoder
        if self._format == "json":
            decoder = msgspec_json.Decoder(list[self._type])  # type: ignore
        else:
            decoder = msgspec_msgpack.Decoder(list[self._type])  # type: ignore

        return decoder.decode(data)


# =============================================================================
# Chat Message Helpers
# =============================================================================


def encode_chat_request(
    messages: list[dict[str, str]],
    model: str = "",
    **kwargs,
) -> bytes:
    """
    Encode chat completion request.

    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model identifier
        **kwargs: Additional options (temperature, max_tokens, etc.)

    Returns:
        JSON bytes
    """
    require_msgspec()

    # Convert to ChatMessage structs
    chat_messages = [
        ChatMessage(
            role=Role(m["role"]),
            content=m["content"],
            name=m.get("name"),
        )
        for m in messages
    ]

    request = ChatCompletionRequest(
        model=model,
        messages=chat_messages,
        temperature=kwargs.get("temperature", 0.7),
        max_tokens=kwargs.get("max_tokens"),
        top_p=kwargs.get("top_p", 1.0),
        stream=kwargs.get("stream", False),
        stop=kwargs.get("stop"),
    )

    encoder = msgspec_json.Encoder()
    return encoder.encode(request)


def decode_chat_response(data: bytes | str) -> ChatCompletionResponse:
    """
    Decode chat completion response.

    Args:
        data: JSON bytes or string

    Returns:
        ChatCompletionResponse struct
    """
    require_msgspec()

    if isinstance(data, str):
        data = data.encode("utf-8")

    decoder = msgspec_json.Decoder(ChatCompletionResponse)
    return decoder.decode(data)


def decode_stream_chunk(data: bytes | str) -> ChatCompletionChunk:
    """
    Decode streaming chat chunk.

    Args:
        data: JSON bytes or string (without "data: " prefix)

    Returns:
        ChatCompletionChunk struct
    """
    require_msgspec()

    if isinstance(data, str):
        # Handle SSE format
        if data.startswith("data: "):
            data = data[6:]
        data = data.encode("utf-8")

    decoder = msgspec_json.Decoder(ChatCompletionChunk)
    return decoder.decode(data)


# =============================================================================
# Benchmarking Utilities
# =============================================================================


@dataclass
class BenchmarkResult:
    """Serialization benchmark result."""

    format: str
    encode_time: float
    decode_time: float
    encoded_size: int
    iterations: int

    @property
    def encode_throughput(self) -> float:
        """Encodes per second."""
        return self.iterations / self.encode_time if self.encode_time > 0 else 0

    @property
    def decode_throughput(self) -> float:
        """Decodes per second."""
        return self.iterations / self.decode_time if self.decode_time > 0 else 0


def benchmark_serialization(
    data: Any,
    iterations: int = 10000,
) -> dict[str, BenchmarkResult]:
    """
    Benchmark JSON vs MessagePack serialization.

    Args:
        data: Object to serialize
        iterations: Number of iterations

    Returns:
        Dict of format -> BenchmarkResult
    """
    require_msgspec()

    results = {}

    # JSON benchmark
    json_enc = msgspec_json.Encoder()
    json_dec = msgspec_json.Decoder()

    # Encode benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        encoded = json_enc.encode(data)
    json_encode_time = time.perf_counter() - start

    # Decode benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        json_dec.decode(encoded)
    json_decode_time = time.perf_counter() - start

    results["json"] = BenchmarkResult(
        format="json",
        encode_time=json_encode_time,
        decode_time=json_decode_time,
        encoded_size=len(encoded),
        iterations=iterations,
    )

    # MessagePack benchmark
    mp_enc = msgspec_msgpack.Encoder()
    mp_dec = msgspec_msgpack.Decoder()

    start = time.perf_counter()
    for _ in range(iterations):
        encoded = mp_enc.encode(data)
    mp_encode_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(iterations):
        mp_dec.decode(encoded)
    mp_decode_time = time.perf_counter() - start

    results["msgpack"] = BenchmarkResult(
        format="msgpack",
        encode_time=mp_encode_time,
        decode_time=mp_decode_time,
        encoded_size=len(encoded),
        iterations=iterations,
    )

    return results


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Availability
    "is_msgspec_available",
    "require_msgspec",
    "MSGSPEC_AVAILABLE",
    # Encoders
    "JSONEncoder",
    "MsgPackEncoder",
    "TypedSerializer",
    # Chat helpers
    "encode_chat_request",
    "decode_chat_response",
    "decode_stream_chunk",
    # Benchmarking
    "BenchmarkResult",
    "benchmark_serialization",
]

# Conditionally export Struct types
if MSGSPEC_AVAILABLE:
    __all__.extend(
        [
            "Role",
            "ChatMessage",
            "ToolCall",
            "FunctionCall",
            "ChatCompletionRequest",
            "ChatCompletionResponse",
            "ChatCompletionChunk",
            "EmbeddingRequest",
            "EmbeddingResponse",
            "ToolDefinition",
            "FunctionDefinition",
        ]
    )
