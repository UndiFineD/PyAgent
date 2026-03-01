# Class Breakdown: TritonAttentionOps

**File**: `src\infrastructure\attention\TritonAttentionOps.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AttentionBackend`

**Line**: 47  
**Inherits**: Enum  
**Methods**: 0

Available attention backends.

[TIP] **Suggested split**: Move to `attentionbackend.py`

---

### 2. `PrecisionMode`

**Line**: 56  
**Inherits**: Enum  
**Methods**: 0

Precision mode for attention computation.

[TIP] **Suggested split**: Move to `precisionmode.py`

---

### 3. `AttentionConfig`

**Line**: 65  
**Methods**: 1

Configuration for attention operations.

Inspired by vLLM's attention configuration patterns.

[TIP] **Suggested split**: Move to `attentionconfig.py`

---

### 4. `AttentionMetadata`

**Line**: 106  
**Methods**: 1

Metadata for attention computation.

Mirrors vLLM's AttentionMetadata structure.

[TIP] **Suggested split**: Move to `attentionmetadata.py`

---

### 5. `AttentionKernel`

**Line**: 139  
**Inherits**: ABC  
**Methods**: 2

Abstract base for attention kernels.

[TIP] **Suggested split**: Move to `attentionkernel.py`

---

### 6. `TritonPagedAttention`

**Line**: 267  
**Inherits**: AttentionKernel  
**Methods**: 3

Triton-based paged attention kernel.

Implements efficient paged attention using Triton JIT compilation.

[TIP] **Suggested split**: Move to `tritonpagedattention.py`

---

### 7. `NaiveAttention`

**Line**: 330  
**Inherits**: AttentionKernel  
**Methods**: 5

Reference implementation of attention (CPU/GPU compatible).

[TIP] **Suggested split**: Move to `naiveattention.py`

---

### 8. `SlidingWindowAttention`

**Line**: 387  
**Inherits**: AttentionKernel  
**Methods**: 3

Sliding window attention for efficient long-context handling.

[TIP] **Suggested split**: Move to `slidingwindowattention.py`

---

### 9. `KVSplitConfig`

**Line**: 436  
**Methods**: 0

Configuration for KV splits to handle long contexts.

Inspired by vLLM's KV split patterns for decode attention.

[TIP] **Suggested split**: Move to `kvsplitconfig.py`

---

### 10. `TritonAttentionOps`

**Line**: 447  
**Methods**: 6

Unified attention operations interface.

Provides automatic backend selection and fallback.

Beyond vLLM: Unified API for all attention backends.

[TIP] **Suggested split**: Move to `tritonattentionops.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
