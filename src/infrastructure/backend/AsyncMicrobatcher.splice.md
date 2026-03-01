# Class Breakdown: AsyncMicrobatcher

**File**: `src\infrastructure\backend\AsyncMicrobatcher.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BatchItem`

**Line**: 24  
**Inherits**: Unknown  
**Methods**: 0

A single item in a batch with its associated future.

[TIP] **Suggested split**: Move to `batchitem.py`

---

### 2. `BatchStats`

**Line**: 32  
**Methods**: 3

Statistics for batching performance.

[TIP] **Suggested split**: Move to `batchstats.py`

---

### 3. `AsyncMicrobatcher`

**Line**: 63  
**Inherits**: Unknown  
**Methods**: 3

Async micro-batcher that collects items and processes them in batches.

This is useful for batching LLM requests, tokenization, or any operation
that benefits from batch processing.

Example:
    >>> ...

[TIP] **Suggested split**: Move to `asyncmicrobatcher.py`

---

### 4. `SyncMicrobatcher`

**Line**: 255  
**Inherits**: Unknown  
**Methods**: 8

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
