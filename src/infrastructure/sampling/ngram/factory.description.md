# factory

**File**: `src\infrastructure\sampling\ngram\factory.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 6 imports  
**Lines**: 44  
**Complexity**: 1 (simple)

## Overview

N-gram Proposer Factory - Helper functions to instantiate proposers.

## Functions (1)

### `create_ngram_proposer(strategy, use_suffix_tree, adaptive)`

Factory function to create n-gram proposer.

Args:
    strategy: "first", "longest", "recent", "weighted"
    use_suffix_tree: Use suffix tree indexing
    adaptive: Use adaptive n-gram sizing
    **kwargs: Additional NgramConfig parameters

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.infrastructure.sampling.ngram.proposer.AdaptiveNgramProposer`
- `src.infrastructure.sampling.ngram.proposer.NgramProposer`
- `src.infrastructure.sampling.ngram.types.MatchingStrategy`
- `src.infrastructure.sampling.ngram.types.NgramConfig`
- `typing.Any`

---
*Auto-generated documentation*
