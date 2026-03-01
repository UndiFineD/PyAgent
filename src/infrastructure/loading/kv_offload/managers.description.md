# managers

**File**: `src\infrastructure\loading\kv_offload\managers.py`  
**Type**: Python Module  
**Summary**: 3 classes, 2 functions, 16 imports  
**Lines**: 526  
**Complexity**: 29 (complex)

## Overview

Management logic for KV offloading eviction policies and tiers.

## Classes (3)

### `LRUOffloadingManager`

**Inherits from**: OffloadingManager

LRU-based offloading manager.

vLLM Pattern: LRUOffloadingManager from lru_manager.py
Evicts blocks by least recently used order.

**Methods** (8):
- `__init__(self, backend, enable_events)`
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `prepare_store(self, block_hashes)`
- `complete_store(self, block_hashes, success)`
- `take_events(self)`

### `ARCOffloadingManager`

**Inherits from**: OffloadingManager

ARC (Adaptive Replacement Cache) offloading manager.

vLLM Pattern: ARCOffloadingManager from arc_manager.py
Dynamically balances recency vs frequency for eviction decisions.

**Methods** (10):
- `__init__(self, backend, enable_events)`
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `_evict_one(self)`
- `prepare_store(self, block_hashes)`
- `complete_store(self, block_hashes, success)`
- `take_events(self)`
- `stats(self)`

### `TieredOffloadManager`

**Inherits from**: OffloadingManager

Tiered offloading with multiple backends (GPU→CPU→NVMe).

**Methods** (9):
- `__init__(self, backends, enable_events)`
- `_get_tier(self, block_hash)`
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `prepare_store(self, block_hashes)`
- `complete_store(self, block_hashes, success)`
- `promote(self, block_hash, target_tier)`

## Functions (2)

### `compute_lru_eviction_rust(blocks, num_to_evict)`

Select blocks to evict using Rust LRU.

### `compute_arc_target_rust(t1_size, t2_size, b1_size, b2_size, current_target, hit_in_b1, capacity)`

Compute new ARC target using Rust.

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `base.OffloadingBackend`
- `base.OffloadingManager`
- `collections.OrderedDict`
- `core.rust_core`
- `logging`
- `models.BlockHash`
- `models.BlockStatus`
- `models.LoadStoreSpec`
- `models.OffloadingEvent`
- `models.PrepareStoreOutput`
- `typing.Any`
- `typing.Dict`
- `typing.Iterable`
- `typing.List`
- ... and 1 more

---
*Auto-generated documentation*
