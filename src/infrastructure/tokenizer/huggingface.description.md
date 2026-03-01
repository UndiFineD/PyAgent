# huggingface

**File**: `src\infrastructure\tokenizer\huggingface.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 113  
**Complexity**: 11 (moderate)

## Overview

HuggingFace tokenizer implementation.

## Classes (1)

### `HuggingFaceTokenizer`

**Inherits from**: BaseTokenizer

HuggingFace transformers tokenizer wrapper.

**Methods** (11):
- `__init__(self, config)`
- `_load_tokenizer(self)`
- `vocab_size(self)`
- `bos_token_id(self)`
- `eos_token_id(self)`
- `pad_token_id(self)`
- `encode(self, text, add_special_tokens)`
- `decode(self, token_ids, skip_special_tokens)`
- `batch_encode(self, texts, add_special_tokens)`
- `apply_chat_template(self, messages, add_generation_prompt)`
- ... and 1 more methods

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `base.BaseTokenizer`
- `models.TokenizerBackend`
- `models.TokenizerConfig`
- `models.TokenizerInfo`
- `transformers.AutoTokenizer`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
