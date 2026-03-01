# Class Breakdown: models

**File**: `src\infrastructure\backend\vllm_advanced\guided\models.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GuidedMode`

**Line**: 15  
**Inherits**: Enum  
**Methods**: 0

Mode of guided decoding.

[TIP] **Suggested split**: Move to `guidedmode.py`

---

### 2. `GuidedConfig`

**Line**: 26  
**Methods**: 1

Configuration for guided decoding.

[TIP] **Suggested split**: Move to `guidedconfig.py`

---

### 3. `RegexPattern`

**Line**: 70  
**Methods**: 8

Regex pattern builder for guided decoding.

[TIP] **Suggested split**: Move to `regexpattern.py`

---

### 4. `ChoiceConstraint`

**Line**: 136  
**Methods**: 6

Choice constraint for limiting output to specific options.

[TIP] **Suggested split**: Move to `choiceconstraint.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
