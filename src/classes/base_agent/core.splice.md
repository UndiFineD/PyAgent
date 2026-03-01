# Class Breakdown: core

**File**: `src\classes\base_agent\core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CodeQualityReport`

**Line**: 20  
**Methods**: 0

[TIP] **Suggested split**: Move to `codequalityreport.py`

---

### 2. `BaseCore`

**Line**: 26  
**Methods**: 12

Pure logic core for all agents.

[TIP] **Suggested split**: Move to `basecore.py`

---

### 3. `LogicCore`

**Line**: 153  
**Methods**: 2

Base class for performance-critical logic.

[TIP] **Suggested split**: Move to `logiccore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
