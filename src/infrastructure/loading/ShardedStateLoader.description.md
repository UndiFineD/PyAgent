# ShardedStateLoader

**File**: `src\infrastructure\loading\ShardedStateLoader.py`  
**Type**: Python Module  
**Summary**: 6 classes, 2 functions, 35 imports  
**Lines**: 471  
**Complexity**: 18 (moderate)

## Overview

Sharded State Loader for PyAgent

This module provides sharded model loading functionality for tensor-parallel
and pipeline-parallel model deployments, inspired by vLLM's sharded_state_loader.py.

Key Features:
- Per-rank shard loading (no need to load full checkpoint)
- Subtensor filtering for shared storage
- S3 and local file system support patterns
- BEYOND vLLM: Incremental loading, async prefetch, smart caching

vLLM Patterns:
- ShardedStateLoader with pattern-based shard discovery
- _filter_subtensors for shared storage handling
- Parallel weight download and loading

## Classes (6)

### `ShardPattern`

Pattern for shard file naming.

vLLM Pattern: DEFAULT_PATTERN = "model-rank-{rank}-part-{part}.safetensors"

**Methods** (2):
- `format_for_rank(self, rank, part)`
- `parse_filename(self, filename)`

### `ShardedTensor`

Represents a tensor that is sharded across ranks.

**Methods** (1):
- `local_shape(self)`

### `SubtensorFilter`

Filter for identifying and handling subtensors.

vLLM Pattern: _filter_subtensors from sharded_state_loader.py
Identifies tensors that share memory with other tensors and keeps
only the parent tensor to avoid duplication.

**Methods** (1):
- `filter_subtensors(tensors)`

### `ShardedStateLoader`

Loader for sharded model checkpoints.

vLLM Pattern: ShardedStateLoader class
Each worker only loads its own shard for efficient tensor-parallel loading.

**Methods** (4):
- `__init__(self, pattern, rank, world_size)`
- `discover_shards(self, model_path)`
- `load_weights(self, model_path, state_dict, strict)`
- `iterate_weights(self, model_path)`

### `IncrementalShardLoader`

Incremental shard loading with memory management.

BEYOND vLLM: Load shards incrementally with configurable memory budget,
evicting old shards as new ones are loaded.

**Methods** (4):
- `__init__(self, base_loader, memory_budget_mb, cache_size)`
- `_evict_if_needed(self)`
- `load_shard(self, shard_file)`
- `load_weights_incremental(self, model_path, callback)`

### `AsyncShardLoader`

Asynchronous shard loading with prefetching.

BEYOND vLLM: Prefetch next shards while processing current shard
for improved throughput on I/O-bound operations.

**Methods** (4):
- `__init__(self, base_loader, prefetch_count, max_workers)`
- `_load_file(self, file_path)`
- `_start_prefetch(self, file_paths)`
- `load_weights_async(self, model_path)`

## Functions (2)

### `compute_shard_assignment_rust(num_params, num_ranks, param_sizes)`

Compute optimal shard assignment using Rust.

### `validate_shard_shapes_rust(shard_specs, rank, world_size)`

Validate shard shapes using Rust.

## Dependencies

**Imports** (35):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `concurrent.futures`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `glob`
- `numpy`
- `os`
- `pathlib.Path`
- `re`
- `rust_core`
- ... and 20 more

---
*Auto-generated documentation*
