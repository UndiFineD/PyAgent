# Models

**File**: `src\infrastructure\speculative_v2\eagle\Models.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 5 imports  
**Lines**: 62  
**Complexity**: 5 (moderate)

## Overview

Draft model wrappers and outputs for EAGLE.

## Classes (3)

### `DraftOutput`

Output from draft model forward pass.

### `DraftModelWrapper`

**Inherits from**: ABC

Abstract wrapper for draft model.

**Methods** (2):
- `forward(self, input_ids, positions, hidden_states)`
- `get_hidden_size(self)`

### `SimpleDraftModel`

**Inherits from**: DraftModelWrapper

Simple mock draft model for testing.

**Methods** (3):
- `__init__(self, vocab_size, hidden_size)`
- `forward(self, input_ids, positions, hidden_states)`
- `get_hidden_size(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `random`

---
*Auto-generated documentation*
