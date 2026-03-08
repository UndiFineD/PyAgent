# FleetEconomyAgent

**File**: `src\logic\agents\swarm\FleetEconomyAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 185  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for FleetEconomyAgent.

## Classes (1)

### `FleetEconomyAgent`

**Inherits from**: BaseAgent

Tier 4 (Economy) - Fleet Economy Agent: Manages internal agent "wallets", 
credits, and resource bidding mechanisms using a persistent SQLite backend.

**Methods** (9):
- `__init__(self, workspace_path)`
- `_init_db(self)`
- `deposit_credits(self, agent_id, amount)`
- `place_bid(self, agent_id, task_id, bid_amount, priority)`
- `resolve_auction(self, task_id)`
- `resolve_bids(self)`
- `get_wallet_summary(self)`
- `log_hardware_savings(self, agent_id, tokens, tps, savings_usd)`
- `get_total_savings(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `sqlite3`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
