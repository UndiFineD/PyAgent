# Class Breakdown: privilege_escalation_core

**File**: `src\core\base\logic\security\privilege_escalation_core.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LUID`

**Line**: 44  
**Inherits**: Structure  
**Methods**: 0

[TIP] **Suggested split**: Move to `luid.py`

---

### 2. `LUID_AND_ATTRIBUTES`

**Line**: 48  
**Inherits**: Structure  
**Methods**: 0

[TIP] **Suggested split**: Move to `luid_and_attributes.py`

---

### 3. `TOKEN_PRIVILEGES`

**Line**: 52  
**Inherits**: Structure  
**Methods**: 0

[TIP] **Suggested split**: Move to `token_privileges.py`

---

### 4. `PROCESSENTRY32`

**Line**: 59  
**Inherits**: Structure  
**Methods**: 0

[TIP] **Suggested split**: Move to `processentry32.py`

---

### 5. `PrivilegeEscalationCore`

**Line**: 74  
**Methods**: 5

Core class for Windows privilege escalation operations.

[TIP] **Suggested split**: Move to `privilegeescalationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
