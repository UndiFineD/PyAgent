# tiktoken

**File**: `src\infrastructure\tokenizer\tiktoken.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 93  
**Complexity**: 10 (moderate)

## Overview

Tiktoken tokenizer implementation.

## Classes (1)

### `TiktokenTokenizer`

**Inherits from**: BaseTokenizer

OpenAI tiktoken tokenizer wrapper.

**Methods** (10):
- `__init__(self, config)`
- `_load_tokenizer(self)`
- `vocab_size(self)`
- `bos_token_id(self)`
- `eos_token_id(self)`
- `pad_token_id(self)`
- `encode(self, text, add_special_tokens)`
- `decode(self, token_ids, skip_special_tokens)`
- `encode_batch(self, texts, add_special_tokens)`
- `estimate_tokens(self, text)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `base.BaseTokenizer`
- `models.TokenizerConfig`
- `tiktoken`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
