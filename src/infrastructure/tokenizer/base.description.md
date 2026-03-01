# base

**File**: `src\infrastructure\tokenizer\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 110  
**Complexity**: 12 (moderate)

## Overview

Base class for tokenizers.

## Classes (1)

### `BaseTokenizer`

**Inherits from**: ABC

Abstract base class for tokenizers.

**Methods** (12):
- `__init__(self, config)`
- `vocab_size(self)`
- `bos_token_id(self)`
- `eos_token_id(self)`
- `pad_token_id(self)`
- `encode(self, text, add_special_tokens)`
- `decode(self, token_ids, skip_special_tokens)`
- `batch_encode(self, texts, add_special_tokens)`
- `batch_decode(self, token_ids_list, skip_special_tokens)`
- `tokenize(self, text, add_special_tokens, return_offsets)`
- ... and 2 more methods

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `models.TokenizeResult`
- `models.TokenizerConfig`
- `models.TokenizerInfo`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
