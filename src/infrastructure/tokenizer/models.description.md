# models

**File**: `src\infrastructure\tokenizer\models.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 11 imports  
**Lines**: 151  
**Complexity**: 6 (moderate)

## Overview

Models and configurations for tokenization.

## Classes (8)

### `TokenizerBackend`

**Inherits from**: Enum

Supported tokenizer backends.

### `SpecialTokenHandling`

**Inherits from**: Enum

How to handle special tokens.

### `TruncationStrategy`

**Inherits from**: Enum

Truncation strategies for long sequences.

### `PaddingStrategy`

**Inherits from**: Enum

Padding strategies for batched inputs.

### `TokenizerConfig`

Configuration for tokenizer initialization.

**Methods** (1):
- `__hash__(self)`

### `TokenizerInfo`

Information about a loaded tokenizer.

**Methods** (1):
- `to_dict(self)`

### `TokenizeResult`

Result of tokenization.

**Methods** (2):
- `__post_init__(self)`
- `to_numpy(self)`

### `BatchTokenizeResult`

Result of batch tokenization.

**Methods** (2):
- `__post_init__(self)`
- `pad_to_max(self, pad_token_id)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
