# Tree

**File**: `src\infrastructure\speculative_v2\eagle\Tree.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 7 imports  
**Lines**: 191  
**Complexity**: 9 (moderate)

## Overview

Speculative tree structures for EAGLE.

## Classes (3)

### `TreeNode`

Node in speculative decoding tree.

**Methods** (3):
- `add_child(self, token_id, logprob, confidence)`
- `path_to_root(self)`
- `all_leaves(self)`

### `SpeculativeTree`

Tree structure for tree-based speculative decoding.

**Methods** (4):
- `create(cls, root_token_id, max_depth, confidence_threshold)`
- `expand(self, node, candidates, max_width)`
- `get_all_paths(self)`
- `prune(self, accepted_depth)`

### `TalonTreeBuilder`

Implements Budget-Driven Adaptive Tree Expansion (arXiv:2601.07353).

**Methods** (2):
- `__init__(self, budget, max_depth, confidence_threshold, branching_factor)`
- `build_tree(self, root_token_id, get_candidates_fn)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `heapq.heappop`
- `heapq.heappush`
- `math`
- `typing.cast`

---
*Auto-generated documentation*
