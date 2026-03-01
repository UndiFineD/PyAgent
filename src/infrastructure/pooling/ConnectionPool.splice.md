# Class Breakdown: ConnectionPool

**File**: `src\infrastructure\pooling\ConnectionPool.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ConnectionState`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

State of a pooled connection.

[TIP] **Suggested split**: Move to `connectionstate.py`

---

### 2. `Closeable`

**Line**: 42  
**Inherits**: Protocol  
**Methods**: 1

Protocol for closeable resources.

[TIP] **Suggested split**: Move to `closeable.py`

---

### 3. `Pingable`

**Line**: 51  
**Inherits**: Protocol  
**Methods**: 1

Protocol for resources that can be health-checked.

[TIP] **Suggested split**: Move to `pingable.py`

---

### 4. `PoolStats`

**Line**: 60  
**Methods**: 4

Statistics for connection pool.

[TIP] **Suggested split**: Move to `poolstats.py`

---

### 5. `PooledConnection`

**Line**: 110  
**Inherits**: Unknown  
**Methods**: 2

Wrapper for a pooled connection.

[TIP] **Suggested split**: Move to `pooledconnection.py`

---

### 6. `ConnectionPool`

**Line**: 129  
**Inherits**: Unknown  
**Methods**: 16

Generic connection pool with health checking.

Features:
- Configurable min/max connections
- Health checking with ping
- Connection aging and rotation
- Wait timeout for busy pool
- Statistics tracki...

[TIP] **Suggested split**: Move to `connectionpool.py`

---

### 7. `AsyncConnectionPool`

**Line**: 464  
**Inherits**: Unknown  
**Methods**: 2

Async connection pool using asyncio.

[TIP] **Suggested split**: Move to `asyncconnectionpool.py`

---

### 8. `PooledConnectionManager`

**Line**: 532  
**Inherits**: Unknown  
**Methods**: 3

Context manager wrapper that auto-releases connection.

[TIP] **Suggested split**: Move to `pooledconnectionmanager.py`

---

### 9. `MultiHostPool`

**Line**: 551  
**Inherits**: Unknown  
**Methods**: 6

Connection pool across multiple hosts with load balancing.

[TIP] **Suggested split**: Move to `multihostpool.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
