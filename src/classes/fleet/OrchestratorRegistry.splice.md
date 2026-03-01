# Class Breakdown: OrchestratorRegistry

**File**: `src\classes\fleet\OrchestratorRegistry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LazyOrchestratorMap`

**Line**: 16  
**Methods**: 7

A dictionary-like object that instantiates orchestrators only when accessed.

[TIP] **Suggested split**: Move to `lazyorchestratormap.py`

---

### 2. `OrchestratorRegistry`

**Line**: 140  
**Methods**: 1

[TIP] **Suggested split**: Move to `orchestratorregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
