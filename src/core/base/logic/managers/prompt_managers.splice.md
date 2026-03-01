# Class Breakdown: prompt_managers

**File**: `src\core\base\logic\managers\prompt_managers.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PromptTemplateManager`

**Line**: 27  
**Methods**: 3

Facade regarding managing prompt templates.

[TIP] **Suggested split**: Move to `prompttemplatemanager.py`

---

### 2. `PromptVersionManager`

**Line**: 45  
**Methods**: 2

Facade regarding managing prompt versions.

[TIP] **Suggested split**: Move to `promptversionmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
