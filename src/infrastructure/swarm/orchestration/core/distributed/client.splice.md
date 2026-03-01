# Class Breakdown: client

**File**: `src\infrastructure\swarm\orchestration\core\distributed\client.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MPClient`

**Line**: 41  
**Inherits**: Unknown  
**Methods**: 7

Client for communicating with worker processes.

Inspired by vLLM's MPClient pattern.
Synchronous interface for multi-process workers.

[TIP] **Suggested split**: Move to `mpclient.py`

---

### 2. `AsyncMPClient`

**Line**: 122  
**Inherits**: Unknown  
**Methods**: 1

Async client for communicating with worker processes.

Inspired by vLLM's AsyncMPClient.
Async interface for non-blocking operations.

[TIP] **Suggested split**: Move to `asyncmpclient.py`

---

### 3. `DPLBAsyncMPClient`

**Line**: 160  
**Inherits**: Unknown  
**Methods**: 3

Data-parallel load-balanced async client.

Inspired by vLLM's dp_lb_pool and DPAsyncMPClient.
Combines coordination with async multi-process execution.

[TIP] **Suggested split**: Move to `dplbasyncmpclient.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
