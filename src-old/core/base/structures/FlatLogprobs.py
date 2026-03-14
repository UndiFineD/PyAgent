r"""LLM_CONTEXT_START

## Source: src-old/core/base/structures/FlatLogprobs.description.md

# FlatLogprobs

**File**: `src\\core\base\\structures\\FlatLogprobs.py`  
**Type**: Python Module  
**Summary**: 3 classes, 2 functions, 9 imports  
**Lines**: 331  
**Complexity**: 22 (complex)

## Overview

FlatLogprobs - Memory-efficient flat storage for token log probabilities.

Inspired by vLLM's FlatLogprobs pattern for reduced GC overhead compared
to list[dict[int, Logprob]] by flattening into primitive type arrays.

Phase 24: Advanced Observability & Parsing

## Classes (3)

### `Logprob`

Log probability information for a single token.

Attributes:
    logprob: The log probability of the token
    rank: The vocab rank of the token (1-based, or None)
    decoded_token: The decoded string representation

### `FlatLogprobs`

**Inherits from**: Unknown

Memory-efficient flat storage for log probabilities.

Compared to list[dict[int, Logprob]], this data structure reduces GC
overhead significantly by flattening logprob information for all positions
and ranks into primitive type lists.

Regardless of sequence length and top_logprobs settings, FlatLogprobs
introduces only a constant number of objects.

Example:
    logprobs = FlatLogprobs()
    logprobs.append({
        100: Logprob(logprob=-0.5, rank=1, decoded_token="hello"),
        200: Logprob(logprob=-1.2, rank=2, decoded_token="world"),
    })
    
    # Access like a list
    position_0 = logprobs[0]  # Returns dict[int, Logprob]

**Methods** (14):
- `append(self, logprobs_one_position)`
- `append_fast(self, token_ids, logprobs, ranks, decoded_tokens)`
- `extend(self, logprobs_multi_positions)`
- `__len__(self)`
- `__getitem__(self, position)`
- `__getitem__(self, s)`
- `__getitem__(self, index)`
- `__setitem__(self, index, value)`
- `__delitem__(self, index)`
- `insert(self, index, value)`
- ... and 4 more methods

### `LogprobsAccumulator`

Accumulator for building FlatLogprobs incrementally.

Provides a builder pattern for constructing logprobs
with validation and statistics.

**Methods** (6):
- `add_position(self, token_ids, logprobs, ranks, decoded_tokens)`
- `build(self)`
- `num_positions(self)`
- `total_entries(self)`
- `min_logprob(self)`
- `max_logprob(self)`

## Functions (2)

### `create_prompt_logprobs(flat_logprobs)`

Create a container for prompt logprobs.

Args:
    flat_logprobs: If True, use memory-efficient FlatLogprobs
    
Returns:
    Empty container with None appended for first token

### `create_sample_logprobs(flat_logprobs)`

Create a container for sampled (decode) logprobs.

Args:
    flat_logprobs: If True, use memory-efficient FlatLogprobs
    
Returns:
    Empty container for storing decode logprobs

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `collections.abc.Iterable`
- `collections.abc.Iterator`
- `collections.abc.MutableSequence`
- `collections.abc.Sequence`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.overload`

---
*Auto-generated documentation*
## Source: src-old/core/base/structures/FlatLogprobs.improvements.md

# Improvements for FlatLogprobs

**File**: `src\\core\base\\structures\\FlatLogprobs.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 331 lines (medium)  
**Complexity**: 22 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FlatLogprobs_test.py` with pytest tests

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
