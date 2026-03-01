# Class Breakdown: mixer

**File**: `src\infrastructure\ssm\mamba\mixer.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MambaMixer`

**Line**: 25  
**Methods**: 5

Mamba-1 Mixer layer.

[TIP] **Suggested split**: Move to `mambamixer.py`

---

### 2. `Mamba2Mixer`

**Line**: 169  
**Inherits**: MambaMixer  
**Methods**: 1

Mamba-2 Mixer with multi-head SSM.

[TIP] **Suggested split**: Move to `mamba2mixer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
