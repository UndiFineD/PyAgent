# MemorySnapshot

**File**: `src\observability\stats\MemorySnapshot.py`  
**Type**: Python Module  
**Summary**: 3 classes, 5 functions, 15 imports  
**Lines**: 352  
**Complexity**: 21 (complex)

## Overview

MemorySnapshot - Device memory profiling with GC tracking.

Inspired by vLLM's mem_utils.py and gc_utils.py patterns for production
memory monitoring and garbage collection optimization.

Phase 17: vLLM Pattern Integration

## Classes (3)

### `MemorySnapshot`

Snapshot of memory usage at a point in time.

Tracks Python, system, and optionally GPU memory.

**Methods** (2):
- `delta(self, other)`
- `to_dict(self)`

### `MemoryProfiler`

Context manager for profiling memory usage.

Example:
    >>> with MemoryProfiler("model_load") as profiler:
    ...     model = load_model()
    >>> print(profiler.report())

**Methods** (5):
- `__init__(self, name, include_gpu)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `delta(self)`
- `report(self)`

### `GCDebugger`

Garbage collection debugger for production monitoring.

Inspired by vLLM's GCDebugger for tracking GC activity.

Example:
    >>> debugger = GCDebugger()
    >>> debugger.start()
    >>> # ... run code ...
    >>> debugger.stop()
    >>> print(debugger.report())

**Methods** (9):
- `__init__(self, log_collections)`
- `start(self)`
- `stop(self)`
- `_gc_callback(self, phase, info)`
- `force_collection(self, generation)`
- `get_top_objects(self, n)`
- `report(self)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`

## Functions (5)

### `capture_memory_snapshot(include_gpu)`

Capture a complete memory snapshot.

Args:
    include_gpu: Whether to capture GPU memory (requires torch)
    
Returns:
    MemorySnapshot with current memory state

### `memory_profile(name, include_gpu)`

Convenience context manager for memory profiling.

Example:
    >>> with memory_profile("data_load") as prof:
    ...     data = load_data()
    >>> print(prof.delta())

### `freeze_gc_heap()`

Freeze the GC heap after initialization.

This marks all current objects as "immortal" to reduce GC overhead.
Should be called after all static/long-lived objects are created.

Returns:
    Number of objects frozen

### `unfreeze_gc_heap()`

Unfreeze the GC heap.

### `gc_stats()`

Get current GC statistics.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `gc`
- `os`
- `psutil`
- `sys`
- `threading`
- `time`
- `torch`
- `tracemalloc`
- `typing.Any`
- `typing.Iterator`
- `typing.Optional`

---
*Auto-generated documentation*
