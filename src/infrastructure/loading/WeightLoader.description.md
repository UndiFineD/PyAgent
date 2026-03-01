# WeightLoader

**File**: `src\infrastructure\loading\WeightLoader.py`  
**Type**: Python Module  
**Summary**: 9 classes, 6 functions, 37 imports  
**Lines**: 572  
**Complexity**: 32 (complex)

## Overview

Weight Loading Utilities for PyAgent

This module provides comprehensive weight loading functionality inspired by
vLLM's weight_utils.py, with significant enhancements for parallel loading,
streaming, and cross-format support.

Key Features:
- Multi-threaded safetensor loading
- Atomic file writing for safe checkpointing  
- Streaming weight loading for memory efficiency
- Format detection and conversion
- BEYOND vLLM: Predictive prefetching, adaptive batch sizing

vLLM Patterns:
- multi_thread_safetensors_weights_iterator
- atomic_writer context manager
- safetensors_weights_iterator (eager/lazy)
- fastsafetensors_weights_iterator
- runai_safetensors_weights_iterator

## Classes (9)

### `WeightFormat`

**Inherits from**: Enum

Supported weight file formats.

### `WeightSpec`

Specification for a weight tensor.

**Methods** (2):
- `__hash__(self)`
- `numel(self)`

### `LoadStats`

Statistics for weight loading.

**Methods** (1):
- `throughput_gbps(self)`

### `AtomicWriter`

Context manager for atomic file writing.

Writes to a temporary file first, then atomically replaces the target.
This ensures the target file is never left in a corrupted state.

vLLM Pattern: atomic_writer from weight_utils.py

**Methods** (3):
- `__init__(self, filepath, mode, encoding)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`

### `WeightLoader`

**Inherits from**: ABC

Abstract base class for weight loaders.

Defines the interface for loading model weights from various sources.

**Methods** (3):
- `iterate_weights(self, file_paths, device)`
- `get_weight_specs(self, file_paths)`
- `load_weights(self, file_paths, device)`

### `SafetensorsLoader`

**Inherits from**: WeightLoader

Loader for safetensors files.

Supports lazy (default) and eager loading strategies.
vLLM Pattern: safetensors_weights_iterator

**Methods** (3):
- `__init__(self, strategy)`
- `iterate_weights(self, file_paths, device)`
- `get_weight_specs(self, file_paths)`

### `MultiThreadWeightLoader`

**Inherits from**: WeightLoader

Multi-threaded weight loader for parallel file loading.

vLLM Pattern: multi_thread_safetensors_weights_iterator
BEYOND vLLM: Adaptive worker count based on file count/size

**Methods** (6):
- `__init__(self, max_workers, adaptive_workers, min_file_size_per_worker)`
- `_get_optimal_workers(self, file_paths)`
- `_load_file(self, file_path, device)`
- `iterate_weights(self, file_paths, device)`
- `get_weight_specs(self, file_paths)`
- `stats(self)`

### `FastSafetensorsLoader`

**Inherits from**: WeightLoader

Fast safetensors loader using GPU direct storage.

vLLM Pattern: fastsafetensors_weights_iterator
Uses fastsafetensors library for direct GPU loading with GDS support.

**Methods** (3):
- `__init__(self, use_gds)`
- `iterate_weights(self, file_paths, device)`
- `get_weight_specs(self, file_paths)`

### `StreamingWeightLoader`

**Inherits from**: WeightLoader

Streaming weight loader for memory-constrained environments.

BEYOND vLLM: Loads weights in batches with configurable memory budget,
supports predictive prefetching and priority-based loading.

**Methods** (5):
- `__init__(self, memory_budget_mb, prefetch_count, priority_weights)`
- `_get_tensor_size(self, tensor)`
- `_should_prefetch(self, name)`
- `iterate_weights(self, file_paths, device)`
- `get_weight_specs(self, file_paths)`

## Functions (6)

### `atomic_writer(filepath, mode, encoding)`

Functional context manager for atomic file writing.

vLLM Pattern: atomic_writer context manager

### `detect_weight_format(file_path)`

Detect weight file format from extension and magic bytes.

### `get_file_lock_path(model_name_or_path, cache_dir)`

Generate a lock file path for model downloads.

### `compute_weight_hash_rust(data)`

Fast weight data hashing using Rust xxHash.

### `validate_weight_shapes_rust(specs, expected)`

Validate weight shapes match expected using Rust.

### `filter_shared_tensors(tensors)`

Filter out tensors that share storage.

vLLM Pattern: _shared_pointers from weight_utils.py
Keeps only one tensor per shared storage to avoid duplicates.

## Dependencies

**Imports** (37):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.defaultdict`
- `concurrent.futures`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `fastsafetensors.SafeTensorsFileLoader`
- `hashlib`
- `json`
- `numpy`
- `os`
- ... and 22 more

---
*Auto-generated documentation*
