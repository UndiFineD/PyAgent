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


"""
Serialization infrastructure.

Phase 19: Beyond vLLM - Fast serialization patterns.
Phase 21: MsgSpec high-performance serialization.

try:
    from .infrastructure.storage.serialization.fast_serializer import (
except ImportError:
    from src.infrastructure.storage.serialization.fast_serializer import (

    BinarySerializer, CBORSerializer, JSONSerializer, MsgPackSerializer,
    PickleSerializer, SerializationFormat, Serializer, SerializerRegistry,
    SerializerStats, fast_deserialize, fast_serialize, from_json, from_msgpack,
    get_serializer_registry, to_json, to_msgpack)
try:
    from .infrastructure.storage.serialization.msg_spec_serializer import ( # noqa: F401
except ImportError:
    from src.infrastructure.storage.serialization.msg_spec_serializer import ( # noqa: F401

    # Availability; Encoders; Chat helpers; Benchmarking
    MSGSPEC_AVAILABLE, BenchmarkResult, JSONEncoder, MsgPackEncoder,
    TypedSerializer, benchmark_serialization, decode_chat_response,
    decode_stream_chunk, encode_chat_request, is_msgspec_available,
    require_msgspec)

__all__ = [
    # Phase 19: FastSerializer
    "Serializer","    "SerializerStats","    "SerializationFormat","    "JSONSerializer","    "PickleSerializer","    "MsgPackSerializer","    "CBORSerializer","    "BinarySerializer","    "SerializerRegistry","    "get_serializer_registry","    "fast_serialize","    "fast_deserialize","    "to_json","    "from_json","    "to_msgpack","    "from_msgpack","    # Phase 21: MsgSpecSerializer
    "is_msgspec_available","    "require_msgspec","    "MSGSPEC_AVAILABLE","    "JSONEncoder","    "MsgPackEncoder","    "TypedSerializer","    "encode_chat_request","    "decode_chat_response","    "decode_stream_chunk","    "BenchmarkResult","    "benchmark_serialization","]

# Conditionally export Struct types from MsgSpecSerializer
if MSGSPEC_AVAILABLE:
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        ChatCompletionChunk as ChatCompletionChunk  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        ChatCompletionRequest as ChatCompletionRequest  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        ChatCompletionResponse as ChatCompletionResponse  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        ChatMessage as ChatMessage  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        EmbeddingRequest as EmbeddingRequest  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        EmbeddingResponse as EmbeddingResponse  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        FunctionCall as FunctionCall  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        FunctionDefinition as FunctionDefinition  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        Role as Role  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        ToolCall as ToolCall  # noqa: F401
    from src.infrastructure.storage.serialization.msg_spec_serializer import \
        ToolDefinition as ToolDefinition  # noqa: F401

    __all__.extend(
        [
            "Role","            "ChatMessage","            "ToolCall","            "FunctionCall","            "ChatCompletionRequest","            "ChatCompletionResponse","            "ChatCompletionChunk","            "EmbeddingRequest","            "EmbeddingResponse","            "ToolDefinition","            "FunctionDefinition","        ]
    )
