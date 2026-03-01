# choice

**File**: `src\infrastructure\structured_output\choice.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 54  
**Complexity**: 3 (simple)

## Overview

Choice-based grammar engine.

## Classes (1)

### `ChoiceGrammar`

**Inherits from**: GrammarEngine

Grammar engine for fixed choice selection.

**Methods** (3):
- `__init__(self, vocab_size, token_strings, eos_token_id)`
- `build_fsm(self, spec)`
- `_build_trie_fsm(self, choices)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `base.GrammarEngine`
- `json`
- `models.FSMTransitionTable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
