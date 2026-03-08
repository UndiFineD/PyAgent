# FleetEconomyAgent

**File**: `src\classes\specialized\FleetEconomyAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 112  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for FleetEconomyAgent.

## Classes (1)

### `FleetEconomyAgent`

Manages internal agent "wallets", credits, and resource bidding mechanisms.
Phase 284: Implemented persistent SQLite backend and Second-Price auctions.

**Methods** (6):
- `__init__(self, workspace_path)`
- `_init_db(self)`
- `deposit_credits(self, agent_id, amount)`
- `place_bid(self, agent_id, task_id, bid_amount, priority)`
- `resolve_auction(self, task_id)`
- `get_wallet_summary(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `logging`
- `numpy`
- `pathlib.Path`
- `sqlite3`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Union`

---
*Auto-generated documentation*
