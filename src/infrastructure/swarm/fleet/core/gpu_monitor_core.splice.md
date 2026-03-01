# Class Breakdown: gpu_monitor_core

**File**: `src\infrastructure\swarm\fleet\core\gpu_monitor_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GPUMetrics`

**Line**: 25  
**Methods**: 1

Pure data class for GPU telemetry.

[TIP] **Suggested split**: Move to `gpumetrics.py`

---

### 2. `GPUMonitorCore`

**Line**: 45  
**Methods**: 3

Pure logic for GPU health and pressure calculation.
Complies with Core/Shell pattern (Side-effect free).

[TIP] **Suggested split**: Move to `gpumonitorcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
