# Class Breakdown: template_manager

**File**: `src\core\base\common\utils\template_manager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Template`

**Line**: 27  
**Methods**: 2

Legacy template object wrapper.

[TIP] **Suggested split**: Move to `template.py`

---

### 2. `TemplateManager`

**Line**: 39  
**Methods**: 4

Manages agent templates and prompt construction.

[TIP] **Suggested split**: Move to `templatemanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
