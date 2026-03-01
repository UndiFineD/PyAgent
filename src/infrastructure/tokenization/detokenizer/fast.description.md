# fast

**File**: `src\infrastructure\tokenization\detokenizer\fast.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 100  
**Complexity**: 3 (simple)

## Overview

Fast incremental detokenization for HuggingFace fast tokenizers.

## Classes (1)

### `FastIncrementalDetokenizer`

**Inherits from**: IncrementalDetokenizer

Fast incremental detokenizer for HuggingFace fast tokenizers.

**Methods** (3):
- `__init__(self, tokenizer, skip_special_tokens, spaces_between_special_tokens, stop_checker)`
- `special_token_ids(self)`
- `_decode_tokens(self, token_ids, prefix_offset, read_offset)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `rust_core.update_prefix_offset_rust`
- `src.infrastructure.tokenization.detokenizer.base.IncrementalDetokenizer`
- `src.infrastructure.tokenization.detokenizer.stop_checker.StopChecker`
- `src.infrastructure.tokenization.detokenizer.types.TokenizerLike`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
