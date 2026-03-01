# Class Breakdown: config

**File**: `src\infrastructure\compute\ssm\mamba\config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MambaConfig`

**Line**: 30  
**Methods**: 3

Configuration for Mamba mixer.

[TIP] **Suggested split**: Move to `mambaconfig.py`

---

### 2. `MambaState`

**Line**: 73  
**Methods**: 2

State for Mamba recurrence.

[TIP] **Suggested split**: Move to `mambastate.py`

---

### 3. `MambaOutput`

**Line**: 108  
**Inherits**: NamedTuple  
**Methods**: 0

Output from Mamba forward pass.

[TIP] **Suggested split**: Move to `mambaoutput.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
