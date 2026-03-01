# Class Breakdown: sandbox_core

**File**: `src\infrastructure\services\sandbox\core\sandbox_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SandboxConfig`

**Line**: 26  
**Methods**: 0

Immutable configuration for agent sandboxing.

[TIP] **Suggested split**: Move to `sandboxconfig.py`

---

### 2. `SandboxCore`

**Line**: 37  
**Methods**: 3

Pure logic for containerized agent runtimes and resource isolation.
Handles enforcement logic, quota calculations, and security constraints.

[TIP] **Suggested split**: Move to `sandboxcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
