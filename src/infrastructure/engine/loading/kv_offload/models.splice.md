# Class Breakdown: models

**File**: `src\infrastructure\engine\loading\kv_offload\models.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `OffloadMedium`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Storage medium types for offloading.

[TIP] **Suggested split**: Move to `offloadmedium.py`

---

### 2. `LoadStoreSpec`

**Line**: 41  
**Methods**: 1

Specification for load/store operations.

[TIP] **Suggested split**: Move to `loadstorespec.py`

---

### 3. `BlockStatus`

**Line**: 56  
**Methods**: 1

Status of an offloaded block.

[TIP] **Suggested split**: Move to `blockstatus.py`

---

### 4. `OffloadingEvent`

**Line**: 71  
**Methods**: 0

Event for block offloading operations.

[TIP] **Suggested split**: Move to `offloadingevent.py`

---

### 5. `PrepareStoreOutput`

**Line**: 81  
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
