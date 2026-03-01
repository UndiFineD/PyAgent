# Class Breakdown: orchestrator_registry

**File**: `src\infrastructure\swarm\fleet\orchestrator_registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LazyOrchestratorMap`

**Line**: 41  
**Methods**: 8

A dictionary-like object that instantiates orchestrators only when accessed.

[TIP] **Suggested split**: Move to `lazyorchestratormap.py`

---

### 2. `OrchestratorRegistry`

**Line**: 228  
**Methods**: 1

Registry for mapping agent types to their corresponding orchestrators.

[TIP] **Suggested split**: Move to `orchestratorregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
