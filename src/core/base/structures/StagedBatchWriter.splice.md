# Class Breakdown: StagedBatchWriter

**File**: `src\core\base\structures\StagedBatchWriter.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `WritePolicy`

**Line**: 56  
**Inherits**: Enum  
**Methods**: 0

Policy for handling conflicting writes.

[TIP] **Suggested split**: Move to `writepolicy.py`

---

### 2. `CoalesceStrategy`

**Line**: 65  
**Inherits**: Enum  
**Methods**: 0

Strategy for coalescing writes.

[TIP] **Suggested split**: Move to `coalescestrategy.py`

---

### 3. `StagedWrite`

**Line**: 73  
**Methods**: 0

A single staged write operation.

[TIP] **Suggested split**: Move to `stagedwrite.py`

---

### 4. `WriteStats`

**Line**: 82  
**Methods**: 2

Statistics for write operations.

[TIP] **Suggested split**: Move to `writestats.py`

---

### 5. `StagedBatchWriter`

**Line**: 106  
**Methods**: 11

Collect writes and apply them in batch to GPU memory.

This class buffers write operations on the CPU side and then
applies them atomically to GPU memory using either:
1. Triton kernel for maximum per...

[TIP] **Suggested split**: Move to `stagedbatchwriter.py`

---

### 6. `StagedWriteTensor`

**Line**: 459  
**Methods**: 10

A tensor with built-in staged write support.

This is a higher-level wrapper that combines a tensor with
a StagedBatchWriter for convenient write-batching.

[TIP] **Suggested split**: Move to `stagedwritetensor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
