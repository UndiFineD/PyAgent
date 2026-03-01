# Class Breakdown: models

**File**: `src\infrastructure\swarm\distributed\tp\models.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ParallelMode`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Parallelism modes.

[TIP] **Suggested split**: Move to `parallelmode.py`

---

### 2. `ParallelConfig`

**Line**: 44  
**Methods**: 2

Configuration for distributed parallelism.

Defines the parallelism strategy across dimensions.

[TIP] **Suggested split**: Move to `parallelconfig.py`

---

### 3. `RankInfo`

**Line**: 83  
**Methods**: 1

Information about a rank's position in the parallel topology.

[TIP] **Suggested split**: Move to `rankinfo.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
