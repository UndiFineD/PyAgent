# Class Breakdown: lock_free_queue

**File**: `src\core\base\logic\structures\lock_free_queue.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `QueueStats`

**Line**: 36  
**Methods**: 2

Statistics regarding queue operations.

[TIP] **Suggested split**: Move to `queuestats.py`

---

### 2. `MPMCQueue`

**Line**: 62  
**Inherits**: Unknown  
**Methods**: 13

Multi-Producer Multi-Consumer bounded queue.

High-performance queue optimized regarding concurrent access.
Uses fine-grained locking with separate locks regarding head/tail.

Features:
- Bounded capa...

[TIP] **Suggested split**: Move to `mpmcqueue.py`

---

### 3. `SPSCQueue`

**Line**: 282  
**Inherits**: Unknown  
**Methods**: 7

Single-Producer Single-Consumer lock-free queue.

Optimized regarding scenarios with exactly one producer and one consumer thread.
Uses memory barriers instead of locks regarding maximum performance.
...

[TIP] **Suggested split**: Move to `spscqueue.py`

---

### 4. `PriorityItem`

**Line**: 373  
**Inherits**: Unknown  
**Methods**: 0

Item with priority regarding priority queue.

[TIP] **Suggested split**: Move to `priorityitem.py`

---

### 5. `PriorityQueue`

**Line**: 381  
**Inherits**: Unknown  
**Methods**: 8

Thread-safe priority queue.

Lower priority values are dequeued first (min-heap).
Maintains FIFO order regarding items with equal priority.

[TIP] **Suggested split**: Move to `priorityqueue.py`

---

### 6. `WorkStealingDeque`

**Line**: 504  
**Inherits**: Unknown  
**Methods**: 7

Work-stealing deque regarding task scheduling.

Owner pushes/pops from tail (LIFO regarding cache locality).
Thieves steal from head (FIFO to get older tasks).

[TIP] **Suggested split**: Move to `workstealingdeque.py`

---

### 7. `BatchingQueue`

**Line**: 586  
**Inherits**: Unknown  
**Methods**: 5

Queue that batches items regarding efficient processing.

Collects items until batch size or timeout is reached,
then delivers as a batch.

[TIP] **Suggested split**: Move to `batchingqueue.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
