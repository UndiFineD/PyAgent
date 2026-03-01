# Class Breakdown: MemorySnapshot

**File**: `src\observability\stats\MemorySnapshot.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MemorySnapshot`

**Line**: 22  
**Methods**: 2

Snapshot of memory usage at a point in time.

Tracks Python, system, and optionally GPU memory.

[TIP] **Suggested split**: Move to `memorysnapshot.py`

---

### 2. `MemoryProfiler`

**Line**: 126  
**Methods**: 5

Context manager for profiling memory usage.

Example:
    >>> with MemoryProfiler("model_load") as profiler:
    ...     model = load_model()
    >>> print(profiler.report())

[TIP] **Suggested split**: Move to `memoryprofiler.py`

---

### 3. `GCDebugger`

**Line**: 190  
**Methods**: 9

Garbage collection debugger for production monitoring.

Inspired by vLLM's GCDebugger for tracking GC activity.

Example:
    >>> debugger = GCDebugger()
    >>> debugger.start()
    >>> # ... run cod...

[TIP] **Suggested split**: Move to `gcdebugger.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
