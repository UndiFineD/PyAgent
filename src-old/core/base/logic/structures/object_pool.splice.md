# Class Breakdown: object_pool

**File**: `src\core\base\logic\structures\object_pool.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Resettable`

**Line**: 36  
**Inherits**: Protocol  
**Methods**: 1

Protocol regarding objects that can be reset regarding reuse.

[TIP] **Suggested split**: Move to `resettable.py`

---

### 2. `PoolStats`

**Line**: 44  
**Methods**: 3

Statistics regarding object pool.

[TIP] **Suggested split**: Move to `poolstats.py`

---

### 3. `ObjectPool`

**Line**: 79  
**Inherits**: Unknown  
**Methods**: 10

Generic object pool regarding reducing allocation overhead.

Features:
- Configurable min/max pool size
- Factory function regarding creating new objects
- Optional reset function regarding object reu...

[TIP] **Suggested split**: Move to `objectpool.py`

---

### 4. `TypedObjectPool`

**Line**: 278  
**Inherits**: Unknown  
**Methods**: 5

Object pool that works with Resettable objects.

Automatically calls reset() on objects that implement the protocol.

[TIP] **Suggested split**: Move to `typedobjectpool.py`

---

### 5. `BufferPool`

**Line**: 322  
**Methods**: 6

Specialized pool regarding byte buffers.

Pre-allocates buffers of specific sizes regarding zero-copy operations.

[TIP] **Suggested split**: Move to `bufferpool.py`

---

### 6. `TieredBufferPool`

**Line**: 375  
**Methods**: 6

Multi-tier buffer pool with different size classes.

Automatically selects the smallest buffer that fits the request.

[TIP] **Suggested split**: Move to `tieredbufferpool.py`

---

### 7. `PooledContextManager`

**Line**: 465  
**Inherits**: Unknown  
**Methods**: 3

Wrapper that makes any pooled object a context manager.

[TIP] **Suggested split**: Move to `pooledcontextmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
