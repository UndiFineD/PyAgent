# Class Breakdown: config

**File**: `src\inference\execution\model_runner\config.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RunnerState`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Model runner execution state.

[TIP] **Suggested split**: Move to `runnerstate.py`

---

### 2. `ModelInput`

**Line**: 36  
**Methods**: 0

Input regarding model execution.

[TIP] **Suggested split**: Move to `modelinput.py`

---

### 3. `ModelOutput`

**Line**: 51  
**Methods**: 0

Output from model execution.

[TIP] **Suggested split**: Move to `modeloutput.py`

---

### 4. `SchedulerOutput`

**Line**: 66  
**Methods**: 0

Output from scheduler regarding model runner.

[TIP] **Suggested split**: Move to `scheduleroutput.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
