# Class Breakdown: types

**File**: `src\infrastructure\services\executor\multiproc\types.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExecutorBackend`

**Line**: 27  
**Inherits**: Enum  
**Methods**: 0

Executor backend types.

[TIP] **Suggested split**: Move to `executorbackend.py`

---

### 2. `WorkerState`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Worker process states.

[TIP] **Suggested split**: Move to `workerstate.py`

---

### 3. `WorkerInfo`

**Line**: 47  
**Methods**: 0

Information about a worker process.

[TIP] **Suggested split**: Move to `workerinfo.py`

---

### 4. `TaskMessage`

**Line**: 62  
**Methods**: 0

Message for task execution.

[TIP] **Suggested split**: Move to `taskmessage.py`

---

### 5. `ResultMessage`

**Line**: 74  
**Methods**: 0

Message for task result.

[TIP] **Suggested split**: Move to `resultmessage.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
