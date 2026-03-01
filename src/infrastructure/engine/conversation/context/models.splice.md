# Class Breakdown: models

**File**: `src\infrastructure\engine\conversation\context\models.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ContextState`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Conversation context state.

[TIP] **Suggested split**: Move to `contextstate.py`

---

### 2. `TurnType`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Conversation turn type.

[TIP] **Suggested split**: Move to `turntype.py`

---

### 3. `ToolExecutionPolicy`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

Tool execution policy.

[TIP] **Suggested split**: Move to `toolexecutionpolicy.py`

---

### 4. `TokenMetrics`

**Line**: 62  
**Methods**: 4

Token usage metrics.

[TIP] **Suggested split**: Move to `tokenmetrics.py`

---

### 5. `ConversationTurn`

**Line**: 104  
**Methods**: 2

Single conversation turn.

[TIP] **Suggested split**: Move to `conversationturn.py`

---

### 6. `ToolExecution`

**Line**: 150  
**Methods**: 2

Tool execution record.

[TIP] **Suggested split**: Move to `toolexecution.py`

---

### 7. `ContextConfig`

**Line**: 176  
**Methods**: 1

Context configuration.

[TIP] **Suggested split**: Move to `contextconfig.py`

---

### 8. `ContextSnapshot`

**Line**: 201  
**Methods**: 2

Snapshot of context state.

[TIP] **Suggested split**: Move to `contextsnapshot.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
