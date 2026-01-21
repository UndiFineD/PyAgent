"""
Serialization infrastructure.

Phase 19: Beyond vLLM - Fast serialization patterns.
Phase 21: MsgSpec high-performance serialization.
"""
from src.infrastructure.storage.serialization.fast_serializer import (
    Serializer,
    SerializerStats,
    SerializationFormat,
    JSONSerializer,
    PickleSerializer,
    MsgPackSerializer,
    CBORSerializer,
    BinarySerializer,
    SerializerRegistry,
    get_serializer_registry,
    fast_serialize,
    fast_deserialize,
    to_json,
    from_json,
    to_msgpack,
    from_msgpack,
)

from src.infrastructure.storage.serialization.msg_spec_serializer import (
    # Availability
    is_msgspec_available,
    require_msgspec,
    MSGSPEC_AVAILABLE,

    # Encoders
    JSONEncoder,
    MsgPackEncoder,
    TypedSerializer,

    # Chat helpers
    encode_chat_request,
    decode_chat_response,
    decode_stream_chunk,

    # Benchmarking
    BenchmarkResult,
    benchmark_serialization,
)

__all__ = [
    # Phase 19: FastSerializer
    'Serializer',
    'SerializerStats',
    'SerializationFormat',
    'JSONSerializer',
    'PickleSerializer',
    'MsgPackSerializer',
    'CBORSerializer',
    'BinarySerializer',
    'SerializerRegistry',
    'get_serializer_registry',
    'fast_serialize',
    'fast_deserialize',
    'to_json',
    'from_json',
    'to_msgpack',
    'from_msgpack',

    # Phase 21: MsgSpecSerializer
    "is_msgspec_available",
    "require_msgspec",
    "MSGSPEC_AVAILABLE",
    "JSONEncoder",
    "MsgPackEncoder",
    "TypedSerializer",
    "encode_chat_request",
    "decode_chat_response",
    "decode_stream_chunk",
    "BenchmarkResult",
    "benchmark_serialization",
]

# Conditionally export Struct types from MsgSpecSerializer
if MSGSPEC_AVAILABLE:
    from src.infrastructure.storage.serialization.msg_spec_serializer import (
        Role,
        ChatMessage,
        ToolCall,
        FunctionCall,
        ChatCompletionRequest,
        ChatCompletionResponse,
        ChatCompletionChunk,
        EmbeddingRequest,
        EmbeddingResponse,
        ToolDefinition,
        FunctionDefinition,
    )

    __all__.extend([
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
    ])

