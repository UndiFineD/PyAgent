# Class Breakdown: config

**File**: `src\infrastructure\engine\core\config.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestStatus`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Status of a request in the engine.

[TIP] **Suggested split**: Move to `requeststatus.py`

---

### 2. `FinishReason`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Reason why a request finished.

[TIP] **Suggested split**: Move to `finishreason.py`

---

### 3. `Request`

**Line**: 47  
**Methods**: 3

A request to be processed by the engine.

[TIP] **Suggested split**: Move to `request.py`

---

### 4. `SchedulerOutput`

**Line**: 77  
**Methods**: 1

Output from the scheduler containing batch info.

[TIP] **Suggested split**: Move to `scheduleroutput.py`

---

### 5. `ModelRunnerOutput`

**Line**: 93  
**Methods**: 1

Output from the model runner.

[TIP] **Suggested split**: Move to `modelrunneroutput.py`

---

### 6. `EngineCoreOutput`

**Line**: 110  
**Methods**: 0

Output for a single request.

[TIP] **Suggested split**: Move to `enginecoreoutput.py`

---

### 7. `EngineCoreOutputs`

**Line**: 122  
**Methods**: 0

Batch of outputs from the engine core.

[TIP] **Suggested split**: Move to `enginecoreoutputs.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
