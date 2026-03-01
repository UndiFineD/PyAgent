# Class Breakdown: sop_core

**File**: `src\core\base\logic\core\sop_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SopStep`

**Line**: 19  
**Inherits**: BaseModel  
**Methods**: 0

[TIP] **Suggested split**: Move to `sopstep.py`

---

### 2. `SopManifest`

**Line**: 26  
**Inherits**: BaseModel  
**Methods**: 0

[TIP] **Suggested split**: Move to `sopmanifest.py`

---

### 3. `SopCore`

**Line**: 34  
**Methods**: 6

Manages 'Standard Operating Procedures' for autonomous workflows.
Pattern harvested from 'Acontext' and 'self_evolving_subagent'.

[TIP] **Suggested split**: Move to `sopcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
