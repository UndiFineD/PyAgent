# ForwardContext

**File**: `src\infrastructure\execution\ForwardContext.py`  
**Type**: Python Module  
**Summary**: 4 classes, 6 functions, 13 imports  
**Lines**: 383  
**Complexity**: 23 (complex)

## Overview

ForwardContext.py - Execution context management for model forward passes.

Inspired by vLLM's forward_context.py. Provides thread-local context for
attention metadata, batch descriptors, and data parallel coordination.

Phase 29: Execution Context, Batching & Async Streaming

## Classes (4)

### `BatchDescriptor`

**Inherits from**: NamedTuple

Batch descriptor for CUDA graph dispatching.

Uniquely identifies a padded batch configuration for graph key matching.
Based on vLLM's BatchDescriptor pattern.

**Methods** (4):
- `relaxed(self)`
- `with_num_tokens(self, num_tokens)`
- `key(self)`
- `hash_key(self)`

### `DPMetadata`

Data parallel metadata for distributed inference.

Tracks token distribution across data parallel ranks for synchronization.
Based on vLLM's DPMetadata pattern.

**Methods** (4):
- `make(cls, world_size, rank, num_tokens, num_tokens_across_dp)`
- `single(cls, num_tokens)`
- `get_local_tokens(self)`
- `get_total_tokens(self)`

### `ForwardContext`

Thread-local context for model forward passes.

Stores attention metadata, batch descriptors, and coordination info
that needs to be accessed during forward execution.

Based on vLLM's ForwardContext pattern.

**Methods** (4):
- `get_attn_metadata(self, layer_name)`
- `get_num_tokens(self)`
- `is_cudagraph_enabled(self)`
- `elapsed_time(self)`

### `ForwardTimingTracker`

Tracks forward pass timing statistics.

Provides batch size to latency mapping for performance analysis.

**Methods** (5):
- `__init__(self, log_interval)`
- `record(self, batch_size, elapsed_ms)`
- `get_stats(self)`
- `should_log(self)`
- `clear(self)`

## Functions (6)

### `get_forward_context()`

Get the current forward context.

Raises RuntimeError if no context is set.

### `is_forward_context_available()`

Check if a forward context is currently set.

### `_set_forward_context(ctx)`

Internal: set context and return previous.

### `create_forward_context(attn_metadata, virtual_engine, batch_descriptor, dp_metadata, cudagraph_mode, num_tokens)`

Factory function to create a ForwardContext.

Args:
    attn_metadata: Dict mapping layer names to attention metadata
    virtual_engine: Virtual engine index
    batch_descriptor: Batch descriptor for CUDA graph dispatching
    dp_metadata: Data parallel metadata
    cudagraph_mode: CUDA graph mode (0=NONE, 1=PIECEWISE, 2=FULL)
    num_tokens: Number of tokens in batch
    **additional_kwargs: Extra model-specific kwargs

Returns:
    Configured ForwardContext

### `set_forward_context(attn_metadata, virtual_engine, batch_descriptor, dp_metadata, cudagraph_mode, num_tokens)`

Context manager for setting forward context.

Supports nested contexts by saving and restoring previous context.

Example:
    with set_forward_context(num_tokens=32, cudagraph_mode=2) as ctx:
        output = model(input_ids, positions)

Args:
    attn_metadata: Dict mapping layer names to attention metadata
    virtual_engine: Virtual engine index
    batch_descriptor: Batch descriptor for CUDA graph dispatching
    dp_metadata: Data parallel metadata
    cudagraph_mode: CUDA graph mode (0=NONE, 1=PIECEWISE, 2=FULL)
    num_tokens: Number of tokens in batch
    **additional_kwargs: Extra model-specific kwargs

Yields:
    The configured ForwardContext

### `get_timing_tracker()`

Get the global timing tracker.

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.IntEnum`
- `enum.auto`
- `numpy`
- `threading`
- `time`
- `typing.Any`
- `typing.Generator`
- `typing.NamedTuple`
- `typing.Optional`

---
*Auto-generated documentation*
