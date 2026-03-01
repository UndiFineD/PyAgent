# buffers

**File**: `src\infrastructure\execution\batch\buffers.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 87  
**Complexity**: 2 (simple)

## Overview

GPU-resident input buffers for batch management.

## Classes (1)

### `InputBuffers`

Pre-allocated GPU tensors for batch inputs.

Maintains persistent buffers to avoid runtime allocation overhead.
CUDA graph compatible through fixed-size allocation.

**Methods** (2):
- `__init__(self, max_num_reqs, max_num_tokens, inputs_embeds_size, vocab_size, dtype, device)`
- `_init_numpy_buffers(self, max_num_reqs, max_num_tokens)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `numpy`
- `torch`
- `typing.Any`

---
*Auto-generated documentation*
