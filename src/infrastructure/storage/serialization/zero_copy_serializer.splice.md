# Class Breakdown: zero_copy_serializer

**File**: `src\infrastructure\storage\serialization\zero_copy_serializer.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ZeroCopyEncoder`

**Line**: 70  
**Methods**: 6

Encoder with zero-copy tensor and numpy array serialization.

Large tensors are stored as references to auxiliary buffers rather than
being copied into the main msgpack buffer. This enables efficient ...

[TIP] **Suggested split**: Move to `zerocopyencoder.py`

---

### 2. `ZeroCopyDecoder`

**Line**: 208  
**Methods**: 6

Decoder with zero-copy tensor and numpy array deserialization.

Reconstructs tensors and arrays from auxiliary buffers without copying.

Example:
    >>> decoder = ZeroCopyDecoder()
    >>> obj = deco...

[TIP] **Suggested split**: Move to `zerocopydecoder.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
