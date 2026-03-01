# Class Breakdown: enums

**File**: `src\infrastructure\structured_output\params\enums.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StructuredOutputType`

**Line**: 4  
**Inherits**: Enum  
**Methods**: 0

Type of structured output constraint.

[TIP] **Suggested split**: Move to `structuredoutputtype.py`

---

### 2. `ConstraintType`

**Line**: 13  
**Inherits**: Enum  
**Methods**: 0

Internal constraint type.

[TIP] **Suggested split**: Move to `constrainttype.py`

---

### 3. `SchemaFormat`

**Line**: 20  
**Inherits**: Enum  
**Methods**: 0

JSON Schema format.

[TIP] **Suggested split**: Move to `schemaformat.py`

---

### 4. `GuidedDecodingBackend`

**Line**: 27  
**Inherits**: Enum  
**Methods**: 0

Guided decoding backend.

[TIP] **Suggested split**: Move to `guideddecodingbackend.py`

---

### 5. `WhitespacePattern`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Whitespace handling in structured output.

[TIP] **Suggested split**: Move to `whitespacepattern.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
