# Class Breakdown: enums

**File**: `src\infrastructure\engine\reasoning\enums.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReasoningFormat`

**Line**: 22  
**Inherits**: Enum  
**Methods**: 0

Supported reasoning token formats.

[TIP] **Suggested split**: Move to `reasoningformat.py`

---

### 2. `ToolCallFormat`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Supported tool/function call formats.

[TIP] **Suggested split**: Move to `toolcallformat.py`

---

### 3. `ParseState`

**Line**: 47  
**Inherits**: Enum  
**Methods**: 0

State machine states for streaming parsing.

[TIP] **Suggested split**: Move to `parsestate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
