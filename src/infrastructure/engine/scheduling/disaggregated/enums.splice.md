# Class Breakdown: enums

**File**: `src\infrastructure\engine\scheduling\disaggregated\enums.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `InstanceRole`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Role of a vLLM instance in disaggregated serving.

[TIP] **Suggested split**: Move to `instancerole.py`

---

### 2. `SchedulingPolicy`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Request routing policy for multi-instance deployment.

[TIP] **Suggested split**: Move to `schedulingpolicy.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
