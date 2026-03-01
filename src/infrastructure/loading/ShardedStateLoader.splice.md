# Class Breakdown: ShardedStateLoader

**File**: `src\infrastructure\loading\ShardedStateLoader.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ShardPattern`

**Line**: 58  
**Methods**: 2

Pattern for shard file naming.

vLLM Pattern: DEFAULT_PATTERN = "model-rank-{rank}-part-{part}.safetensors"

[TIP] **Suggested split**: Move to `shardpattern.py`

---

### 2. `ShardedTensor`

**Line**: 86  
**Methods**: 1

Represents a tensor that is sharded across ranks.

[TIP] **Suggested split**: Move to `shardedtensor.py`

---

### 3. `SubtensorFilter`

**Line**: 104  
**Methods**: 1

Filter for identifying and handling subtensors.

vLLM Pattern: _filter_subtensors from sharded_state_loader.py
Identifies tensors that share memory with other tensors and keeps
only the parent tensor ...

[TIP] **Suggested split**: Move to `subtensorfilter.py`

---

### 4. `ShardedStateLoader`

**Line**: 167  
**Methods**: 4

Loader for sharded model checkpoints.

vLLM Pattern: ShardedStateLoader class
Each worker only loads its own shard for efficient tensor-parallel loading.

[TIP] **Suggested split**: Move to `shardedstateloader.py`

---

### 5. `IncrementalShardLoader`

**Line**: 271  
**Methods**: 4

Incremental shard loading with memory management.

BEYOND vLLM: Load shards incrementally with configurable memory budget,
evicting old shards as new ones are loaded.

[TIP] **Suggested split**: Move to `incrementalshardloader.py`

---

### 6. `AsyncShardLoader`

**Line**: 343  
**Methods**: 4

Asynchronous shard loading with prefetching.

BEYOND vLLM: Prefetch next shards while processing current shard
for improved throughput on I/O-bound operations.

[TIP] **Suggested split**: Move to `asyncshardloader.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
