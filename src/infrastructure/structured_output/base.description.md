# base

**File**: `src\infrastructure\structured_output\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 82  
**Complexity**: 4 (simple)

## Overview

Base class for grammar engines.

## Classes (1)

### `GrammarEngine`

**Inherits from**: ABC

Abstract base class for grammar engines.

**Methods** (4):
- `__init__(self, vocab_size, token_strings, eos_token_id)`
- `build_fsm(self, spec)`
- `get_tokens_for_chars(self, chars)`
- `get_token_mask(self, fsm, state)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `models.FSMTransitionTable`
- `models.TokenMask`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
