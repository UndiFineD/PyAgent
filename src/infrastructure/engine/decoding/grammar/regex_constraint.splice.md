# Class Breakdown: regex_constraint

**File**: `src\infrastructure\engine\decoding\grammar\regex_constraint.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RegexGrammar`

**Line**: 38  
**Inherits**: StructuredOutputGrammar  
**Methods**: 10

Grammar that constrains output to match a regex pattern.

Uses DFA-based matching for efficient token validation.
Inspired by vLLM's outlines backend.

Phase 39: Rust-accelerated bitmasking for full-v...

[TIP] **Suggested split**: Move to `regexgrammar.py`

---

### 2. `ChoiceGrammar`

**Line**: 232  
**Inherits**: StructuredOutputGrammar  
**Methods**: 9

Grammar that constrains output to one of several choices.

Efficient matching by tracking which choices remain possible.

[TIP] **Suggested split**: Move to `choicegrammar.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
