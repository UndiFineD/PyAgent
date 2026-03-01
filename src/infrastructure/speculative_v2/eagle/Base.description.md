# Base

**File**: `src\infrastructure\speculative_v2\eagle\Base.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 5 imports  
**Lines**: 60  
**Complexity**: 6 (moderate)

## Overview

Base utilities and metadata for EAGLE.

## Classes (4)

### `InputBuffer`

**Inherits from**: Protocol

Protocol for input buffer.

**Methods** (3):
- `get_token_ids(self)`
- `get_positions(self)`
- `get_hidden_states(self)`

### `CpuGpuBuffer`

Buffer that syncs between CPU and GPU.

**Methods** (3):
- `sync_to_gpu(self)`
- `sync_to_cpu(self)`
- `update(self, data)`

### `AttentionMetadata`

Metadata for attention computation.

### `TreeAttentionMetadata`

**Inherits from**: AttentionMetadata

Metadata for tree attention.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.Protocol`

---
*Auto-generated documentation*
