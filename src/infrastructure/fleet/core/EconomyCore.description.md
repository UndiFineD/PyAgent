# EconomyCore

**File**: `src\infrastructure\fleet\core\EconomyCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 34  
**Complexity**: 3 (simple)

## Overview

Core logic for Swarm Economy (Phase 179).
Handles bidding and GPU priority allocation logic.

## Classes (1)

### `EconomyCore`

Class EconomyCore implementation.

**Methods** (3):
- `calculate_bid_priority(credits, importance, urgency)`
- `select_winning_bids(bids, slots_available)`
- `calculate_gpu_surcharge(vram_needed_gb, current_utilization)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
