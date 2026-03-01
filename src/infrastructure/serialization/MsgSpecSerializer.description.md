# MsgSpecSerializer

**File**: `src\infrastructure\serialization\MsgSpecSerializer.py`  
**Type**: Python Module  
**Summary**: 20 classes, 6 functions, 22 imports  
**Lines**: 622  
**Complexity**: 23 (complex)

## Overview

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

## Classes (20)

### `JSONEncoder`

High-performance JSON encoder using msgspec.

Features:
- 10-50x faster than stdlib json
- Automatic datetime/enum handling
- Custom type hooks

**Methods** (6):
- `__init__(self)`
- `_default_enc_hook(obj)`
- `encode(self, obj)`
- `encode_str(self, obj)`
- `decode(self, data, type_)`
- `decode_lines(self, data)`

### `MsgPackEncoder`

High-performance MessagePack encoder using msgspec.

Features:
- Binary format, smaller than JSON
- Faster than JSON for large payloads
- Native datetime/bytes support

**Methods** (4):
- `__init__(self)`
- `_default_enc_hook(obj)`
- `encode(self, obj)`
- `decode(self, data, type_)`

### `TypedSerializer`

**Inherits from**: Unknown

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

**Methods** (5):
- `__init__(self, type_, format)`
- `encode(self, obj)`
- `decode(self, data)`
- `encode_many(self, objects)`
- `decode_many(self, data)`

### `BenchmarkResult`

Serialization benchmark result.

**Methods** (2):
- `encode_throughput(self)`
- `decode_throughput(self)`

### `Role`

**Inherits from**: str, Enum

Chat message roles.

### `ChatMessage`

**Inherits from**: Struct

Chat message structure for LLM APIs.

### `ToolCall`

**Inherits from**: Struct

Tool/function call from assistant.

### `FunctionCall`

**Inherits from**: Struct

Function call details.

### `ChatCompletionRequest`

**Inherits from**: Struct

OpenAI-compatible chat completion request.

### `ToolDefinition`

**Inherits from**: Struct

Tool definition for function calling.

### `FunctionDefinition`

**Inherits from**: Struct

Function definition.

### `ChatChoice`

**Inherits from**: Struct

Single completion choice.

### `Usage`

**Inherits from**: Struct

Token usage statistics.

### `ChatCompletionResponse`

**Inherits from**: Struct

OpenAI-compatible chat completion response.

### `StreamDelta`

**Inherits from**: Struct

Streaming delta content.

### `StreamChoice`

**Inherits from**: Struct

Streaming choice.

### `ChatCompletionChunk`

**Inherits from**: Struct

Streaming chat completion chunk.

### `EmbeddingData`

**Inherits from**: Struct

Single embedding result.

### `EmbeddingRequest`

**Inherits from**: Struct

Embedding request.

### `EmbeddingResponse`

**Inherits from**: Struct

Embedding response.

## Functions (6)

### `is_msgspec_available()`

Check if msgspec is available.

### `require_msgspec()`

Raise ImportError if msgspec is not available.

### `encode_chat_request(messages, model)`

Encode chat completion request.

Args:
    messages: List of message dicts with 'role' and 'content'
    model: Model identifier
    **kwargs: Additional options (temperature, max_tokens, etc.)

Returns:
    JSON bytes

### `decode_chat_response(data)`

Decode chat completion response.

Args:
    data: JSON bytes or string

Returns:
    ChatCompletionResponse struct

### `decode_stream_chunk(data)`

Decode streaming chat chunk.

Args:
    data: JSON bytes or string (without "data: " prefix)

Returns:
    ChatCompletionChunk struct

### `benchmark_serialization(data, iterations)`

Benchmark JSON vs MessagePack serialization.

Args:
    data: Object to serialize
    iterations: Number of iterations

Returns:
    Dict of format -> BenchmarkResult

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `base64`
- `dataclasses.dataclass`
- `datetime.datetime`
- `datetime.timezone`
- `enum.Enum`
- `logging`
- `msgspec`
- `msgspec.Struct`
- `msgspec.json`
- `msgspec.msgpack`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- ... and 7 more

---
*Auto-generated documentation*
