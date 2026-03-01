# ebnf

**File**: `src\infrastructure\structured_output\ebnf.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 71  
**Complexity**: 5 (moderate)

## Overview

EBNF grammar engine.

## Classes (1)

### `EBNFGrammar`

**Inherits from**: GrammarEngine

EBNF/Lark grammar engine.

**Methods** (5):
- `__init__(self, vocab_size, token_strings, eos_token_id)`
- `build_fsm(self, spec)`
- `_parse_ebnf(self, spec)`
- `_rule_to_fsm(self, rule, all_rules)`
- `_build_literal_fsm(self, spec)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `base.GrammarEngine`
- `models.FSMTransitionTable`
- `re`
- `regex.RegexGrammar`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
