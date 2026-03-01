# Class Breakdown: debugging

**File**: `src\infrastructure\services\dev\agent_tests\debugging.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExecutionReplayer`

**Line**: 41  
**Methods**: 7

Replay test execution for debugging.

[TIP] **Suggested split**: Move to `executionreplayer.py`

---

### 2. `TestProfiler`

**Line**: 126  
**Methods**: 6

Runtime profiling for tests.

[TIP] **Suggested split**: Move to `testprofiler.py`

---

### 3. `TestRecorder`

**Line**: 190  
**Methods**: 5

Records test execution.

[TIP] **Suggested split**: Move to `testrecorder.py`

---

### 4. `TestReplayer`

**Line**: 227  
**Methods**: 1

Replays recorded tests.

[TIP] **Suggested split**: Move to `testreplayer.py`

---

### 5. `Recording`

**Line**: 199  
**Methods**: 0

A recording of test actions.

[TIP] **Suggested split**: Move to `recording.py`

---

### 6. `ReplayResult`

**Line**: 231  
**Methods**: 0

Result of a test replay.

[TIP] **Suggested split**: Move to `replayresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
