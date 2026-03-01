# models

**File**: `src\infrastructure\structured_output\models.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 10 imports  
**Lines**: 127  
**Complexity**: 15 (moderate)

## Overview

Models for Grammar Engine and FSM state management.

## Classes (3)

### `FSMState`

Immutable representation of FSM state.

**Methods** (2):
- `get_transition(self, char)`
- `get_all_transitions(self)`

### `FSMTransitionTable`

Transition table for efficient FSM execution.

**Methods** (5):
- `__post_init__(self)`
- `add_transition(self, from_state, char, to_state)`
- `get_next_state(self, current_state, char)`
- `is_accepting(self, state)`
- `get_allowed_chars(self, state)`

### `TokenMask`

Token-level constraint mask.

**Methods** (8):
- `__post_init__(self)`
- `allow_only(self, token_ids)`
- `disallow(self, token_ids)`
- `apply_to_logits(self, logits)`
- `get_allowed_count(self)`
- `get_allowed_tokens(self)`
- `combine_and(self, other)`
- `combine_or(self, other)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `typing.Dict`
- `typing.FrozenSet`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
