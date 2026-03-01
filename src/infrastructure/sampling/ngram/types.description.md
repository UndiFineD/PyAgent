# types

**File**: `src\infrastructure\sampling\ngram\types.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 5 imports  
**Lines**: 78  
**Complexity**: 4 (simple)

## Overview

N-gram Proposer Types - Enums and Configuration for n-gram matching.

## Classes (3)

### `MatchingStrategy`

**Inherits from**: Enum

Strategy for n-gram matching.

### `NgramConfig`

Configuration for n-gram proposer.

**Methods** (1):
- `__post_init__(self)`

### `ProposalStats`

Statistics for n-gram proposals.

**Methods** (3):
- `update(self, proposal_length, ngram_size, position)`
- `success_rate(self)`
- `reset(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`

---
*Auto-generated documentation*
