# mistral

**File**: `src\infrastructure\tokenizer\mistral.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 76  
**Complexity**: 8 (moderate)

## Overview

Mistral tokenizer implementation.

## Classes (1)

### `MistralTokenizer`

**Inherits from**: BaseTokenizer

Mistral tokenizer wrapper.

**Methods** (8):
- `__init__(self, config)`
- `_load_tokenizer(self)`
- `vocab_size(self)`
- `bos_token_id(self)`
- `eos_token_id(self)`
- `pad_token_id(self)`
- `encode(self, text, add_special_tokens)`
- `decode(self, token_ids, skip_special_tokens)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `base.BaseTokenizer`
- `mistral_common.tokens.tokenizers.mistral.MistralTokenizer`
- `models.TokenizerConfig`
- `transformers.AutoTokenizer`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
