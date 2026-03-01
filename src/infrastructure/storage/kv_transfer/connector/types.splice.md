# Class Breakdown: types

**File**: `src\infrastructure\storage\kv_transfer\connector\types.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `KVConnectorRole`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Role of the KV connector in disaggregated inference.

[TIP] **Suggested split**: Move to `kvconnectorrole.py`

---

### 2. `KVTransferMode`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

Transfer mode for KV cache data.

[TIP] **Suggested split**: Move to `kvtransfermode.py`

---

### 3. `KVTransferConfig`

**Line**: 49  
**Methods**: 3

Configuration for KV transfer operations.

[TIP] **Suggested split**: Move to `kvtransferconfig.py`

---

### 4. `KVConnectorMetadata`

**Line**: 81  
**Methods**: 0

Metadata for KV transfer operations.

[TIP] **Suggested split**: Move to `kvconnectormetadata.py`

---

### 5. `KVCacheBlocks`

**Line**: 91  
**Methods**: 3

Represents allocated KV cache blocks for a request.

[TIP] **Suggested split**: Move to `kvcacheblocks.py`

---

### 6. `ForwardContext`

**Line**: 111  
**Inherits**: Protocol  
**Methods**: 1

Protocol for forward context during model execution.

[TIP] **Suggested split**: Move to `forwardcontext.py`

---

### 7. `Request`

**Line**: 119  
**Inherits**: Protocol  
**Methods**: 2

Protocol for request objects.

[TIP] **Suggested split**: Move to `request.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
