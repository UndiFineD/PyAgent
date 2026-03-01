# Class Breakdown: communicator

**File**: `src\infrastructure\swarm\distributed\nccl\communicator.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `NCCLCommunicator`

**Line**: 44  
**Methods**: 18

Pure Python wrapper for NCCL collective operations.

Provides:
- Standard collective operations with error handling
- Automatic retry on transient failures
- Stream-based async operations
- CUDA graph...

[TIP] **Suggested split**: Move to `ncclcommunicator.py`

---

### 2. `CustomAllReduce`

**Line**: 427  
**Methods**: 4

Custom all-reduce implementation for specific scenarios.

[TIP] **Suggested split**: Move to `customallreduce.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
