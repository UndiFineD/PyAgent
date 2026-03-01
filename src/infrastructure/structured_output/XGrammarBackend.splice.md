# Class Breakdown: XGrammarBackend

**File**: `src\infrastructure\structured_output\XGrammarBackend.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GrammarType`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

Types of grammar specifications.

[TIP] **Suggested split**: Move to `grammartype.py`

---

### 2. `VocabType`

**Line**: 63  
**Inherits**: Enum  
**Methods**: 0

Vocabulary encoding types.

[TIP] **Suggested split**: Move to `vocabtype.py`

---

### 3. `TokenizerInfo`

**Line**: 71  
**Methods**: 2

Tokenizer information for XGrammar.

Encapsulates vocabulary and tokenizer metadata needed for
grammar compilation and bitmask generation.

[TIP] **Suggested split**: Move to `tokenizerinfo.py`

---

### 4. `CompiledGrammar`

**Line**: 130  
**Methods**: 7

Compiled grammar context.

Holds the compiled grammar state and provides methods for
token acceptance checking and bitmask generation.

[TIP] **Suggested split**: Move to `compiledgrammar.py`

---

### 5. `GrammarMatcher`

**Line**: 183  
**Methods**: 4

Grammar matcher with rollback support.

Wraps CompiledGrammar with additional state management
for speculative decoding scenarios.

[TIP] **Suggested split**: Move to `grammarmatcher.py`

---

### 6. `GrammarCompiler`

**Line**: 226  
**Methods**: 9

Grammar compiler with caching.

Compiles grammar specifications into executable matchers
with thread-safe caching and configurable limits.

[TIP] **Suggested split**: Move to `grammarcompiler.py`

---

### 7. `XGrammarGrammar`

**Line**: 402  
**Methods**: 7

XGrammar grammar wrapper.

Provides the interface expected by the structured output system
while wrapping the internal grammar matcher.

[TIP] **Suggested split**: Move to `xgrammargrammar.py`

---

### 8. `XGrammarBackend`

**Line**: 446  
**Methods**: 7

XGrammar-based structured output backend.

Provides constrained decoding using grammar-based token filtering.
Supports JSON schema, regex, EBNF, and structural tags.

Beyond vLLM innovations:
- Multi-...

[TIP] **Suggested split**: Move to `xgrammarbackend.py`

---

### 9. `AsyncXGrammarBackend`

**Line**: 576  
**Inherits**: XGrammarBackend  
**Methods**: 1

Async-enabled XGrammar backend.

Provides async grammar compilation for non-blocking operation.

[TIP] **Suggested split**: Move to `asyncxgrammarbackend.py`

---

### 10. `CompositeGrammar`

**Line**: 604  
**Methods**: 6

Composite grammar for combining multiple constraints.

Beyond vLLM: Allows chaining multiple grammars for complex constraints.

[TIP] **Suggested split**: Move to `compositegrammar.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
