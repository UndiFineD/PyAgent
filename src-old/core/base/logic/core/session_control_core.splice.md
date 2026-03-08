# Class Breakdown: session_control_core

**File**: `src\core\base\logic\core\session_control_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SessionSignal`

**Line**: 20  
**Inherits**: Enum  
**Methods**: 0

Signals for agent session lifecycle control.

[TIP] **Suggested split**: Move to `sessionsignal.py`

---

### 2. `SessionControlCore`

**Line**: 27  
**Methods**: 6

Manages session interrupt signals and shared state flags for long-running agent tasks.
Enables orchestration layers to pause or stop agents mid-loop via filesystem or shared memory flags.
Lesson harve...

[TIP] **Suggested split**: Move to `sessioncontrolcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
