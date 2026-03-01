# Class Breakdown: CUDAGraphConfig

**File**: `src\infrastructure\execution\CUDAGraphConfig.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CUDAGraphMode`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

CUDA graph execution modes.

Based on vLLM's CUDAGraphMode enum.

[TIP] **Suggested split**: Move to `cudagraphmode.py`

---

### 2. `CUDAGraphConfig`

**Line**: 46  
**Methods**: 5

Configuration for CUDA graph capture and replay.

Based on vLLM's compilation config patterns.

[TIP] **Suggested split**: Move to `cudagraphconfig.py`

---

### 3. `CUDAGraphEntry`

**Line**: 132  
**Methods**: 3

A captured CUDA graph entry.

Stores the graph and associated metadata.

[TIP] **Suggested split**: Move to `cudagraphentry.py`

---

### 4. `CUDAGraphRegistry`

**Line**: 194  
**Methods**: 8

Registry for captured CUDA graphs.

Manages graph capture, storage, and lookup.

[TIP] **Suggested split**: Move to `cudagraphregistry.py`

---

### 5. `CUDAGraphManager`

**Line**: 344  
**Methods**: 11

High-level manager for CUDA graph operations.

Provides convenient interface for graph capture and replay.

[TIP] **Suggested split**: Move to `cudagraphmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
