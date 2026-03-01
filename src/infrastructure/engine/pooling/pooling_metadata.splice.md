# Class Breakdown: pooling_metadata

**File**: `src\infrastructure\engine\pooling\pooling_metadata.py`  
**Classes**: 12

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PoolingStrategy`

**Line**: 49  
**Inherits**: Enum  
**Methods**: 0

Pooling strategies for sequence embeddings.

[TIP] **Suggested split**: Move to `poolingstrategy.py`

---

### 2. `PoolingCursor`

**Line**: 61  
**Methods**: 6

Cursor for tracking pooling positions (vLLM PoolingCursor equivalent).

Tracks the position within a sequence for pooling operations,
supporting both contiguous and chunked prefill scenarios.

[TIP] **Suggested split**: Move to `poolingcursor.py`

---

### 3. `PoolingStates`

**Line**: 115  
**Methods**: 3

State tracking for pooling operations (vLLM PoolingStates equivalent).

Tracks intermediate states for multi-pass pooling strategies.

[TIP] **Suggested split**: Move to `poolingstates.py`

---

### 4. `PoolingMetadata`

**Line**: 189  
**Methods**: 4

Metadata for pooling operations (vLLM PoolingMetadata equivalent).

Contains all information needed to perform pooling across a batch.

[TIP] **Suggested split**: Move to `poolingmetadata.py`

---

### 5. `Pooler`

**Line**: 281  
**Inherits**: ABC  
**Methods**: 1

Abstract base for pooling implementations.

[TIP] **Suggested split**: Move to `pooler.py`

---

### 6. `MeanPooler`

**Line**: 294  
**Inherits**: Pooler  
**Methods**: 1

Mean pooling implementation.

[TIP] **Suggested split**: Move to `meanpooler.py`

---

### 7. `MaxPooler`

**Line**: 312  
**Inherits**: Pooler  
**Methods**: 1

Max pooling implementation.

[TIP] **Suggested split**: Move to `maxpooler.py`

---

### 8. `LastTokenPooler`

**Line**: 330  
**Inherits**: Pooler  
**Methods**: 1

Last token pooling regarding decoder-only models.

[TIP] **Suggested split**: Move to `lasttokenpooler.py`

---

### 9. `AttentionWeightedPooler`

**Line**: 347  
**Inherits**: Pooler  
**Methods**: 2

Attention-weighted pooling implementation.

[TIP] **Suggested split**: Move to `attentionweightedpooler.py`

---

### 10. `PoolerFactory`

**Line**: 379  
**Methods**: 1

Factory for creating poolers.

[TIP] **Suggested split**: Move to `poolerfactory.py`

---

### 11. `PoolerOutput`

**Line**: 397  
**Methods**: 3

Output from pooling operations (vLLM PoolerOutput equivalent).

Contains pooled embeddings and metadata.

[TIP] **Suggested split**: Move to `pooleroutput.py`

---

### 12. `ChunkedPoolingManager`

**Line**: 423  
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
