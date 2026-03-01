# stop_checker

**File**: `src\infrastructure\tokenization\detokenizer\stop_checker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 74  
**Complexity**: 4 (simple)

## Overview

Stop condition checker for detokenization.

## Classes (1)

### `StopChecker`

Checks for stop conditions in generated text.

Handles both stop strings and stop token IDs.

**Methods** (4):
- `__init__(self, stop_strings, stop_token_ids, eos_token_id, include_stop_string_in_output)`
- `check_token(self, token_id)`
- `check_text(self, text)`
- `check_partial(self, text)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `rust_core.check_stop_tokens_rust`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
