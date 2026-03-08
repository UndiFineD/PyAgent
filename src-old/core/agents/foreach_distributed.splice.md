# Class Breakdown: foreach_distributed

**File**: `src\core\agents\foreach_distributed.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `WorkerClaimError`

**Line**: 28  
**Inherits**: Exception  
**Methods**: 0

Raised when a worker fails to claim a shard.

[TIP] **Suggested split**: Move to `workerclaimerror.py`

---

### 2. `Worker`

**Line**: 32  
**Methods**: 9

A simple worker that claims a shard, acquires locks, and reports status.

This is a synchronous helper designed for staged runs and unit tests.

[TIP] **Suggested split**: Move to `worker.py`

---

### 3. `Coordinator`

**Line**: 177  
**Methods**: 4

A lightweight coordinator for staged Foreach runs.

The Coordinator reads a manifest describing shards and monitors worker
status files in a scratch area. It will detect stalled workers and emit
simpl...

[TIP] **Suggested split**: Move to `coordinator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
