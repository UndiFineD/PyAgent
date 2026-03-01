# factory

**File**: `src\infrastructure\tokenization\detokenizer\factory.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 10 imports  
**Lines**: 86  
**Complexity**: 2 (simple)

## Overview

Factory for incremental detokenizers.

## Functions (2)

### `create_detokenizer(tokenizer, skip_special_tokens, spaces_between_special_tokens, stop_strings, stop_token_ids, use_fast)`

Create an appropriate detokenizer for the given tokenizer.

### `detokenize_incrementally(tokenizer, token_ids, skip_special_tokens, spaces_between_special_tokens, stop_strings)`

Convenience function to detokenize a sequence of tokens.

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `src.infrastructure.tokenization.detokenizer.base.IncrementalDetokenizer`
- `src.infrastructure.tokenization.detokenizer.fast.FastIncrementalDetokenizer`
- `src.infrastructure.tokenization.detokenizer.slow.SlowIncrementalDetokenizer`
- `src.infrastructure.tokenization.detokenizer.stop_checker.StopChecker`
- `src.infrastructure.tokenization.detokenizer.types.TokenizerLike`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
