# Class Breakdown: core

**File**: `src\infrastructure\conversation\context\core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ConversationContext`

**Line**: 28  
**Inherits**: ABC  
**Methods**: 18

Abstract base class for conversation context.

[TIP] **Suggested split**: Move to `conversationcontext.py`

---

### 2. `AgenticContext`

**Line**: 193  
**Inherits**: ConversationContext  
**Methods**: 4

Context for agentic workflows with tool orchestration.

[TIP] **Suggested split**: Move to `agenticcontext.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
