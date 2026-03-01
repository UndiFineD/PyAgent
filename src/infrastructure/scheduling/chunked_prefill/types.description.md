# types

**File**: `src\infrastructure\scheduling\chunked_prefill\types.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 9 imports  
**Lines**: 172  
**Complexity**: 12 (moderate)

## Overview

Types and data structures for chunked prefill.

## Classes (6)

### `ChunkState`

**Inherits from**: Enum

State of a prefill chunk.

### `ChunkPriority`

**Inherits from**: Enum

Priority for chunk scheduling.

### `ChunkMetrics`

Metrics for chunk processing.

**Methods** (3):
- `queue_time_ms(self)`
- `execution_time_ms(self)`
- `total_time_ms(self)`

### `PrefillChunk`

A single chunk of prefill tokens.

Attributes:
    chunk_id: Unique identifier for this chunk
    request_id: Parent request identifier
    chunk_index: Index within the request (0-based)
    start_idx: Start token index in original prompt
    end_idx: End token index (exclusive)
    tokens: Token IDs for this chunk

**Methods** (4):
- `__post_init__(self)`
- `size(self)`
- `is_first(self)`
- `is_complete(self)`

### `ChunkedRequest`

A request split into multiple chunks.

Attributes:
    request_id: Unique request identifier
    total_tokens: Total prompt tokens
    chunks: List of chunks for this request

**Methods** (5):
- `num_chunks(self)`
- `completed_chunks(self)`
- `progress(self)`
- `is_complete(self)`
- `next_chunk(self)`

### `ChunkedPrefillConfig`

Configuration for chunked prefill.

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.Any`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
