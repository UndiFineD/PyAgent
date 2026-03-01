# Sync

**File**: `src\infrastructure\orchestration\core\distributed\Sync.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 9 imports  
**Lines**: 107  
**Complexity**: 11 (moderate)

## Overview

High-performance synchronization primitives using RDMA/Nixl.

## Classes (3)

### `DistributedSyncProvider`

**Inherits from**: ABC

Base class for distributed synchronization providers.

**Methods** (3):
- `barrier(self, name, timeout)`
- `broadcast_state(self, key, value)`
- `get_remote_state(self, key, rank)`

### `NixlSyncProvider`

**Inherits from**: DistributedSyncProvider

Synchronization provider using NIXL RDMA primitives.

Utilizes zero-copy memory mapping for low-latency synchronization.

**Methods** (4):
- `__init__(self, rank, world_size)`
- `barrier(self, name, timeout)`
- `broadcast_state(self, key, value)`
- `get_remote_state(self, key, rank)`

### `TCPSyncProvider`

**Inherits from**: DistributedSyncProvider

Fallback TCP-based synchronization.

**Methods** (4):
- `__init__(self, rank, world_size)`
- `barrier(self, name, timeout)`
- `broadcast_state(self, key, value)`
- `get_remote_state(self, key, rank)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `src.core.rust_bridge.RustBridge`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
