# Class Breakdown: storage

**File**: `src\infrastructure\engine\attention\paged_attention\storage.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BlockTable`

**Line**: 28  
**Methods**: 6

Manages physical block allocation for sequences.

[TIP] **Suggested split**: Move to `blocktable.py`

---

### 2. `SlotMapping`

**Line**: 72  
**Methods**: 3

Maps tokens to (block_idx, block_offset) slots.

[TIP] **Suggested split**: Move to `slotmapping.py`

---

### 3. `PagedKVCache`

**Line**: 100  
**Methods**: 4

Block-organized key/value cache.

[TIP] **Suggested split**: Move to `pagedkvcache.py`

---

### 4. `AttentionMetadata`

**Line**: 145  
**Methods**: 3

Metadata for batched attention computation.

[TIP] **Suggested split**: Move to `attentionmetadata.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
