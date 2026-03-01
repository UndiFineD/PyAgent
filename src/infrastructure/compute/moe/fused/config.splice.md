# Class Breakdown: config

**File**: `src\infrastructure\compute\moe\fused\config.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExpertPlacementStrategy`

**Line**: 25  
**Inherits**: str, Enum  
**Methods**: 0

Strategy for placing experts across devices.

[TIP] **Suggested split**: Move to `expertplacementstrategy.py`

---

### 2. `MoEQuantMethod`

**Line**: 34  
**Inherits**: str, Enum  
**Methods**: 0

Quantization methods for MoE weights.

[TIP] **Suggested split**: Move to `moequantmethod.py`

---

### 3. `FusedMoEConfig`

**Line**: 45  
**Methods**: 1

Configuration for a Fused MoE layer.

[TIP] **Suggested split**: Move to `fusedmoeconfig.py`

---

### 4. `FusedMoEParallelConfig`

**Line**: 67  
**Methods**: 0

Parallelization configuration for MoE.

[TIP] **Suggested split**: Move to `fusedmoeparallelconfig.py`

---

### 5. `FusedMoEQuantConfig`

**Line**: 80  
**Methods**: 0

Quantization configuration for MoE.

[TIP] **Suggested split**: Move to `fusedmoequantconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
