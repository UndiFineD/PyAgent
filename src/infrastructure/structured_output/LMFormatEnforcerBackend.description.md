# LMFormatEnforcerBackend

**File**: `src\infrastructure\structured_output\LMFormatEnforcerBackend.py`  
**Type**: Python Module  
**Summary**: 11 classes, 0 functions, 25 imports  
**Lines**: 563  
**Complexity**: 36 (complex)

## Overview

LMFormatEnforcerBackend - LM Format Enforcer integration.

Implements structured output using regex-based token filtering:
- Regex automaton compilation
- DFA state transitions
- Multi-pattern support
- Efficient token masking

Beyond vLLM innovations:
- Compiled pattern caching
- Lazy DFA construction
- Incremental matching
- Pattern composition

## Classes (11)

### `DFAStateType`

**Inherits from**: Enum

Types of DFA states.

### `DFAState`

Immutable DFA state.

Represents a state in the deterministic finite automaton
used for regex matching.

**Methods** (1):
- `__hash__(self)`

### `DFATransition`

DFA transition.

Maps a character/token to the next state.

**Methods** (1):
- `matches(self, char)`

### `CompiledDFA`

Compiled DFA from regex pattern.

Provides efficient string matching via state transitions.

**Methods** (6):
- `__init__(self, pattern)`
- `_build_dfa(self)`
- `get_next_state(self, current_state, char)`
- `is_accepting(self, state_id)`
- `matches(self, text)`
- `partial_match(self, text)`

### `TokenVocabulary`

Token vocabulary with efficient lookup.

Maps tokens to IDs and provides fast prefix matching.

**Methods** (5):
- `__init__(self, tokenizer)`
- `_build_vocab(self)`
- `token_to_id(self, token)`
- `id_to_token(self, token_id)`
- `vocab_size(self)`

### `RegexMatchState`

State for regex-based matching.

Tracks current match position and partial matches.

**Methods** (2):
- `accept_token(self, token_text, dfa)`
- `reset(self)`

### `CompiledEnforcer`

Compiled format enforcer.

Enforces that generated text matches a given pattern.

**Methods** (4):
- `__init__(self, pattern, vocab)`
- `create_state(self)`
- `get_allowed_tokens(self, state)`
- `fill_bitmask(self, state, bitmask)`

### `LMFormatEnforcerBackend`

LM Format Enforcer backend for structured output.

Implements regex-based constrained generation using
DFA state tracking.

**Methods** (8):
- `__init__(self, tokenizer, vocab_size, max_cache_size)`
- `compile_regex(self, pattern)`
- `compile_json_schema(self, schema)`
- `_schema_to_regex(self, schema)`
- `_schema_obj_to_regex(self, schema)`
- `allocate_bitmask(self, batch_size)`
- `get_stats(self)`
- `clear_cache(self)`

### `AsyncLMFormatEnforcerBackend`

**Inherits from**: LMFormatEnforcerBackend

Async-enabled LM Format Enforcer backend.

Provides async pattern compilation for non-blocking operation.

### `FormatEnforcerGrammar`

Grammar wrapper for Format Enforcer.

Provides the standard grammar interface.

**Methods** (6):
- `__init__(self, enforcer, state)`
- `accept_token(self, token_id)`
- `accept_token_text(self, text)`
- `fill_next_token_bitmask(self, bitmask)`
- `is_terminated(self)`
- `reset(self)`

### `CompositeEnforcer`

Composite enforcer combining multiple patterns.

Matches if any sub-pattern matches (OR composition).

**Methods** (3):
- `__init__(self, enforcers)`
- `create_states(self)`
- `get_allowed_tokens(self, states)`

## Dependencies

**Imports** (25):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `json`
- `numpy`
- `re`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- ... and 10 more

---
*Auto-generated documentation*
