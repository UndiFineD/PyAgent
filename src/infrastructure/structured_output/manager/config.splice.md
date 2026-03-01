# Class Breakdown: config

**File**: `src\infrastructure\structured_output\manager\config.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GrammarType`

**Line**: 7  
**Inherits**: Enum  
**Methods**: 0

Types of grammar constraints supported.

[TIP] **Suggested split**: Move to `grammartype.py`

---

### 2. `CompilationStatus`

**Line**: 18  
**Inherits**: Enum  
**Methods**: 0

Status of grammar compilation.

[TIP] **Suggested split**: Move to `compilationstatus.py`

---

### 3. `GrammarSpec`

**Line**: 27  
**Methods**: 1

Specification for a grammar constraint.

[TIP] **Suggested split**: Move to `grammarspec.py`

---

### 4. `CompilationResult`

**Line**: 40  
**Methods**: 2

Result of grammar compilation.

[TIP] **Suggested split**: Move to `compilationresult.py`

---

### 5. `ValidationResult`

**Line**: 56  
**Methods**: 0

Result of token validation.

[TIP] **Suggested split**: Move to `validationresult.py`

---

### 6. `BackendStats`

**Line**: 64  
**Methods**: 0

Statistics for a structured output backend.

[TIP] **Suggested split**: Move to `backendstats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
