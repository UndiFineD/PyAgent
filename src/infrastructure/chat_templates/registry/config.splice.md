# Class Breakdown: config

**File**: `src\infrastructure\chat_templates\registry\config.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TemplateType`

**Line**: 10  
**Inherits**: Enum  
**Methods**: 0

Chat template types.

[TIP] **Suggested split**: Move to `templatetype.py`

---

### 2. `ModelType`

**Line**: 30  
**Inherits**: Enum  
**Methods**: 0

Model types for template resolution.

[TIP] **Suggested split**: Move to `modeltype.py`

---

### 3. `TemplateConfig`

**Line**: 138  
**Methods**: 1

Chat template configuration.

[TIP] **Suggested split**: Move to `templateconfig.py`

---

### 4. `TemplateInfo`

**Line**: 161  
**Methods**: 1

Template metadata.

[TIP] **Suggested split**: Move to `templateinfo.py`

---

### 5. `RenderOptions`

**Line**: 183  
**Methods**: 1

Template rendering options.

[TIP] **Suggested split**: Move to `renderoptions.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
