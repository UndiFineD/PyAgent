# Class Breakdown: models

**File**: `src\infrastructure\engine\attention\backend\models.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AttentionBackendEnum`

**Line**: 28  
**Inherits**: Enum  
**Methods**: 0

Enumeration of available attention backends.

[TIP] **Suggested split**: Move to `attentionbackendenum.py`

---

### 2. `AttentionType`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Types of attention computation.

[TIP] **Suggested split**: Move to `attentiontype.py`

---

### 3. `AttentionCapabilities`

**Line**: 51  
**Methods**: 0

Capabilities of an attention backend.

[TIP] **Suggested split**: Move to `attentioncapabilities.py`

---

### 4. `AttentionMetadata`

**Line**: 81  
**Methods**: 0

Metadata for attention computation.

[TIP] **Suggested split**: Move to `attentionmetadata.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
