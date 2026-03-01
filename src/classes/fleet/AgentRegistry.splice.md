# Class Breakdown: AgentRegistry

**File**: `src\classes\fleet\AgentRegistry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LazyAgentMap`

**Line**: 40  
**Inherits**: dict  
**Methods**: 20

A dictionary that instantiates agents only when they are first accessed.

[TIP] **Suggested split**: Move to `lazyagentmap.py`

---

### 2. `AgentRegistry`

**Line**: 339  
**Methods**: 1

Registry for mapping agent names to their implementations via lazy loading.

[TIP] **Suggested split**: Move to `agentregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
