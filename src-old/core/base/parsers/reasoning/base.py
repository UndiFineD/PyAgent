r"""LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/base.description.md

# base

**File**: `src\\core\base\\parsers\reasoning\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 131  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for base.

## Classes (1)

### `ReasoningParser`

**Inherits from**: ABC

Abstract reasoning parser class for extracting reasoning from model outputs.

Subclasses must implement:
- is_reasoning_end: Check if reasoning section has ended
- extract_content_ids: Extract content token IDs from full output
- extract_reasoning: Extract reasoning from complete output
- extract_reasoning_streaming: Extract reasoning incrementally

Attributes:
    tokenizer: The tokenizer used for token-level operations.

**Methods** (7):
- `__init__(self, tokenizer)`
- `vocab(self)`
- `is_reasoning_end(self, input_ids)`
- `is_reasoning_end_streaming(self, input_ids, delta_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `functools.cached_property`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/base.improvements.md

# Improvements for base

**File**: `src\\core\base\\parsers\reasoning\base.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `base_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""
