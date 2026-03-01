# base

**File**: `src\infrastructure\structured_output\manager\base.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 106  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for base.

## Classes (2)

### `StructuredOutputGrammar`

**Inherits from**: ABC

Abstract base class for grammar instances.

**Methods** (8):
- `__init__(self, grammar_spec, vocab_size, request_id)`
- `accept_tokens(self, tokens)`
- `validate_tokens(self, tokens)`
- `fill_bitmask(self, bitmask, batch_index)`
- `get_allowed_tokens(self)`
- `rollback(self, num_tokens)`
- `is_terminated(self)`
- `reset(self)`

### `StructuredOutputBackend`

**Inherits from**: ABC

Abstract backend for grammar compilation and management.

**Methods** (5):
- `__init__(self, vocab_size, tokenizer_encode, tokenizer_decode)`
- `compile_grammar(self, grammar_spec, request_id)`
- `get_supported_types(self)`
- `allocate_token_bitmask(self, max_batch_size)`
- `get_stats(self)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `config.BackendStats`
- `config.GrammarSpec`
- `config.GrammarType`
- `numpy`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
