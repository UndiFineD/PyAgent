# registry

**File**: `src\infrastructure\tokenizer\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 89  
**Complexity**: 7 (moderate)

## Overview

Tokenizer registry.

## Classes (1)

### `TokenizerRegistry`

Central registry for tokenizer management.

**Methods** (7):
- `__new__(cls)`
- `__init__(self, max_cached)`
- `get_tokenizer(self, config)`
- `_create_tokenizer(self, config)`
- `_auto_create(self, config)`
- `clear_cache(self)`
- `get_stats(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `base.BaseTokenizer`
- `collections.OrderedDict`
- `huggingface.HuggingFaceTokenizer`
- `mistral.MistralTokenizer`
- `models.TokenizerBackend`
- `models.TokenizerConfig`
- `threading`
- `tiktoken.TiktokenTokenizer`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
