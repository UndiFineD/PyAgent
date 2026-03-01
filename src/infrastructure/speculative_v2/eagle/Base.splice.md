# Class Breakdown: Base

**File**: `src\infrastructure\speculative_v2\eagle\Base.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `InputBuffer`

**Line**: 12  
**Inherits**: Protocol  
**Methods**: 3

Protocol for input buffer.

[TIP] **Suggested split**: Move to `inputbuffer.py`

---

### 2. `CpuGpuBuffer`

**Line**: 20  
**Methods**: 3

Buffer that syncs between CPU and GPU.

[TIP] **Suggested split**: Move to `cpugpubuffer.py`

---

### 3. `AttentionMetadata`

**Line**: 44  
**Methods**: 0

Metadata for attention computation.

[TIP] **Suggested split**: Move to `attentionmetadata.py`

---

### 4. `TreeAttentionMetadata`

**Line**: 56  
**Inherits**: AttentionMetadata  
**Methods**: 0

Metadata for tree attention.

[TIP] **Suggested split**: Move to `treeattentionmetadata.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
