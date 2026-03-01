# Class Breakdown: SelfHealingCore

**File**: `src\infrastructure\orchestration\SelfHealingCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HealthStatus`

**Line**: 31  
**Methods**: 0

[TIP] **Suggested split**: Move to `healthstatus.py`

---

### 2. `SelfHealingCore`

**Line**: 39  
**Methods**: 5

Pure logic core for the SelfHealing orchestrator.

[TIP] **Suggested split**: Move to `selfhealingcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
