# Class Breakdown: EBNFGrammar

**File**: `src\infrastructure\decoding\grammar\EBNFGrammar.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GrammarRule`

**Line**: 23  
**Methods**: 0

A single EBNF grammar rule.

[TIP] **Suggested split**: Move to `grammarrule.py`

---

### 2. `EBNFGrammar`

**Line**: 30  
**Inherits**: StructuredOutputGrammar  
**Methods**: 12

Grammar that constrains output using EBNF rules.

Supports simple context-free grammars for SQL, code, etc.
Inspired by vLLM's xgrammar EBNF support.

[TIP] **Suggested split**: Move to `ebnfgrammar.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
