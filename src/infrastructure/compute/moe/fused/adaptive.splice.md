# Class Breakdown: adaptive

**File**: `src\infrastructure\compute\moe\fused\adaptive.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AdaptiveMoELayer`

**Line**: 27  
**Inherits**: FusedMoELayer  
**Methods**: 2

Adaptive MoE layer with dynamic top-k selection and capacity management.

[TIP] **Suggested split**: Move to `adaptivemoelayer.py`

---

### 2. `HierarchicalMoELayer`

**Line**: 64  
**Methods**: 3

Two-level hierarchical MoE for extreme scale.

[TIP] **Suggested split**: Move to `hierarchicalmoelayer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
