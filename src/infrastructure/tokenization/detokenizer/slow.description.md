# slow

**File**: `src\infrastructure\tokenization\detokenizer\slow.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 78  
**Complexity**: 3 (simple)

## Overview

Fallback incremental detokenization for non-fast tokenizers.

## Classes (1)

### `SlowIncrementalDetokenizer`

**Inherits from**: IncrementalDetokenizer

Fallback incremental detokenizer for non-fast tokenizers.

**Methods** (3):
- `__init__(self, tokenizer, skip_special_tokens, spaces_between_special_tokens, stop_checker)`
- `reset(self)`
- `_decode_tokens(self, token_ids, prefix_offset, read_offset)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.infrastructure.tokenization.detokenizer.base.IncrementalDetokenizer`
- `src.infrastructure.tokenization.detokenizer.stop_checker.StopChecker`
- `src.infrastructure.tokenization.detokenizer.types.TokenizerLike`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
