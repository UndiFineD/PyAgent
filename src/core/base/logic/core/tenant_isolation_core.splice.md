# Class Breakdown: tenant_isolation_core

**File**: `src\core\base\logic\core\tenant_isolation_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TenantContext`

**Line**: 19  
**Inherits**: BaseModel  
**Methods**: 0

[TIP] **Suggested split**: Move to `tenantcontext.py`

---

### 2. `TenantIsolationCore`

**Line**: 26  
**Methods**: 5

Handles isolation of agent sessions between different tenants/users.
Patterns harvested from AgentCloud.

[TIP] **Suggested split**: Move to `tenantisolationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
