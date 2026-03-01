# impl

**File**: `src\infrastructure\structured_output\manager\impl.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 159  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for impl.

## Classes (2)

### `SimpleRegexGrammar`

**Inherits from**: StructuredOutputGrammar

Simple regex-based grammar using Python's re module.

**Methods** (6):
- `__init__(self, grammar_spec, vocab_size, request_id, token_strings)`
- `accept_tokens(self, tokens)`
- `_is_partial_match(self, text)`
- `validate_tokens(self, tokens)`
- `fill_bitmask(self, bitmask, batch_index)`
- `get_allowed_tokens(self)`

### `ChoiceGrammar`

**Inherits from**: StructuredOutputGrammar

Grammar for choosing from a fixed set of options.

**Methods** (7):
- `__init__(self, grammar_spec, vocab_size, request_id, token_strings, encode_fn)`
- `accept_tokens(self, tokens)`
- `validate_tokens(self, tokens)`
- `fill_bitmask(self, bitmask, batch_index)`
- `get_allowed_tokens(self)`
- `_compute_allowed_tokens(self)`
- `rollback(self, num_tokens)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `base.StructuredOutputGrammar`
- `config.GrammarSpec`
- `json`
- `numpy`
- `re`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
