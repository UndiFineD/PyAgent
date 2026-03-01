# Class Breakdown: Metadata

**File**: `src\infrastructure\speculative_v2\spec_decode\Metadata.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SpecDecodeMetadataV2`

**Line**: 19  
**Methods**: 8

Enhanced metadata for speculative decoding verification.

[TIP] **Suggested split**: Move to `specdecodemetadatav2.py`

---

### 2. `TreeVerificationMetadata`

**Line**: 102  
**Methods**: 3

Metadata for tree-based verification.

[TIP] **Suggested split**: Move to `treeverificationmetadata.py`

---

### 3. `SpecDecodeMetadataFactory`

**Line**: 144  
**Methods**: 2

Factory for creating speculative decode metadata.

[TIP] **Suggested split**: Move to `specdecodemetadatafactory.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
