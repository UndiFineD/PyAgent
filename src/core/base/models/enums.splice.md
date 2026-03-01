# Class Breakdown: enums

**File**: `src\core\base\models\enums.py`  
**Classes**: 17

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentState`

**Line**: 20  
**Inherits**: Enum  
**Methods**: 0

Agent lifecycle states.

[TIP] **Suggested split**: Move to `agentstate.py`

---

### 2. `ResponseQuality`

**Line**: 32  
**Inherits**: Enum  
**Methods**: 0

AI response quality levels.

[TIP] **Suggested split**: Move to `responsequality.py`

---

### 3. `EventType`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

Agent event types for hooks.

[TIP] **Suggested split**: Move to `eventtype.py`

---

### 4. `AuthMethod`

**Line**: 50  
**Inherits**: Enum  
**Methods**: 0

Authentication methods for backends.

[TIP] **Suggested split**: Move to `authmethod.py`

---

### 5. `SerializationFormat`

**Line**: 60  
**Inherits**: Enum  
**Methods**: 0

Custom serialization formats.

[TIP] **Suggested split**: Move to `serializationformat.py`

---

### 6. `FilePriority`

**Line**: 69  
**Inherits**: Enum  
**Methods**: 0

File priority levels for request prioritization.

[TIP] **Suggested split**: Move to `filepriority.py`

---

### 7. `InputType`

**Line**: 77  
**Inherits**: Enum  
**Methods**: 0

Input types for multimodal support.

[TIP] **Suggested split**: Move to `inputtype.py`

---

### 8. `AgentType`

**Line**: 86  
**Inherits**: Enum  
**Methods**: 0

Agent type classifications.

[TIP] **Suggested split**: Move to `agenttype.py`

---

### 9. `MessageRole`

**Line**: 94  
**Inherits**: Enum  
**Methods**: 0

Roles for conversation messages.

[TIP] **Suggested split**: Move to `messagerole.py`

---

### 10. `AgentEvent`

**Line**: 100  
**Inherits**: Enum  
**Methods**: 0

Agent event types.

[TIP] **Suggested split**: Move to `agentevent.py`

---

### 11. `AgentExecutionState`

**Line**: 106  
**Inherits**: Enum  
**Methods**: 0

Execution state for an agent run.

[TIP] **Suggested split**: Move to `agentexecutionstate.py`

---

### 12. `AgentPriority`

**Line**: 115  
**Inherits**: Enum  
**Methods**: 0

Priority level for agent execution.

[TIP] **Suggested split**: Move to `agentpriority.py`

---

### 13. `ConfigFormat`

**Line**: 123  
**Inherits**: Enum  
**Methods**: 0

Configuration file format.

[TIP] **Suggested split**: Move to `configformat.py`

---

### 14. `DiffOutputFormat`

**Line**: 130  
**Inherits**: Enum  
**Methods**: 0

Output format for diff preview.

[TIP] **Suggested split**: Move to `diffoutputformat.py`

---

### 15. `HealthStatus`

**Line**: 137  
**Inherits**: Enum  
**Methods**: 0

Health status for components.

[TIP] **Suggested split**: Move to `healthstatus.py`

---

### 16. `LockType`

**Line**: 144  
**Inherits**: Enum  
**Methods**: 0

File locking type.

[TIP] **Suggested split**: Move to `locktype.py`

---

### 17. `RateLimitStrategy`

**Line**: 150  
**Inherits**: Enum  
**Methods**: 0

Rate limiting strategy for API calls.

[TIP] **Suggested split**: Move to `ratelimitstrategy.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
