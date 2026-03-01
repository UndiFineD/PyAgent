# Class Breakdown: Worker

**File**: `src\infrastructure\orchestration\core\distributed\Worker.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BaseWorker`

**Line**: 30  
**Inherits**: ABC  
**Methods**: 5

Abstract base class for distributed workers.

Workers receive requests, process them, and return results.

[TIP] **Suggested split**: Move to `baseworker.py`

---

### 2. `WorkerProcess`

**Line**: 73  
**Methods**: 7

Wrapper for a worker running in a subprocess.

Inspired by vLLM's CoreEngineProc.

[TIP] **Suggested split**: Move to `workerprocess.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
