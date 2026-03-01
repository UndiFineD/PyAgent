# regex

**File**: `src\infrastructure\structured_output\regex.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 179  
**Complexity**: 5 (moderate)

## Overview

Regex-based grammar engine.

## Classes (1)

### `RegexGrammar`

**Inherits from**: GrammarEngine

Regex-based grammar engine.

**Methods** (5):
- `__init__(self, vocab_size, token_strings, eos_token_id)`
- `build_fsm(self, spec)`
- `_build_nfa(self, parsed)`
- `_nfa_to_dfa(self, nfa_data)`
- `_build_simple_fsm(self, spec)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `base.GrammarEngine`
- `models.FSMTransitionTable`
- `re._parser`
- `sre_parse`
- `sys`
- `typing.Dict`
- `typing.FrozenSet`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `warnings`

---
*Auto-generated documentation*
