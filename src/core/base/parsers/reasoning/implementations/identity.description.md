# identity

**File**: `src\core\base\parsers\reasoning\implementations\identity.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 45  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for identity.

## Classes (1)

### `IdentityReasoningParser`

**Inherits from**: ReasoningParser

No-op parser that returns the full output as content.

**Methods** (4):
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (6):
- `base.ReasoningParser`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
