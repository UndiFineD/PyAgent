# base

**File**: `src\infrastructure\loading\kv_offload\base.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 98  
**Complexity**: 12 (moderate)

## Overview

Base classes for KV offloading backends and managers.

## Classes (2)

### `OffloadingBackend`

**Inherits from**: ABC

Abstract backend for block storage.

**Methods** (6):
- `medium(self)`
- `block_size(self)`
- `get_num_free_blocks(self)`
- `allocate_blocks(self, block_hashes)`
- `free(self, block)`
- `get_load_store_spec(self, block_hashes, blocks)`

### `OffloadingManager`

**Inherits from**: ABC

Abstract manager for KV cache offloading.

**Methods** (6):
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `prepare_store(self, block_hashes)`
- `complete_store(self, block_hashes, success)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `models.BlockHash`
- `models.BlockStatus`
- `models.LoadStoreSpec`
- `models.PrepareStoreOutput`
- `typing.Dict`
- `typing.Iterable`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
