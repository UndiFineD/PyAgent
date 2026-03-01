# Class Breakdown: types

**File**: `src\infrastructure\storage\kv_transfer\arc\types.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `OffloadMedium`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Storage medium for offloaded blocks.

[TIP] **Suggested split**: Move to `offloadmedium.py`

---

### 2. `BlockState`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

State of an offloaded block.

[TIP] **Suggested split**: Move to `blockstate.py`

---

### 3. `BlockStatus`

**Line**: 50  
**Methods**: 2

Status of a cached block.

[TIP] **Suggested split**: Move to `blockstatus.py`

---

### 4. `LoadStoreSpec`

**Line**: 74  
**Methods**: 0

Specification for load/store operation.

[TIP] **Suggested split**: Move to `loadstorespec.py`

---

### 5. `OffloadingEvent`

**Line**: 84  
**Methods**: 0

Event representing offloading operation.

[TIP] **Suggested split**: Move to `offloadingevent.py`

---

### 6. `PrepareStoreOutput`

**Line**: 95  
**Methods**: 0

Output from prepare_store operation.

[TIP] **Suggested split**: Move to `preparestoreoutput.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
