# CUDAGraphConfig

**File**: `src\infrastructure\execution\CUDAGraphConfig.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 15 imports  
**Lines**: 505  
**Complexity**: 27 (complex)

## Overview

CUDAGraphConfig.py - CUDA graph mode management and configuration.

Inspired by vLLM's config/compilation.py. Provides CUDA graph capture
and replay management for optimized inference.

Phase 29: Execution Context, Batching & Async Streaming

## Classes (5)

### `CUDAGraphMode`

**Inherits from**: Enum

CUDA graph execution modes.

Based on vLLM's CUDAGraphMode enum.

### `CUDAGraphConfig`

Configuration for CUDA graph capture and replay.

Based on vLLM's compilation config patterns.

**Methods** (5):
- `should_use_cudagraph(self, batch_size, seq_len)`
- `get_padded_batch_size(self, batch_size)`
- `to_dict(self)`
- `from_dict(cls, d)`
- `disabled(cls)`

### `CUDAGraphEntry`

A captured CUDA graph entry.

Stores the graph and associated metadata.

**Methods** (3):
- `replay(self, inputs)`
- `key(self)`
- `avg_replay_time_ms(self)`

### `CUDAGraphRegistry`

Registry for captured CUDA graphs.

Manages graph capture, storage, and lookup.

**Methods** (8):
- `__init__(self, config)`
- `capture(self, batch_size, seq_len, capture_fn, input_shapes, output_shapes)`
- `get(self, batch_size, seq_len)`
- `has(self, batch_size, seq_len)`
- `remove(self, batch_size, seq_len)`
- `clear(self)`
- `num_graphs(self)`
- `stats(self)`

### `CUDAGraphManager`

High-level manager for CUDA graph operations.

Provides convenient interface for graph capture and replay.

**Methods** (11):
- `__init__(self, config)`
- `mode(self)`
- `mode(self, value)`
- `is_enabled(self)`
- `should_capture(self, batch_size, seq_len)`
- `get_mode_for_batch(self, batch_size, seq_len)`
- `capture_graph(self, batch_size, seq_len, capture_fn, input_shapes, output_shapes)`
- `replay_graph(self, batch_size, seq_len, inputs)`
- `execute_or_capture(self, batch_size, seq_len, execute_fn, inputs, input_shapes, output_shapes)`
- `stats(self)`
- ... and 1 more methods

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `logging`
- `numpy`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
