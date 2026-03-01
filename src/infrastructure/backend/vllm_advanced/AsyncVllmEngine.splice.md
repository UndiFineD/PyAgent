# Class Breakdown: AsyncVllmEngine

**File**: `src\infrastructure\backend\vllm_advanced\AsyncVllmEngine.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestState`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

State of an async request.

[TIP] **Suggested split**: Move to `requeststate.py`

---

### 2. `AsyncEngineConfig`

**Line**: 66  
**Methods**: 1

Configuration for the async vLLM engine.

[TIP] **Suggested split**: Move to `asyncengineconfig.py`

---

### 3. `AsyncRequestHandle`

**Line**: 112  
**Methods**: 3

Handle for tracking an async request.

[TIP] **Suggested split**: Move to `asyncrequesthandle.py`

---

### 4. `AsyncVllmEngine`

**Line**: 154  
**Methods**: 7

High-throughput async vLLM engine for PyAgent.

Provides:
- Concurrent request handling
- Request tracking and cancellation
- Automatic batching via vLLM scheduler
- Streaming support via async iterat...

[TIP] **Suggested split**: Move to `asyncvllmengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
