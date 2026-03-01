# Class Breakdown: messages

**File**: `src\infrastructure\swarm\orchestration\core\distributed\messages.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CoordinatorMessage`

**Line**: 30  
**Methods**: 0

Base message type for coordinator communication.

[TIP] **Suggested split**: Move to `coordinatormessage.py`

---

### 2. `RequestMessage`

**Line**: 38  
**Inherits**: CoordinatorMessage  
**Methods**: 0

Request message sent to workers.

[TIP] **Suggested split**: Move to `requestmessage.py`

---

### 3. `ResponseMessage`

**Line**: 47  
**Inherits**: CoordinatorMessage  
**Methods**: 0

Response message from workers.

[TIP] **Suggested split**: Move to `responsemessage.py`

---

### 4. `ControlMessage`

**Line**: 57  
**Inherits**: CoordinatorMessage  
**Methods**: 0

Control message for worker management.

[TIP] **Suggested split**: Move to `controlmessage.py`

---

### 5. `MetricsMessage`

**Line**: 65  
**Inherits**: CoordinatorMessage  
**Methods**: 0

Metrics message from workers.

[TIP] **Suggested split**: Move to `metricsmessage.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
