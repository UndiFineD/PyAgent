# Class Breakdown: LMFormatEnforcerBackend

**File**: `src\infrastructure\structured_output\LMFormatEnforcerBackend.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DFAStateType`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Types of DFA states.

[TIP] **Suggested split**: Move to `dfastatetype.py`

---

### 2. `DFAState`

**Line**: 62  
**Methods**: 1

Immutable DFA state.

Represents a state in the deterministic finite automaton
used for regex matching.

[TIP] **Suggested split**: Move to `dfastate.py`

---

### 3. `DFATransition`

**Line**: 78  
**Methods**: 1

DFA transition.

Maps a character/token to the next state.

[TIP] **Suggested split**: Move to `dfatransition.py`

---

### 4. `CompiledDFA`

**Line**: 99  
**Methods**: 6

Compiled DFA from regex pattern.

Provides efficient string matching via state transitions.

[TIP] **Suggested split**: Move to `compileddfa.py`

---

### 5. `TokenVocabulary`

**Line**: 164  
**Methods**: 5

Token vocabulary with efficient lookup.

Maps tokens to IDs and provides fast prefix matching.

[TIP] **Suggested split**: Move to `tokenvocabulary.py`

---

### 6. `RegexMatchState`

**Line**: 212  
**Methods**: 2

State for regex-based matching.

Tracks current match position and partial matches.

[TIP] **Suggested split**: Move to `regexmatchstate.py`

---

### 7. `CompiledEnforcer`

**Line**: 251  
**Methods**: 4

Compiled format enforcer.

Enforces that generated text matches a given pattern.

[TIP] **Suggested split**: Move to `compiledenforcer.py`

---

### 8. `LMFormatEnforcerBackend`

**Line**: 316  
**Methods**: 8

LM Format Enforcer backend for structured output.

Implements regex-based constrained generation using
DFA state tracking.

[TIP] **Suggested split**: Move to `lmformatenforcerbackend.py`

---

### 9. `AsyncLMFormatEnforcerBackend`

**Line**: 455  
**Inherits**: LMFormatEnforcerBackend  
**Methods**: 0

Async-enabled LM Format Enforcer backend.

Provides async pattern compilation for non-blocking operation.

[TIP] **Suggested split**: Move to `asynclmformatenforcerbackend.py`

---

### 10. `FormatEnforcerGrammar`

**Line**: 481  
**Methods**: 6

Grammar wrapper for Format Enforcer.

Provides the standard grammar interface.

[TIP] **Suggested split**: Move to `formatenforcergrammar.py`

---

### 11. `CompositeEnforcer`

**Line**: 520  
**Methods**: 3

Composite enforcer combining multiple patterns.

Matches if any sub-pattern matches (OR composition).

[TIP] **Suggested split**: Move to `compositeenforcer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
