# Class Breakdown: k_vzap

**File**: `src\infrastructure\storage\kv_transfer\k_vzap.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `KVzapConfig`

**Line**: 29  
**Methods**: 0

Configuration for KVzap pruning.

[TIP] **Suggested split**: Move to `kvzapconfig.py`

---

### 2. `KVzapSurrogate`

**Line**: 40  
**Inherits**: Module  
**Methods**: 2

Lightweight surrogate model to predict KV importance scores from hidden states.
Efficiently predicts which tokens can be safely pruned from the cache.

[TIP] **Suggested split**: Move to `kvzapsurrogate.py`

---

### 3. `KVzapPruner`

**Line**: 65  
**Methods**: 4

Orchestrates KV cache pruning using the surrogate model.

[TIP] **Suggested split**: Move to `kvzappruner.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
