# Class Breakdown: method

**File**: `src\infrastructure\compute\moe\fused\method.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FusedMoEMethodBase`

**Line**: 38  
**Inherits**: ABC  
**Methods**: 2

Base class for MoE computation methods.

[TIP] **Suggested split**: Move to `fusedmoemethodbase.py`

---

### 2. `UnquantizedFusedMoEMethod`

**Line**: 62  
**Inherits**: FusedMoEMethodBase  
**Methods**: 4

Unquantized MoE computation method.

[TIP] **Suggested split**: Move to `unquantizedfusedmoemethod.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
