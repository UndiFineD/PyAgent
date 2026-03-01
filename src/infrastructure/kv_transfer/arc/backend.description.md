# backend

**File**: `src\infrastructure\kv_transfer\arc\backend.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 116  
**Complexity**: 13 (moderate)

## Overview

Phase 45: ARC Offload Backends
Backends for block storage in the ARC offloading system.

## Classes (2)

### `Backend`

**Inherits from**: ABC

Abstract backend for block storage.

**Methods** (6):
- `get_num_free_blocks(self)`
- `allocate_blocks(self, block_hashes)`
- `free(self, block)`
- `get_load_store_spec(self, block_hashes, blocks)`
- `block_size(self)`
- `medium(self)`

### `SimpleBackend`

**Inherits from**: Backend

Simple in-memory backend for testing.

**Methods** (7):
- `__init__(self, num_blocks, block_size, medium)`
- `get_num_free_blocks(self)`
- `allocate_blocks(self, block_hashes)`
- `free(self, block)`
- `get_load_store_spec(self, block_hashes, blocks)`
- `block_size(self)`
- `medium(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `src.infrastructure.kv_transfer.arc.types.BlockHash`
- `src.infrastructure.kv_transfer.arc.types.BlockState`
- `src.infrastructure.kv_transfer.arc.types.BlockStatus`
- `src.infrastructure.kv_transfer.arc.types.LoadStoreSpec`
- `src.infrastructure.kv_transfer.arc.types.OffloadMedium`
- `threading`

---
*Auto-generated documentation*
