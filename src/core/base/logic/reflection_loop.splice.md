# Class Breakdown: reflection_loop

**File**: `src\core\base\logic\reflection_loop.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReflectionResult`

**Line**: 39  
**Inherits**: BaseModel  
**Methods**: 0

Result of a reflection iteration.

[TIP] **Suggested split**: Move to `reflectionresult.py`

---

### 2. `ReflectionLoopConfig`

**Line**: 49  
**Inherits**: BaseModel  
**Methods**: 0

Configuration for reflection loop execution.

[TIP] **Suggested split**: Move to `reflectionloopconfig.py`

---

### 3. `ReflectionContext`

**Line**: 65  
**Methods**: 0

Context maintained throughout the reflection loop.

[TIP] **Suggested split**: Move to `reflectioncontext.py`

---

### 4. `ReflectionAgent`

**Line**: 74  
**Inherits**: ABC  
**Methods**: 0

Abstract base class for agents that can participate in reflection loops.

[TIP] **Suggested split**: Move to `reflectionagent.py`

---

### 5. `LLMReflectionAgent`

**Line**: 88  
**Inherits**: ReflectionAgent  
**Methods**: 1

LLM-based reflection agent using any LLM provider.

[TIP] **Suggested split**: Move to `llmreflectionagent.py`

---

### 6. `CodeReflectionAgent`

**Line**: 119  
**Inherits**: LLMReflectionAgent  
**Methods**: 1

Specialized agent for code reflection and improvement.

[TIP] **Suggested split**: Move to `codereflectionagent.py`

---

### 7. `ReflectionLoopOrchestrator`

**Line**: 181  
**Methods**: 4

Orchestrates the reflection loop process.

[TIP] **Suggested split**: Move to `reflectionlooporchestrator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
