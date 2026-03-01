# Class Breakdown: async_microbatcher

**File**: `src\infrastructure\compute\backend\async_microbatcher.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BatchItem`

**Line**: 39  
**Inherits**: Unknown  
**Methods**: 0

A single item in a batch with its associated future.

[TIP] **Suggested split**: Move to `batchitem.py`

---

### 2. `BatchStats`

**Line**: 48  
**Methods**: 3

Statistics for batching performance.

[TIP] **Suggested split**: Move to `batchstats.py`

---

### 3. `AsyncMicrobatcher`

**Line**: 80  
**Inherits**: Unknown  
**Methods**: 6

Async micro-batcher that collects items and processes them in batches.

This is useful for batching LLM requests, tokenization, or any operation
that benefits from batch processing.

Example:
    >>> ...

[TIP] **Suggested split**: Move to `asyncmicrobatcher.py`

---

### 4. `SyncMicrobatcher`

**Line**: 276  
**Inherits**: Unknown  
**Methods**: 11

Synchronous micro-batcher using a background thread.

For use in synchronous code that needs batching.

[TIP] **Suggested split**: Move to `syncmicrobatcher.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
