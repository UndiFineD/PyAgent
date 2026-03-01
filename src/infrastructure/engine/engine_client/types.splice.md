# Class Breakdown: types

**File**: `src\infrastructure\engine\engine_client\types.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ClientMode`

**Line**: 28  
**Inherits**: Enum  
**Methods**: 0

Engine client execution mode.

[TIP] **Suggested split**: Move to `clientmode.py`

---

### 2. `WorkerState`

**Line**: 37  
**Inherits**: Enum  
**Methods**: 0

Worker health state.

[TIP] **Suggested split**: Move to `workerstate.py`

---

### 3. `EngineClientConfig`

**Line**: 47  
**Methods**: 0

Configuration for engine client.

[TIP] **Suggested split**: Move to `engineclientconfig.py`

---

### 4. `SchedulerOutput`

**Line**: 61  
**Methods**: 0

Output from scheduler for engine core.

[TIP] **Suggested split**: Move to `scheduleroutput.py`

---

### 5. `EngineOutput`

**Line**: 73  
**Methods**: 0

Output from engine core execution.

[TIP] **Suggested split**: Move to `engineoutput.py`

---

### 6. `WorkerInfo`

**Line**: 85  
**Methods**: 0

Worker metadata and health.

[TIP] **Suggested split**: Move to `workerinfo.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
