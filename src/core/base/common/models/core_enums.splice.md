# Class Breakdown: core_enums

**File**: `src\core\base\common\models\core_enums.py`  
**Classes**: 20

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentState`

**Line**: 22  
**Inherits**: Enum  
**Methods**: 0

Agent lifecycle states.

[TIP] **Suggested split**: Move to `agentstate.py`

---

### 2. `ResponseQuality`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

AI response quality levels.

[TIP] **Suggested split**: Move to `responsequality.py`

---

### 3. `FailureClassification`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

Phase 336: Structured failure taxonomy for collective intelligence.

[TIP] **Suggested split**: Move to `failureclassification.py`

---

### 4. `EventType`

**Line**: 66  
**Inherits**: Enum  
**Methods**: 0

Agent event types for hooks.

[TIP] **Suggested split**: Move to `eventtype.py`

---

### 5. `AuthMethod`

**Line**: 81  
**Inherits**: Enum  
**Methods**: 0

Authentication methods for backends.

[TIP] **Suggested split**: Move to `authmethod.py`

---

### 6. `SerializationFormat`

**Line**: 96  
**Inherits**: Enum  
**Methods**: 0

Custom serialization formats.

[TIP] **Suggested split**: Move to `serializationformat.py`

---

### 7. `FilePriority`

**Line**: 108  
**Inherits**: Enum  
**Methods**: 0

File priority levels for request prioritization.

[TIP] **Suggested split**: Move to `filepriority.py`

---

### 8. `InputType`

**Line**: 118  
**Inherits**: Enum  
**Methods**: 0

Input types for multimodal support.

[TIP] **Suggested split**: Move to `inputtype.py`

---

### 9. `AgentType`

**Line**: 170  
**Inherits**: Enum  
**Methods**: 0

Agent type classifications.

[TIP] **Suggested split**: Move to `agenttype.py`

---

### 10. `MessageRole`

**Line**: 181  
**Inherits**: Enum  
**Methods**: 0

Roles for conversation messages.

[TIP] **Suggested split**: Move to `messagerole.py`

---

### 11. `AgentEvent`

**Line**: 189  
**Inherits**: Enum  
**Methods**: 0

Agent event types.

[TIP] **Suggested split**: Move to `agentevent.py`

---

### 12. `AgentExecutionState`

**Line**: 197  
**Inherits**: Enum  
**Methods**: 0

Execution state for an agent run.

[TIP] **Suggested split**: Move to `agentexecutionstate.py`

---

### 13. `AgentPriority`

**Line**: 208  
**Inherits**: Enum  
**Methods**: 0

Priority level for agent execution.

[TIP] **Suggested split**: Move to `agentpriority.py`

---

### 14. `ConfigFormat`

**Line**: 218  
**Inherits**: Enum  
**Methods**: 0

Configuration file format.

[TIP] **Suggested split**: Move to `configformat.py`

---

### 15. `DiffOutputFormat`

**Line**: 227  
**Inherits**: Enum  
**Methods**: 0

Output format for diff preview.

[TIP] **Suggested split**: Move to `diffoutputformat.py`

---

### 16. `HealthStatus`

**Line**: 236  
**Inherits**: Enum  
**Methods**: 0

Health status for components.

[TIP] **Suggested split**: Move to `healthstatus.py`

---

### 17. `LockType`

**Line**: 245  
**Inherits**: Enum  
**Methods**: 0

File locking type.

[TIP] **Suggested split**: Move to `locktype.py`

---

### 18. `RateLimitStrategy`

**Line**: 253  
**Inherits**: Enum  
**Methods**: 0

Rate limiting strategy for API calls.

[TIP] **Suggested split**: Move to `ratelimitstrategy.py`

---

### 19. `EnvironmentStatus`

**Line**: 262  
**Inherits**: Enum  
**Methods**: 0

Environment instance status.

[TIP] **Suggested split**: Move to `environmentstatus.py`

---

### 20. `EnvironmentIsolation`

**Line**: 273  
**Inherits**: Enum  
**Methods**: 0

Environment isolation levels.

[TIP] **Suggested split**: Move to `environmentisolation.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
