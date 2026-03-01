# utils

**File**: `src\infrastructure\tokenizer\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 7 imports  
**Lines**: 55  
**Complexity**: 4 (simple)

## Overview

Utility functions for tokenization.

## Functions (4)

### `get_tokenizer(model_name, backend)`

Get a tokenizer from the global registry.

### `create_tokenizer(config)`

Create a tokenizer from config.

### `estimate_token_count(text, model_name)`

Fast token count estimation.

### `detect_tokenizer_backend(model_name)`

Auto-detect the appropriate tokenizer backend.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `base.BaseTokenizer`
- `models.TokenizerBackend`
- `models.TokenizerConfig`
- `registry.TokenizerRegistry`
- `rust_core`
- `typing.Optional`

---
*Auto-generated documentation*
