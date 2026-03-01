# CUDAGraphManager

**File**: `src\infrastructure\cuda\CUDAGraphManager.py`  
**Type**: Python Module  
**Summary**: 8 classes, 2 functions, 24 imports  
**Lines**: 505  
**Complexity**: 29 (complex)

## Overview

CUDAGraphManager - CUDA graph capture and replay management.

Implements vLLM's CUDAGraphWrapper patterns for efficient GPU execution:
- BatchDescriptor: Graph cache keys for shape-based lookup
- CUDAGraphEntry: Cached graphs with weak-ref outputs
- CUDAGraphWrapper: Automatic capture/replay management
- Runtime modes: NONE/PIECEWISE/FULL

Beyond vLLM:
- Adaptive capture based on hit rate patterns
- Predictive pre-warming for common shapes
- Memory-aware graph selection

## Classes (8)

### `CUDAGraphMode`

**Inherits from**: IntEnum

CUDA graph execution modes.

**Methods** (2):
- `has_graphs(self)`
- `has_full_cudagraphs(self)`

### `BatchDescriptor`

Key for CUDA graph cache lookup.

Attributes:
    num_tokens: Number of tokens in batch
    num_reqs: Number of requests (optional)
    is_uniform_decode: Whether batch is uniform decode

**Methods** (2):
- `__hash__(self)`
- `relaxed(self)`

### `CUDAGraphEntry`

Cached CUDA graph entry with metadata.

Attributes:
    batch_descriptor: Key for this entry
    cudagraph: The captured CUDA graph (mock for non-GPU)
    output: Weak reference to output tensors
    input_addresses: Tracked input tensor addresses for validation
    capture_time: When graph was captured
    replay_count: Number of times replayed

**Methods** (1):
- `increment_replay(self)`

### `CUDAGraphOptions`

Options for CUDA graph wrapper behavior.

### `CUDAGraphStats`

Statistics for CUDA graph usage.

**Methods** (1):
- `hit_rate(self)`

### `MockCUDAGraph`

Mock CUDA graph for non-GPU environments.

**Methods** (4):
- `__init__(self)`
- `capture_begin(self)`
- `capture_end(self)`
- `replay(self)`

### `CUDAGraphWrapper`

Wraps a callable to add CUDA graph capture/replay.

Based on vLLM's CUDAGraphWrapper from cuda_graph.py.
Provides automatic graph caching, capture, and replay
based on batch descriptors.

Beyond vLLM:
- Adaptive capture based on hit patterns
- Memory-aware graph eviction
- Predictive pre-warming

**Methods** (12):
- `__init__(self, runnable, runtime_mode, options, max_cached_graphs)`
- `__getattr__(self, key)`
- `unwrap(self)`
- `__call__(self)`
- `_capture(self, descriptor)`
- `_replay(self, descriptor)`
- `_cache_entry(self, descriptor, entry)`
- `_evict_lru(self)`
- `_get_input_addresses(self, args)`
- `get_cached_descriptors(self)`
- ... and 2 more methods

### `AdaptiveCUDAGraphWrapper`

**Inherits from**: CUDAGraphWrapper

Extended wrapper with adaptive capture based on usage patterns.

Beyond vLLM:
- Tracks shape frequency to prioritize common shapes
- Predictive pre-warming of likely shapes
- Memory budget awareness

**Methods** (5):
- `__init__(self, runnable, runtime_mode, options, max_cached_graphs, min_replays_to_keep)`
- `__call__(self)`
- `_evict_lru(self)`
- `get_hot_shapes(self, top_k)`
- `prewarm(self, shapes, dummy_fn)`

## Functions (2)

### `cudagraph_context(mode, descriptor)`

Context manager for CUDA graph execution context.

### `get_cudagraph_sizes(capture_sizes, max_num_reqs, max_num_tokens, mode)`

Compute CUDA graph capture sizes.

Args:
    capture_sizes: Explicit sizes to capture
    max_num_reqs: Maximum number of requests
    max_num_tokens: Maximum number of tokens
    mode: CUDA graph mode
    
Returns:
    List of sizes to capture graphs for

## Dependencies

**Imports** (24):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.defaultdict`
- `contextlib.contextmanager`
- `dataclasses`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.IntEnum`
- `enum.auto`
- `gc`
- `logging`
- `threading`
- `time`
- `typing.Any`
- ... and 9 more

---
*Auto-generated documentation*
