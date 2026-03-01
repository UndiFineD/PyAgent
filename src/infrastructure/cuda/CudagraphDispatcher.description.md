# CudagraphDispatcher

**File**: `src\infrastructure\cuda\CudagraphDispatcher.py`  
**Type**: Python Module  
**Summary**: 10 classes, 2 functions, 22 imports  
**Lines**: 513  
**Complexity**: 30 (complex)

## Overview

CudagraphDispatcher - Dispatch logic for CUDA graph execution.

Implements vLLM's CudagraphDispatcher patterns for:
- Graph selection based on batch descriptors
- Fallback to eager execution
- Piecewise vs full graph dispatch
- Thread-safe graph management

Beyond vLLM:
- Predictive graph selection
- Multi-stream dispatch
- Composite graph support

## Classes (10)

### `DispatchMode`

**Inherits from**: Enum

Mode of execution dispatch.

### `DispatchKey`

Key for dispatch decisions.

Attributes:
    num_tokens: Number of tokens in batch
    num_reqs: Number of requests
    max_seq_len: Maximum sequence length
    is_prefill: Whether this is prefill phase

**Methods** (1):
- `__hash__(self)`

### `DispatchStats`

Statistics for dispatch decisions.

**Methods** (1):
- `graph_ratio(self)`

### `DispatchPolicy`

**Inherits from**: ABC

Abstract dispatch policy.

**Methods** (2):
- `should_use_graph(self, key, graph_available)`
- `select_mode(self, key, available_modes)`

### `DefaultDispatchPolicy`

**Inherits from**: DispatchPolicy

Default policy preferring graphs when available.

**Methods** (3):
- `__init__(self, min_tokens_for_graph, max_tokens_for_graph, prefer_piecewise)`
- `should_use_graph(self, key, graph_available)`
- `select_mode(self, key, available_modes)`

### `AdaptiveDispatchPolicy`

**Inherits from**: DispatchPolicy

Adaptive policy learning from history.

Beyond vLLM:
- Learns optimal dispatch based on performance history
- Adjusts thresholds dynamically

**Methods** (4):
- `__init__(self, history_size)`
- `record(self, key, mode, latency)`
- `should_use_graph(self, key, graph_available)`
- `select_mode(self, key, available_modes)`

### `GraphEntry`

Entry in the graph cache.

### `CudagraphDispatcher`

Dispatcher for CUDA graph execution.

Manages graph selection, fallback logic, and execution
based on vLLM's dispatch patterns.

**Methods** (11):
- `__init__(self, eager_runner, policy, max_cached_graphs)`
- `register_graph(self, key, graph, input_ptrs)`
- `has_graph(self, key)`
- `get_graph(self, key)`
- `dispatch(self, key)`
- `_replay_graph(self, entry)`
- `_replay_piecewise(self, entry)`
- `stats(self)`
- `clear_cache(self)`
- `enable_mode(self, mode)`
- ... and 1 more methods

### `CompositeDispatcher`

Composite dispatcher supporting multiple strategies.

Beyond vLLM:
- Chains multiple dispatchers
- Priority-based selection
- Fallback chains

**Methods** (3):
- `__init__(self)`
- `add_dispatcher(self, name, dispatcher, priority)`
- `dispatch(self, key)`

### `StreamDispatcher`

**Inherits from**: CudagraphDispatcher

Multi-stream dispatcher.

Beyond vLLM:
- Dispatches to different CUDA streams
- Stream-local graph caching

**Methods** (3):
- `__init__(self, eager_runner, num_streams)`
- `_select_stream(self, key)`
- `dispatch(self, key)`

## Functions (2)

### `create_dispatch_key(num_tokens, num_reqs, max_seq_len, is_prefill)`

Factory function for dispatch keys.

### `get_padded_key(key, pad_to)`

Get padded key for graph cache alignment.

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generic`
- ... and 7 more

---
*Auto-generated documentation*
