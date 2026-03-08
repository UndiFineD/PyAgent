# json

**File**: `src\core\base\parsers\reasoning\implementations\json.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for json.

## Classes (1)

### `JSONReasoningParser`

**Inherits from**: ReasoningParser

Parser for JSON-structured reasoning outputs.

Expects output in format:
{"reasoning": "...", "answer": "..."}

**Methods** (5):
- `__init__(self, tokenizer)`
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (8):
- `base.ReasoningParser`
- `json`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `re`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
