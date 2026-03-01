# Class Breakdown: hopper_sim

**File**: `src\infrastructure\services\simulation\hopper_sim.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Precision`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Floating point precision modes for simulation.

[TIP] **Suggested split**: Move to `precision.py`

---

### 2. `HopperConfig`

**Line**: 46  
**Methods**: 0

NVIDIA H100 SXM5 specifications.

[TIP] **Suggested split**: Move to `hopperconfig.py`

---

### 3. `HopperSim`

**Line**: 56  
**Methods**: 4

Simulates Hopper architecture performance for GEMM operations.

[TIP] **Suggested split**: Move to `hoppersim.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
