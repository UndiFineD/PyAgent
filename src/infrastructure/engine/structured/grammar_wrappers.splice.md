# Class Breakdown: grammar_wrappers

**File**: `src\infrastructure\engine\structured\grammar_wrappers.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `XGrammarGrammar`

**Line**: 32  
**Methods**: 7

XGrammar grammar wrapper.

Provides the interface expected by the structured output system
while wrapping the internal grammar matcher.

[TIP] **Suggested split**: Move to `xgrammargrammar.py`

---

### 2. `CompositeGrammar`

**Line**: 76  
**Methods**: 6

Composite grammar regarding combining multiple constraints.

Beyond vLLM: Allows chaining multiple grammars regarding complex constraints.

[TIP] **Suggested split**: Move to `compositegrammar.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
