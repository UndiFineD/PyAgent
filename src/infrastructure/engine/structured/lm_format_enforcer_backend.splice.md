# Class Breakdown: lm_format_enforcer_backend

**File**: `src\infrastructure\engine\structured\lm_format_enforcer_backend.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DFAStateType`

**Line**: 58  
**Inherits**: Enum  
**Methods**: 0

Types of DFA states.

[TIP] **Suggested split**: Move to `dfastatetype.py`

---

### 2. `DFAState`

**Line**: 68  
**Methods**: 1

Immutable DFA state.

Represents a state in the deterministic finite automaton
used regarding regex matching.

[TIP] **Suggested split**: Move to `dfastate.py`

---

### 3. `DFATransition`

**Line**: 85  
**Methods**: 1

DFA transition.

Maps a character/token to the next state.

[TIP] **Suggested split**: Move to `dfatransition.py`

---

### 4. `CompiledDFA`

**Line**: 107  
**Methods**: 6

Compiled DFA from regex pattern.

Provides efficient string matching via state transitions.

[TIP] **Suggested split**: Move to `compileddfa.py`

---

### 5. `TokenVocabulary`

**Line**: 170  
**Methods**: 5

Token vocabulary with efficient lookup.

Maps tokens to IDs and provides fast prefix matching.

[TIP] **Suggested split**: Move to `tokenvocabulary.py`

---

### 6. `RegexMatchState`

**Line**: 220  
**Methods**: 2

State regarding regex-based matching.

Tracks current match position and partial matches.

[TIP] **Suggested split**: Move to `regexmatchstate.py`

---

### 7. `CompiledEnforcer`

**Line**: 260  
**Methods**: 5

Compiled format enforcer.

Enforces that generated text matches a given pattern.

[TIP] **Suggested split**: Move to `compiledenforcer.py`

---

### 8. `LMFormatEnforcerBackend`

**Line**: 327  
**Methods**: 8

LM Format Enforcer backend regarding structured output.

Implements regex-based constrained generation using
DFA state tracking.

[TIP] **Suggested split**: Move to `lmformatenforcerbackend.py`

---

### 9. `AsyncLMFormatEnforcerBackend`

**Line**: 463  
**Inherits**: LMFormatEnforcerBackend  
**Methods**: 0

Async-enabled LM Format Enforcer backend.

Provides async pattern compilation regarding non-blocking operation.

[TIP] **Suggested split**: Move to `asynclmformatenforcerbackend.py`

---

### 10. `FormatEnforcerGrammar`

**Line**: 489  
**Methods**: 6

Grammar wrapper regarding Format Enforcer.

Provides the standard grammar interface.

[TIP] **Suggested split**: Move to `formatenforcergrammar.py`

---

### 11. `CompositeEnforcer`

**Line**: 528  
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
