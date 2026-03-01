# Class Breakdown: LockFreeQueue

**File**: `src\core\base\structures\LockFreeQueue.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `QueueStats`

**Line**: 30  
**Methods**: 2

Statistics for queue operations.

[TIP] **Suggested split**: Move to `queuestats.py`

---

### 2. `MPMCQueue`

**Line**: 55  
**Inherits**: Unknown  
**Methods**: 13

Multi-Producer Multi-Consumer bounded queue.

High-performance queue optimized for concurrent access.
Uses fine-grained locking with separate locks for head/tail.

Features:
- Bounded capacity to prev...

[TIP] **Suggested split**: Move to `mpmcqueue.py`

---

### 3. `SPSCQueue`

**Line**: 262  
**Inherits**: Unknown  
**Methods**: 7

Single-Producer Single-Consumer lock-free queue.

Optimized for scenarios with exactly one producer and one consumer thread.
Uses memory barriers instead of locks for maximum performance.

WARNING: On...

[TIP] **Suggested split**: Move to `spscqueue.py`

---

### 4. `PriorityItem`

**Line**: 353  
**Inherits**: Unknown  
**Methods**: 0

Item with priority for priority queue.

[TIP] **Suggested split**: Move to `priorityitem.py`

---

### 5. `PriorityQueue`

**Line**: 360  
**Inherits**: Unknown  
**Methods**: 8

Thread-safe priority queue.

Lower priority values are dequeued first (min-heap).
Maintains FIFO order for items with equal priority.

[TIP] **Suggested split**: Move to `priorityqueue.py`

---

### 6. `WorkStealingDeque`

**Line**: 477  
**Inherits**: Unknown  
**Methods**: 7

Work-stealing deque for task scheduling.

Owner pushes/pops from tail (LIFO for cache locality).
Thieves steal from head (FIFO to get older tasks).

[TIP] **Suggested split**: Move to `workstealingdeque.py`

---

### 7. `BatchingQueue`

**Line**: 559  
**Inherits**: Unknown  
**Methods**: 5

Queue that batches items for efficient processing.

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
