# Class Breakdown: manager

**File**: `src\infrastructure\storage\kv_transfer\arc\manager.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ARCOffloadManager`

**Line**: 41  
**Inherits**: OffloadingManager  
**Methods**: 12

ARC (Adaptive Replacement Cache) offloading manager.

Implements the ARC eviction policy which adaptively balances
recency (T1) and frequency (T2) based on workload patterns.

[TIP] **Suggested split**: Move to `arcoffloadmanager.py`

---

### 2. `AdaptiveARCManager`

**Line**: 304  
**Inherits**: ARCOffloadManager  
**Methods**: 6

ARC manager with enhanced adaptation features.

[TIP] **Suggested split**: Move to `adaptivearcmanager.py`

---

### 3. `AsyncARCManager`

**Line**: 384  
**Methods**: 1

Async wrapper for ARC offloading manager.

[TIP] **Suggested split**: Move to `asyncarcmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
