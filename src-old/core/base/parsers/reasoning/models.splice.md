# Class Breakdown: models

**File**: `src\core\base\parsers\reasoning\models.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReasoningResult`

**Line**: 7  
**Methods**: 0

Result of reasoning extraction.

Attributes:
    reasoning: The extracted reasoning/thinking content.
    content: The extracted content/answer.
    reasoning_tokens: Token IDs for reasoning (if avail...

[TIP] **Suggested split**: Move to `reasoningresult.py`

---

### 2. `StreamingReasoningState`

**Line**: 26  
**Methods**: 0

State for streaming reasoning extraction.

Tracks the current state of reasoning extraction during streaming.

[TIP] **Suggested split**: Move to `streamingreasoningstate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
