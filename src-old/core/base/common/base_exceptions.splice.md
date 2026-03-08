# Class Breakdown: base_exceptions

**File**: `src\core\base\common\base_exceptions.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PyAgentException`

**Line**: 20  
**Inherits**: Exception  
**Methods**: 1

Base exception for all PyAgent errors.

[TIP] **Suggested split**: Move to `pyagentexception.py`

---

### 2. `InfrastructureError`

**Line**: 29  
**Inherits**: PyAgentException  
**Methods**: 0

Errors related to system infrastructure (I/O, Network).

[TIP] **Suggested split**: Move to `infrastructureerror.py`

---

### 3. `LogicError`

**Line**: 33  
**Inherits**: PyAgentException  
**Methods**: 0

Errors related to agent logic or reasoning failure.

[TIP] **Suggested split**: Move to `logicerror.py`

---

### 4. `SecurityError`

**Line**: 37  
**Inherits**: PyAgentException  
**Methods**: 0

Errors related to unauthorized access or safety violations.

[TIP] **Suggested split**: Move to `securityerror.py`

---

### 5. `ModelError`

**Line**: 41  
**Inherits**: PyAgentException  
**Methods**: 0

Errors related to LLM connectivity or output parsing.

[TIP] **Suggested split**: Move to `modelerror.py`

---

### 6. `ConfigurationError`

**Line**: 45  
**Inherits**: PyAgentException  
**Methods**: 0

Errors in settings or manifest validation.

[TIP] **Suggested split**: Move to `configurationerror.py`

---

### 7. `CycleInterrupt`

**Line**: 49  
**Inherits**: PyAgentException  
**Methods**: 0

Interruption of an agent cycle (e.g., quota exceeded).

[TIP] **Suggested split**: Move to `cycleinterrupt.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
