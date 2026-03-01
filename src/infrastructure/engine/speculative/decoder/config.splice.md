# Class Breakdown: config

**File**: `src\infrastructure\engine\speculative\decoder\config.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ProposerType`

**Line**: 22  
**Inherits**: Enum  
**Methods**: 0

Types of speculative proposers.

[TIP] **Suggested split**: Move to `proposertype.py`

---

### 2. `AcceptanceMethod`

**Line**: 32  
**Inherits**: Enum  
**Methods**: 0

Token acceptance verification methods.

[TIP] **Suggested split**: Move to `acceptancemethod.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
