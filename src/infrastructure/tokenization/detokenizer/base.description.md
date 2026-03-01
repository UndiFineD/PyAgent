# base

**File**: `src\infrastructure\tokenization\detokenizer\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 142  
**Complexity**: 6 (moderate)

## Overview

Base class for incremental detokenization.

## Classes (1)

### `IncrementalDetokenizer`

**Inherits from**: ABC

Abstract base class for incremental detokenization.

**Methods** (6):
- `__init__(self, tokenizer, skip_special_tokens, spaces_between_special_tokens, stop_checker)`
- `reset(self)`
- `is_finished(self)`
- `_decode_tokens(self, token_ids, prefix_offset, read_offset)`
- `update(self, new_token_ids, finished)`
- `finalize(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `src.infrastructure.tokenization.detokenizer.stop_checker.StopChecker`
- `src.infrastructure.tokenization.detokenizer.types.DetokenizeResult`
- `src.infrastructure.tokenization.detokenizer.types.TokenizerLike`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
