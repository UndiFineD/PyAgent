# types

**File**: `src\infrastructure\tokenization\detokenizer\types.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 77  
**Complexity**: 7 (moderate)

## Overview

Types and protocols for incremental detokenization.

## Classes (2)

### `TokenizerLike`

**Inherits from**: Protocol

Protocol for tokenizer abstraction.

**Methods** (6):
- `encode(self, text)`
- `decode(self, token_ids, skip_special_tokens)`
- `convert_ids_to_tokens(self, ids)`
- `convert_tokens_to_ids(self, tokens)`
- `vocab(self)`
- `eos_token_id(self)`

### `DetokenizeResult`

Result of incremental detokenization.

**Methods** (1):
- `has_new_text(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.Union`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
