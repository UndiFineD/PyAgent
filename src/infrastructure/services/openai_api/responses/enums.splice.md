# Class Breakdown: enums

**File**: `src\infrastructure\services\openai_api\responses\enums.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ResponseStatus`

**Line**: 23  
**Inherits**: Enum  
**Methods**: 0

Response processing status.

[TIP] **Suggested split**: Move to `responsestatus.py`

---

### 2. `ResponseType`

**Line**: 34  
**Inherits**: Enum  
**Methods**: 0

Response object types.

[TIP] **Suggested split**: Move to `responsetype.py`

---

### 3. `ContentPartType`

**Line**: 42  
**Inherits**: Enum  
**Methods**: 0

Content part types.

[TIP] **Suggested split**: Move to `contentparttype.py`

---

### 4. `ToolType`

**Line**: 54  
**Inherits**: Enum  
**Methods**: 0

Tool types.

[TIP] **Suggested split**: Move to `tooltype.py`

---

### 5. `RoleType`

**Line**: 65  
**Inherits**: Enum  
**Methods**: 0

Message role types.

[TIP] **Suggested split**: Move to `roletype.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
