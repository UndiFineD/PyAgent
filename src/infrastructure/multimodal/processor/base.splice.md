# Class Breakdown: base

**File**: `src\infrastructure\multimodal\processor\base.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ModalityType`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Supported modality types for multimodal inputs.

[TIP] **Suggested split**: Move to `modalitytype.py`

---

### 2. `MultiModalConfig`

**Line**: 40  
**Methods**: 2

Configuration for multimodal processing.

[TIP] **Suggested split**: Move to `multimodalconfig.py`

---

### 3. `PlaceholderInfo`

**Line**: 63  
**Methods**: 1

Information about a placeholder in the token sequence.

[TIP] **Suggested split**: Move to `placeholderinfo.py`

---

### 4. `MultiModalData`

**Line**: 76  
**Methods**: 2

Raw multimodal data before processing.

[TIP] **Suggested split**: Move to `multimodaldata.py`

---

### 5. `MultiModalInputs`

**Line**: 103  
**Methods**: 2

Processed multimodal inputs ready for model consumption.

[TIP] **Suggested split**: Move to `multimodalinputs.py`

---

### 6. `BaseMultiModalProcessor`

**Line**: 121  
**Inherits**: ABC, Unknown  
**Methods**: 4

Abstract base class for modality-specific processors.

[TIP] **Suggested split**: Move to `basemultimodalprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
