# index

**File**: `src\infrastructure\sampling\ngram\index.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 158  
**Complexity**: 9 (moderate)

## Overview

N-gram Indexing - Suffix-based indices for fast n-gram lookup.

## Classes (2)

### `SuffixIndex`

Suffix-based index for fast n-gram lookup.

Beyond vLLM: O(1) average case lookup for n-gram matching
using hash-based suffix indexing.

**Methods** (6):
- `__init__(self, max_n)`
- `build(self, tokens)`
- `lookup(self, ngram)`
- `get_continuations(self, prefix, tokens, k)`
- `clear(self)`
- `is_built(self)`

### `SuffixTreeProposer`

Suffix tree-based proposer for O(m) lookup complexity.

Beyond vLLM: Uses suffix tree for exact and approximate matching
with support for edit distance tolerance.

**Methods** (3):
- `__init__(self, num_speculative_tokens, max_edit_distance)`
- `build(self, tokens)`
- `find_continuation(self, prefix, tokens)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `numpy`
- `numpy.typing.NDArray`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
