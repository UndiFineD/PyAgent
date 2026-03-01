# InputBufferManager

**File**: `src\infrastructure\cuda\InputBufferManager.py`  
**Type**: Python Module  
**Summary**: 9 classes, 1 functions, 25 imports  
**Lines**: 480  
**Complexity**: 30 (complex)

## Overview

InputBufferManager - Input staging and buffer management for CUDA graphs.

Implements vLLM's InputBatch patterns:
- Pre-allocated input buffers
- Static tensor storage for graph capture
- Efficient input staging
- Memory-efficient buffer pooling

Beyond vLLM:
- Hierarchical buffer pools
- Predictive pre-allocation
- Zero-copy staging when possible

## Classes (9)

### `BufferState`

**Inherits from**: Enum

State of a buffer.

### `BufferSpec`

Specification for a buffer.

**Methods** (2):
- `size_bytes(self)`
- `__hash__(self)`

### `BufferEntry`

Entry in the buffer pool.

**Methods** (2):
- `mark_in_use(self)`
- `release(self)`

### `BufferPool`

**Inherits from**: ABC

Abstract buffer pool interface.

**Methods** (3):
- `allocate(self, spec)`
- `release(self, tensor)`
- `clear(self)`

### `SimpleBufferPool`

**Inherits from**: BufferPool

Simple buffer pool implementation.

**Methods** (6):
- `__init__(self, max_buffers)`
- `allocate(self, spec)`
- `_create_tensor(self, spec)`
- `_evict_oldest(self)`
- `release(self, tensor)`
- `clear(self)`

### `InputSlot`

A slot for input data in the buffer.

**Methods** (1):
- `set_data(self, data)`

### `InputBufferManager`

Manages input buffers for CUDA graph execution.

Based on vLLM's InputBatch pattern for pre-allocated
static buffers used during graph capture/replay.

**Methods** (7):
- `__init__(self, pool, max_batch_size, max_seq_len)`
- `_init_default_slots(self)`
- `register_slot(self, name, spec, is_static)`
- `get_slot(self, name)`
- `stage_inputs(self, inputs, num_tokens)`
- `get_static_tensors(self)`
- `release_all(self)`

### `HierarchicalBufferPool`

**Inherits from**: BufferPool

Hierarchical buffer pool.

Beyond vLLM:
- Multiple tiers (pinned CPU, GPU, managed)
- Automatic promotion/demotion

**Methods** (4):
- `__init__(self)`
- `allocate(self, spec)`
- `release(self, tensor)`
- `clear(self)`

### `PredictiveBufferManager`

**Inherits from**: InputBufferManager

Predictive buffer pre-allocation.

Beyond vLLM:
- Predicts future buffer needs
- Pre-warms buffers based on patterns

**Methods** (4):
- `__init__(self)`
- `record_usage(self, num_tokens)`
- `predict_next_sizes(self, n)`
- `prewarm(self)`

## Functions (1)

### `create_input_buffer_manager(max_batch_size, max_seq_len, use_hierarchical, use_predictive)`

Factory function for input buffer managers.

Args:
    max_batch_size: Maximum batch size
    max_seq_len: Maximum sequence length
    use_hierarchical: Use hierarchical pool
    use_predictive: Use predictive manager
    
Returns:
    Configured buffer manager

## Dependencies

**Imports** (25):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.Counter`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `numpy`
- `threading`
- `time`
- `torch`
- `typing.Any`
- ... and 10 more

---
*Auto-generated documentation*
