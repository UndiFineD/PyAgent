# Class Breakdown: streaming_engine

**File**: `src\infrastructure\compute\backend\vllm_advanced\streaming_engine.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StreamCallback`

**Line**: 54  
**Inherits**: Protocol  
**Methods**: 1

Protocol for stream callbacks.

[TIP] **Suggested split**: Move to `streamcallback.py`

---

### 2. `StreamingConfig`

**Line**: 68  
**Methods**: 0

Configuration for streaming engine.

[TIP] **Suggested split**: Move to `streamingconfig.py`

---

### 3. `StreamToken`

**Line**: 87  
**Methods**: 0

A streamed token.

[TIP] **Suggested split**: Move to `streamtoken.py`

---

### 4. `TokenStreamIterator`

**Line**: 98  
**Methods**: 4

Iterator for streaming tokens.

Can be used in both sync and async contexts.

Example (sync):
    for token in stream_iterator:
        print(token.text, end="", flush=True)

Example (async):
    asyn...

[TIP] **Suggested split**: Move to `tokenstreamiterator.py`

---

### 5. `StreamingVllmEngine`

**Line**: 207  
**Methods**: 11

Streaming vLLM engine for real-time token output.

Provides multiple streaming modes:
1. Callback-based: Register a callback for each token
2. Iterator-based: Use async for loop
3. Buffer-based: Colle...

[TIP] **Suggested split**: Move to `streamingvllmengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
