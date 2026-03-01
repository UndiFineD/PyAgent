# Class Breakdown: enums

**File**: `src\infrastructure\engine\structured\enums.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GrammarType`

**Line**: 22  
**Inherits**: Enum  
**Methods**: 0

Types of grammar specifications.

[TIP] **Suggested split**: Move to `grammartype.py`

---

### 2. `VocabType`

**Line**: 34  
**Inherits**: Enum  
**Methods**: 0

Vocabulary encoding types.

[TIP] **Suggested split**: Move to `vocabtype.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
