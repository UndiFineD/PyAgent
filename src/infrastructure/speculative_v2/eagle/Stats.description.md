# Stats

**File**: `src\infrastructure\speculative_v2\eagle\Stats.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 63  
**Complexity**: 6 (moderate)

## Overview

Acceptance statistics tracking for EAGLE.

## Classes (1)

### `AcceptanceStats`

Track acceptance statistics for adaptive speculation.

**Methods** (6):
- `__init__(self, window_size)`
- `record(self, num_proposed, num_accepted)`
- `record_position(self, position, accepted)`
- `get_acceptance_rate(self)`
- `get_position_acceptance_rate(self, position)`
- `get_optimal_depth(self, min_rate)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `collections.deque`
- `threading`

---
*Auto-generated documentation*
