# backends

**File**: `src\infrastructure\loading\kv_offload\backends.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 87  
**Complexity**: 7 (moderate)

## Overview

Storage backends for KV block offloading.

## Classes (1)

### `MemoryBackend`

**Inherits from**: OffloadingBackend

In-memory backend for block storage.

Simple implementation for testing and CPU offloading.

**Methods** (7):
- `__init__(self, capacity_blocks, block_size, medium)`
- `medium(self)`
- `block_size(self)`
- `get_num_free_blocks(self)`
- `allocate_blocks(self, block_hashes)`
- `free(self, block)`
- `get_load_store_spec(self, block_hashes, blocks)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `base.OffloadingBackend`
- `models.BlockHash`
- `models.BlockStatus`
- `models.LoadStoreSpec`
- `models.OffloadMedium`
- `threading`
- `typing.Dict`
- `typing.Iterable`
- `typing.List`

---
*Auto-generated documentation*
