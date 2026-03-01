# Class Breakdown: resource_core

**File**: `src\core\base\common\resource_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `QuotaConfig`

**Line**: 29  
**Methods**: 0

Configuration for agent resource quotas.

[TIP] **Suggested split**: Move to `quotaconfig.py`

---

### 2. `ResourceUsage`

**Line**: 38  
**Methods**: 2

Current resource usage for an agent session.

[TIP] **Suggested split**: Move to `resourceusage.py`

---

### 3. `ResourceCore`

**Line**: 57  
**Inherits**: BaseCore  
**Methods**: 6

Authoritative engine for resource quota enforcement.

[TIP] **Suggested split**: Move to `resourcecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
