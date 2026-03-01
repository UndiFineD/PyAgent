# Class Breakdown: types

**File**: `src\infrastructure\scheduling\chunked_prefill\types.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ChunkState`

**Line**: 13  
**Inherits**: Enum  
**Methods**: 0

State of a prefill chunk.

[TIP] **Suggested split**: Move to `chunkstate.py`

---

### 2. `ChunkPriority`

**Line**: 23  
**Inherits**: Enum  
**Methods**: 0

Priority for chunk scheduling.

[TIP] **Suggested split**: Move to `chunkpriority.py`

---

### 3. `ChunkMetrics`

**Line**: 32  
**Methods**: 3

Metrics for chunk processing.

[TIP] **Suggested split**: Move to `chunkmetrics.py`

---

### 4. `PrefillChunk`

**Line**: 62  
**Methods**: 4

A single chunk of prefill tokens.

Attributes:
    chunk_id: Unique identifier for this chunk
    request_id: Parent request identifier
    chunk_index: Index within the request (0-based)
    start_id...

[TIP] **Suggested split**: Move to `prefillchunk.py`

---

### 5. `ChunkedRequest`

**Line**: 112  
**Methods**: 5

A request split into multiple chunks.

Attributes:
    request_id: Unique request identifier
    total_tokens: Total prompt tokens
    chunks: List of chunks for this request

[TIP] **Suggested split**: Move to `chunkedrequest.py`

---

### 6. `ChunkedPrefillConfig`

**Line**: 164  
**Methods**: 0

Configuration for chunked prefill.

[TIP] **Suggested split**: Move to `chunkedprefillconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
