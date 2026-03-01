# base

**File**: `src\infrastructure\prompt_renderer\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 62  
**Complexity**: 6 (moderate)

## Overview

Base Prompt Renderer class.

## Classes (1)

### `PromptRenderer`

**Inherits from**: ABC

Abstract base class for prompt renderers.

**Methods** (6):
- `__init__(self, tokenizer, max_model_tokens)`
- `render(self, config)`
- `_tokenize(self, text, add_special_tokens)`
- `_detokenize(self, tokens)`
- `_apply_truncation(self, tokens, config)`
- `_generate_cache_salt(self, config)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `models.PromptConfig`
- `models.RenderResult`
- `models.TruncationResult`
- `models.TruncationStrategy`
- `salt.CacheSaltGenerator`
- `truncation.TruncationManager`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
