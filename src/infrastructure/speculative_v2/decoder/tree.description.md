# tree

**File**: `src\infrastructure\speculative_v2\decoder\tree.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 81  
**Complexity**: 6 (moderate)

## Overview

Tree structure for speculative tokens.

## Classes (2)

### `SpeculativeToken`

A single speculative token with metadata.

### `SpeculativeTree`

Tree structure for speculative tokens.

Represents a tree of candidate tokens where each node
can have multiple children (branching speculation).

**Methods** (6):
- `add_token(self, token_id, position, parent_idx, probability)`
- `get_path_to_root(self, idx)`
- `get_children(self, idx)`
- `get_leaves(self)`
- `to_sequences(self)`
- `__len__(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
