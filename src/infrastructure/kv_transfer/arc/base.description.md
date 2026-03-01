# base

**File**: `src\infrastructure\kv_transfer\arc\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 44  
**Complexity**: 5 (moderate)

## Overview

Phase 45: ARC Offload Base
Abstract base for offloading managers.

## Classes (1)

### `OffloadingManager`

**Inherits from**: ABC

Abstract base for offloading managers.

**Methods** (5):
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `prepare_store(self, block_hashes)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `src.infrastructure.kv_transfer.arc.types.BlockHash`
- `src.infrastructure.kv_transfer.arc.types.LoadStoreSpec`
- `src.infrastructure.kv_transfer.arc.types.PrepareStoreOutput`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
