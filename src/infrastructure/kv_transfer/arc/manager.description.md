# manager

**File**: `src\infrastructure\kv_transfer\arc\manager.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 22 imports  
**Lines**: 397  
**Complexity**: 19 (moderate)

## Overview

Phase 45: ARC Offload Manager
Implementation of Adaptive Replacement Cache (ARC) and variants.

## Classes (3)

### `ARCOffloadManager`

**Inherits from**: OffloadingManager

ARC (Adaptive Replacement Cache) offloading manager.

Implements the ARC eviction policy which adaptively balances
recency (T1) and frequency (T2) based on workload patterns.

**Methods** (12):
- `__init__(self, backend, enable_events, adaptation_speed, kvzap_config)`
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `prepare_store(self, block_hashes)`
- `_select_victim(self)`
- `update_block_importance(self, block_hash, hidden_states)`
- `_trim_ghost_lists(self)`
- `complete_store(self, block_hashes)`
- ... and 2 more methods

### `AdaptiveARCManager`

**Inherits from**: ARCOffloadManager

ARC manager with enhanced adaptation features.

**Methods** (6):
- `__init__(self, backend, enable_events, min_adaptation_speed, max_adaptation_speed)`
- `touch_for_request(self, block_hashes, request_id)`
- `complete_request(self, request_id)`
- `get_block_affinity(self, block_hash)`
- `_select_victim(self)`
- `adjust_adaptation_speed(self, hit_rate)`

### `AsyncARCManager`

Async wrapper for ARC offloading manager.

**Methods** (1):
- `__init__(self, manager)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `asyncio`
- `collections.OrderedDict`
- `src.infrastructure.kv_transfer.KVzap.KVzapConfig`
- `src.infrastructure.kv_transfer.KVzap.KVzapPruner`
- `src.infrastructure.kv_transfer.arc.backend.Backend`
- `src.infrastructure.kv_transfer.arc.base.OffloadingManager`
- `src.infrastructure.kv_transfer.arc.types.BlockHash`
- `src.infrastructure.kv_transfer.arc.types.BlockState`
- `src.infrastructure.kv_transfer.arc.types.BlockStatus`
- `src.infrastructure.kv_transfer.arc.types.LoadStoreSpec`
- `src.infrastructure.kv_transfer.arc.types.OffloadingEvent`
- `src.infrastructure.kv_transfer.arc.types.PrepareStoreOutput`
- `threading`
- `time`
- ... and 7 more

---
*Auto-generated documentation*
