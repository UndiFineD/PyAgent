# Class Breakdown: enums

**File**: `src\infrastructure\engine\lifecycle\enums.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FinishReason`

**Line**: 27  
**Inherits**: IntEnum  
**Methods**: 2

Reason a request finished - stop, length, abort, or error.

Attributes:
    STOP: A stop string or token was emitted
    LENGTH: max_tokens was consumed, or max_model_len was reached
    ABORT: Aborte...

[TIP] **Suggested split**: Move to `finishreason.py`

---

### 2. `RequestStatus`

**Line**: 51  
**Inherits**: IntEnum  
**Methods**: 4

Status of a request in the engine.

States before PREEMPTED are considered "active" (not finished).
States after PREEMPTED are considered "finished".

[TIP] **Suggested split**: Move to `requeststatus.py`

---

### 3. `RequestEventType`

**Line**: 146  
**Inherits**: Enum  
**Methods**: 0

Types of request lifecycle events.

[TIP] **Suggested split**: Move to `requesteventtype.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
