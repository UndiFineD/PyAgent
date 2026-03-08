# markdown

**File**: `src\core\base\parsers\reasoning\implementations\markdown.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 84  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for markdown.

## Classes (1)

### `MarkdownReasoningParser`

**Inherits from**: ReasoningParser

Parser for Markdown-style think blocks.

Extracts reasoning from ```thinking blocks or > prefixed lines.

**Methods** (5):
- `__init__(self, tokenizer)`
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (7):
- `base.ReasoningParser`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `re`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
