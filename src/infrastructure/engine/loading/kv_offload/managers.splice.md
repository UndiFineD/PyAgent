# Class Breakdown: managers

**File**: `src\infrastructure\engine\loading\kv_offload\managers.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LRUOffloadingManager`

**Line**: 42  
**Inherits**: OffloadingManager  
**Methods**: 8

LRU-based offloading manager.

vLLM Pattern: LRUOffloadingManager from lru_manager.py
Evicts blocks by least recently used order.

[TIP] **Suggested split**: Move to `lruoffloadingmanager.py`

---

### 2. `ARCOffloadingManager`

**Line**: 189  
**Inherits**: OffloadingManager  
**Methods**: 10

ARC (Adaptive Replacement Cache) offloading manager.

vLLM Pattern: ARCOffloadingManager from arc_manager.py
Dynamically balances recency vs frequency regarding eviction decisions.

[TIP] **Suggested split**: Move to `arcoffloadingmanager.py`

---

### 3. `TieredOffloadManager`

**Line**: 409  
**Inherits**: OffloadingManager  
**Methods**: 9

Tiered offloading with multiple backends (GPU→CPU→NVMe).

[TIP] **Suggested split**: Move to `tieredoffloadmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
