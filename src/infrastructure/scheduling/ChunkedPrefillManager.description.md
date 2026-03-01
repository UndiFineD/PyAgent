# ChunkedPrefillManager

**File**: `src\infrastructure\scheduling\ChunkedPrefillManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 16 imports  
**Lines**: 578  
**Complexity**: 20 (complex)

## Overview

ChunkedPrefillManager - Chunked prefill orchestration for long prompts.

This module implements chunked prefill for processing long prompts across
multiple forward passes, enabling better memory utilization and latency.

Inspired by vLLM's chunked prefill, but extends with:
- Dynamic chunk sizing based on memory pressure
- Priority-aware chunk ordering
- Chunk state tracking with resumption support
- Overlapping chunk processing with pipeline

Example:
    >>> manager = ChunkedPrefillManager(chunk_size=512)
    >>> chunks = manager.create_chunks(request_id="req1", prompt_tokens=2048)
    >>> for chunk in manager.iterate_chunks("req1"):
    ...     result = model.prefill(chunk.tokens)
    ...     manager.complete_chunk(chunk.chunk_id, result)
    >>> final = manager.merge_chunks("req1")

## Classes (1)

### `ChunkedPrefillManager`

Manager for chunked prefill operations.

This class handles splitting long prompts into chunks and
orchestrating their execution across multiple forward passes.

Attributes:
    config: Manager configuration
    requests: Active chunked requests

**Methods** (18):
- `__init__(self, config, tokenize_fn)`
- `should_chunk(self, token_count)`
- `compute_chunk_boundaries(self, total_tokens, chunk_size, memory_pressure)`
- `create_chunks(self, request_id, prompt_tokens, priority, chunk_size, memory_pressure)`
- `create_chunks_from_prompt(self, request_id, prompt, priority, chunk_size)`
- `_sort_pending(self)`
- `schedule_chunk(self)`
- `start_chunk(self, chunk_id)`
- `complete_chunk(self, chunk_id, output, kv_cache)`
- `fail_chunk(self, chunk_id, error)`
- ... and 8 more methods

## Functions (2)

### `create_prefill_manager(chunk_size, threshold, dynamic)`

Create a chunked prefill manager.

### `chunk_prompt(tokens, chunk_size)`

Simple utility to chunk tokens.

Args:
    tokens: Token list to chunk
    chunk_size: Size of each chunk
    
Returns:
    List of token chunks

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `src.core.rust_bridge.get_bridge`
- `src.infrastructure.scheduling.chunked_prefill.types.ChunkMetrics`
- `src.infrastructure.scheduling.chunked_prefill.types.ChunkPriority`
- `src.infrastructure.scheduling.chunked_prefill.types.ChunkState`
- `src.infrastructure.scheduling.chunked_prefill.types.ChunkedPrefillConfig`
- `src.infrastructure.scheduling.chunked_prefill.types.ChunkedRequest`
- `src.infrastructure.scheduling.chunked_prefill.types.PrefillChunk`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Iterator`
- `typing.Optional`
- `typing.TypeVar`
- ... and 1 more

---
*Auto-generated documentation*
