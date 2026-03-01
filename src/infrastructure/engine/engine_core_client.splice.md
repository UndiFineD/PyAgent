# Class Breakdown: engine_core_client

**File**: `src\infrastructure\engine\engine_core_client.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestType`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

Types of requests to engine core.

[TIP] **Suggested split**: Move to `requesttype.py`

---

### 2. `ClientConfig`

**Line**: 54  
**Methods**: 0

Configuration for engine core clients.

[TIP] **Suggested split**: Move to `clientconfig.py`

---

### 3. `EngineCoreClient`

**Line**: 64  
**Inherits**: ABC  
**Methods**: 10

Abstract base class for engine core clients.

Provides interface for adding requests, getting outputs,
and managing engine lifecycle.

[TIP] **Suggested split**: Move to `enginecoreclient.py`

---

### 4. `InprocClient`

**Line**: 133  
**Inherits**: EngineCoreClient  
**Methods**: 6

In-process client for EngineCore.

Runs the engine in the same process, suitable for single-threaded
or testing scenarios.

[TIP] **Suggested split**: Move to `inprocclient.py`

---

### 5. `SyncMPClient`

**Line**: 204  
**Inherits**: EngineCoreClient  
**Methods**: 13

Synchronous multiprocess client for EngineCore.

Runs the engine in a background thread with queue-based communication.

[TIP] **Suggested split**: Move to `syncmpclient.py`

---

### 6. `AsyncMPClient`

**Line**: 318  
**Inherits**: EngineCoreClient  
**Methods**: 6

Asynchronous multiprocess client for EngineCore.

Provides async interface with background engine execution.

[TIP] **Suggested split**: Move to `asyncmpclient.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
