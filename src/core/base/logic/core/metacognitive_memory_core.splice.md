# Class Breakdown: metacognitive_memory_core

**File**: `src\core\base\logic\core\metacognitive_memory_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MemoryItem`

**Line**: 19  
**Inherits**: BaseModel  
**Methods**: 0

[TIP] **Suggested split**: Move to `memoryitem.py`

---

### 2. `MetacognitiveMemoryCore`

**Line**: 24  
**Methods**: 2

Core logic for agents to manage their own session memory using tool calls.
Harvested from .external/agno

[TIP] **Suggested split**: Move to `metacognitivememorycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
