# Class Breakdown: x_grammar_backend

**File**: `src\infrastructure\engine\structured\x_grammar_backend.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `XGrammarBackend`

**Line**: 55  
**Methods**: 7

XGrammar-based structured output backend.

Provides constrained decoding using grammar-based token filtering.
Supports JSON schema, regex, EBNF, and structural tags.

Beyond vLLM innovations:
- Multi-...

[TIP] **Suggested split**: Move to `xgrammarbackend.py`

---

### 2. `AsyncXGrammarBackend`

**Line**: 185  
**Inherits**: XGrammarBackend  
**Methods**: 1

Async-enabled XGrammar backend.

Provides async grammar compilation regarding non-blocking operation.

[TIP] **Suggested split**: Move to `asyncxgrammarbackend.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
