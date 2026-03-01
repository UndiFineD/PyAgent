# Class Breakdown: Storage

**File**: `src\infrastructure\attention\paged_attention\Storage.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BlockTable`

**Line**: 9  
**Methods**: 6

Manages physical block allocation for sequences.

[TIP] **Suggested split**: Move to `blocktable.py`

---

### 2. `SlotMapping`

**Line**: 43  
**Methods**: 3

Maps tokens to (block_idx, block_offset) slots.

[TIP] **Suggested split**: Move to `slotmapping.py`

---

### 3. `PagedKVCache`

**Line**: 67  
**Methods**: 4

Block-organized key/value cache.

[TIP] **Suggested split**: Move to `pagedkvcache.py`

---

### 4. `AttentionMetadata`

**Line**: 105  
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
