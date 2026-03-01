# Class Breakdown: Enums

**File**: `src\infrastructure\openai_api\responses\Enums.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ResponseStatus`

**Line**: 4  
**Inherits**: Enum  
**Methods**: 0

Response processing status.

[TIP] **Suggested split**: Move to `responsestatus.py`

---

### 2. `ResponseType`

**Line**: 13  
**Inherits**: Enum  
**Methods**: 0

Response object types.

[TIP] **Suggested split**: Move to `responsetype.py`

---

### 3. `ContentPartType`

**Line**: 19  
**Inherits**: Enum  
**Methods**: 0

Content part types.

[TIP] **Suggested split**: Move to `contentparttype.py`

---

### 4. `ToolType`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Tool types.

[TIP] **Suggested split**: Move to `tooltype.py`

---

### 5. `RoleType`

**Line**: 38  
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
