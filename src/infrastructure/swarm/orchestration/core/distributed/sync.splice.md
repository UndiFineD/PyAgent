# Class Breakdown: sync

**File**: `src\infrastructure\swarm\orchestration\core\distributed\sync.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DistributedSyncProvider`

**Line**: 33  
**Inherits**: ABC  
**Methods**: 3

Base class for distributed synchronization providers.

[TIP] **Suggested split**: Move to `distributedsyncprovider.py`

---

### 2. `NixlSyncProvider`

**Line**: 52  
**Inherits**: DistributedSyncProvider  
**Methods**: 4

Synchronization provider using NIXL RDMA primitives.

Utilizes zero-copy memory mapping for low-latency synchronization.

[TIP] **Suggested split**: Move to `nixlsyncprovider.py`

---

### 3. `TCPSyncProvider`

**Line**: 104  
**Inherits**: DistributedSyncProvider  
**Methods**: 4

Fallback TCP-based synchronization.

[TIP] **Suggested split**: Move to `tcpsyncprovider.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
