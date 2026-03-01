# Class Breakdown: constraints

**File**: `src\infrastructure\structured_output\params\constraints.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `OutputConstraint`

**Line**: 9  
**Methods**: 2

Base output constraint.

[TIP] **Suggested split**: Move to `outputconstraint.py`

---

### 2. `JsonSchemaConstraint`

**Line**: 25  
**Inherits**: OutputConstraint  
**Methods**: 4

JSON Schema constraint.

[TIP] **Suggested split**: Move to `jsonschemaconstraint.py`

---

### 3. `RegexConstraint`

**Line**: 154  
**Inherits**: OutputConstraint  
**Methods**: 3

Regex pattern constraint.

[TIP] **Suggested split**: Move to `regexconstraint.py`

---

### 4. `ChoiceConstraint`

**Line**: 181  
**Inherits**: OutputConstraint  
**Methods**: 2

Fixed choice constraint.

[TIP] **Suggested split**: Move to `choiceconstraint.py`

---

### 5. `GrammarConstraint`

**Line**: 199  
**Inherits**: OutputConstraint  
**Methods**: 1

Grammar constraint (EBNF/Lark).

[TIP] **Suggested split**: Move to `grammarconstraint.py`

---

### 6. `TypeConstraint`

**Line**: 214  
**Inherits**: OutputConstraint  
**Methods**: 2

Type annotation constraint.

[TIP] **Suggested split**: Move to `typeconstraint.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
