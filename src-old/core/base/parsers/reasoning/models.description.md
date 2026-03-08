# models

**File**: `src\core\base\parsers\reasoning\models.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 2 imports  
**Lines**: 37  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for models.

## Classes (2)

### `ReasoningResult`

Result of reasoning extraction.

Attributes:
    reasoning: The extracted reasoning/thinking content.
    content: The extracted content/answer.
    reasoning_tokens: Token IDs for reasoning (if available).
    content_tokens: Token IDs for content (if available).
    is_complete: Whether reasoning extraction is complete.

### `StreamingReasoningState`

State for streaming reasoning extraction.

Tracks the current state of reasoning extraction during streaming.

## Dependencies

**Imports** (2):
- `dataclasses.dataclass`
- `dataclasses.field`

---
*Auto-generated documentation*
