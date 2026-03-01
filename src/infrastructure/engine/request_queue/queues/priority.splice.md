# Class Breakdown: priority

**File**: `src\infrastructure\engine\request_queue\queues\priority.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PriorityQueue`

**Line**: 32  
**Inherits**: RequestQueue  
**Methods**: 11

Priority queue using heap.

[TIP] **Suggested split**: Move to `priorityqueue.py`

---

### 2. `DeadlineQueue`

**Line**: 93  
**Inherits**: PriorityQueue  
**Methods**: 2

Deadline-aware priority queue.

[TIP] **Suggested split**: Move to `deadlinequeue.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
