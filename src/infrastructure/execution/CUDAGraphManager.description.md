# CUDAGraphManager

**File**: `src\infrastructure\execution\CUDAGraphManager.py`  
**Type**: Python Module  
**Summary**: 5 classes, 2 functions, 14 imports  
**Lines**: 561  
**Complexity**: 22 (complex)

## Overview

CUDAGraphManager - Graph capture and replay for reduced kernel launch overhead.

Implements vLLM's CUDA graph patterns for efficient GPU execution:
- CUDAGraphEntry: Captured graph with metadata
- CUDAGraphKey: Batch size + flags hashing
- CUDAGraphManager: Capture/lookup/replay operations

Beyond vLLM: LRU eviction for memory pressure management.

## Classes (5)

### `CUDAGraphMode`

**Inherits from**: Enum

CUDA graph execution modes.

### `BatchDescriptor`

**Inherits from**: NamedTuple

Describes a batch for CUDA graph keying.

### `CUDAGraphEntry`

A captured CUDA graph with associated metadata.

**Methods** (1):
- `mark_used(self)`

### `CUDAGraphRegistry`

Registry of captured CUDA graphs with LRU eviction.

**Methods** (7):
- `__init__(self, max_graphs, max_memory_bytes)`
- `get(self, key)`
- `put(self, entry)`
- `_evict_lru(self)`
- `clear(self)`
- `__len__(self)`
- `__contains__(self, key)`

### `CUDAGraphManager`

Manages CUDA graph capture and replay for model execution.

Provides:
- Graph capture with dummy inputs
- Batch-size keyed lookup
- Graph replay with input buffer updates
- Memory pool tracking
- LRU eviction (beyond vLLM)

**Methods** (12):
- `__init__(self, mode, max_graphs, max_memory_bytes, device)`
- `enabled(self)`
- `warmup(self, generate_fn, max_tokens, max_reqs, create_dummy_inputs)`
- `capture(self, generate_fn, num_tokens, num_reqs, input_buffers, uniform, has_lora, has_multimodal)`
- `_estimate_graph_memory(self, input_buffers, output_buffers)`
- `lookup(self, num_tokens, num_reqs, uniform, has_lora, has_multimodal)`
- `replay(self, entry, input_updates)`
- `get_or_run(self, generate_fn, input_buffers, num_tokens, num_reqs, uniform, has_lora, has_multimodal)`
- `pad_for_cudagraph(self, size, granularity)`
- `find_closest_size(self, num_tokens, num_reqs)`
- ... and 2 more methods

## Functions (2)

### `compute_graph_key(desc)`

Compute a unique key for a batch descriptor.

The key is used to lookup cached CUDA graphs.

### `generate_warmup_sizes(max_tokens, max_reqs, granularity)`

Generate batch sizes for CUDA graph warmup.

Uses power-of-2 and granularity-aligned sizes for efficient coverage.

Args:
    max_tokens: Maximum tokens per batch
    max_reqs: Maximum requests per batch
    granularity: Alignment granularity
    
Returns:
    List of (num_tokens, num_reqs) tuples

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `logging`
- `numpy`
- `time`
- `torch`
- `typing.Any`
- `typing.Callable`
- `typing.NamedTuple`

---
*Auto-generated documentation*
