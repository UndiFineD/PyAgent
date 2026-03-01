# Class Breakdown: self_healing_engine_core

**File**: `src\infrastructure\swarm\orchestration\healing\self_healing_engine_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FailureType`

**Line**: 35  
**Methods**: 0

Enumeration of swarm failure types.

[TIP] **Suggested split**: Move to `failuretype.py`

---

### 2. `SelfHealingEngineCore`

**Line**: 46  
**Methods**: 2

Pure logic for self-healing analysis.
Decides what kind of fix is needed based on the traceback.

[TIP] **Suggested split**: Move to `selfhealingenginecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
