# Class Breakdown: types

**File**: `src\infrastructure\parallel\dp\types.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DPRole`

**Line**: 14  
**Inherits**: Enum  
**Methods**: 0

Data parallel role.

[TIP] **Suggested split**: Move to `dprole.py`

---

### 2. `WorkerHealth`

**Line**: 20  
**Inherits**: Enum  
**Methods**: 0

Worker health status.

[TIP] **Suggested split**: Move to `workerhealth.py`

---

### 3. `LoadBalanceStrategy`

**Line**: 27  
**Inherits**: Enum  
**Methods**: 0

Load balancing strategy.

[TIP] **Suggested split**: Move to `loadbalancestrategy.py`

---

### 4. `DPConfig`

**Line**: 35  
**Methods**: 0

Configuration for data parallel coordinator.

[TIP] **Suggested split**: Move to `dpconfig.py`

---

### 5. `WorkerState`

**Line**: 49  
**Methods**: 1

State of a DP worker.

[TIP] **Suggested split**: Move to `workerstate.py`

---

### 6. `StepState`

**Line**: 67  
**Methods**: 2

State for a single step.

[TIP] **Suggested split**: Move to `stepstate.py`

---

### 7. `WaveState`

**Line**: 86  
**Methods**: 1

State for an execution wave.

[TIP] **Suggested split**: Move to `wavestate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
