# Class Breakdown: types

**File**: `src\infrastructure\services\metrics\lora\types.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoRALoadState`

**Line**: 28  
**Inherits**: Enum  
**Methods**: 0

State of a LoRA adapter.

[TIP] **Suggested split**: Move to `loraloadstate.py`

---

### 2. `RequestStatus`

**Line**: 38  
**Inherits**: Enum  
**Methods**: 0

Status of a request in the system.

[TIP] **Suggested split**: Move to `requeststatus.py`

---

### 3. `LoRAAdapterInfo`

**Line**: 50  
**Methods**: 1

Information about a LoRA adapter.

[TIP] **Suggested split**: Move to `loraadapterinfo.py`

---

### 4. `LoRARequestState`

**Line**: 70  
**Methods**: 4

State of a LoRA request.

Tracks per-request LoRA adapter usage and timing.

[TIP] **Suggested split**: Move to `lorarequeststate.py`

---

### 5. `LoRAStats`

**Line**: 118  
**Methods**: 0

Aggregate statistics for LoRA operations.

[TIP] **Suggested split**: Move to `lorastats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
