# Class Breakdown: PoolingMetadata

**File**: `src\infrastructure\pooling\PoolingMetadata.py`  
**Classes**: 12

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PoolingStrategy`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Pooling strategies for sequence embeddings.

[TIP] **Suggested split**: Move to `poolingstrategy.py`

---

### 2. `PoolingCursor`

**Line**: 46  
**Methods**: 6

Cursor for tracking pooling positions (vLLM PoolingCursor equivalent).

Tracks the position within a sequence for pooling operations,
supporting both contiguous and chunked prefill scenarios.

[TIP] **Suggested split**: Move to `poolingcursor.py`

---

### 3. `PoolingStates`

**Line**: 99  
**Methods**: 3

State tracking for pooling operations (vLLM PoolingStates equivalent).

Tracks intermediate states for multi-pass pooling strategies.

[TIP] **Suggested split**: Move to `poolingstates.py`

---

### 4. `PoolingMetadata`

**Line**: 173  
**Methods**: 4

Metadata for pooling operations (vLLM PoolingMetadata equivalent).

Contains all information needed to perform pooling across a batch.

[TIP] **Suggested split**: Move to `poolingmetadata.py`

---

### 5. `Pooler`

**Line**: 256  
**Inherits**: ABC  
**Methods**: 1

Abstract base for pooling implementations.

[TIP] **Suggested split**: Move to `pooler.py`

---

### 6. `MeanPooler`

**Line**: 269  
**Inherits**: Pooler  
**Methods**: 1

Mean pooling implementation.

[TIP] **Suggested split**: Move to `meanpooler.py`

---

### 7. `MaxPooler`

**Line**: 287  
**Inherits**: Pooler  
**Methods**: 1

Max pooling implementation.

[TIP] **Suggested split**: Move to `maxpooler.py`

---

### 8. `LastTokenPooler`

**Line**: 305  
**Inherits**: Pooler  
**Methods**: 1

Last token pooling (for decoder-only models).

[TIP] **Suggested split**: Move to `lasttokenpooler.py`

---

### 9. `AttentionWeightedPooler`

**Line**: 321  
**Inherits**: Pooler  
**Methods**: 2

Attention-weighted pooling implementation.

[TIP] **Suggested split**: Move to `attentionweightedpooler.py`

---

### 10. `PoolerFactory`

**Line**: 355  
**Methods**: 1

Factory for creating poolers.

[TIP] **Suggested split**: Move to `poolerfactory.py`

---

### 11. `PoolerOutput`

**Line**: 374  
**Methods**: 3

Output from pooling operations (vLLM PoolerOutput equivalent).

Contains pooled embeddings and metadata.

[TIP] **Suggested split**: Move to `pooleroutput.py`

---

### 12. `ChunkedPoolingManager`

**Line**: 398  
**Methods**: 5

Manager for chunked prefill pooling.

Beyond vLLM: Supports async prefetch and memory-efficient processing.

[TIP] **Suggested split**: Move to `chunkedpoolingmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
