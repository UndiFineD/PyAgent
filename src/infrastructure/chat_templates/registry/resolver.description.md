# resolver

**File**: `src\infrastructure\chat_templates\registry\resolver.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 64  
**Complexity**: 5 (moderate)

## Overview

Advanced template resolution with caching.

## Classes (1)

### `TemplateResolver`

Advanced template resolution with caching.

**Methods** (5):
- `__init__(self, registry)`
- `resolve(self, model_name, model_type)`
- `_normalize_model_name(self, name)`
- `_wrap_multimodal(self, template)`
- `clear_cache(self)`

## Dependencies

**Imports** (8):
- `base.ChatTemplate`
- `config.ModelType`
- `functools.lru_cache`
- `re`
- `registry.ChatTemplateRegistry`
- `threading`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
