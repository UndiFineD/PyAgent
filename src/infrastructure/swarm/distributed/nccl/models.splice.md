# Class Breakdown: models

**File**: `src\infrastructure\swarm\distributed\nccl\models.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReduceOp`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

NCCL reduction operations.

[TIP] **Suggested split**: Move to `reduceop.py`

---

### 2. `NCCLConfig`

**Line**: 36  
**Methods**: 0

Configuration for NCCL communicator.

[TIP] **Suggested split**: Move to `ncclconfig.py`

---

### 3. `NCCLStats`

**Line**: 63  
**Methods**: 0

Statistics for NCCL operations.

[TIP] **Suggested split**: Move to `ncclstats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
