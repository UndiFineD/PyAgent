# AgentEconomy

**File**: `src\classes\fleet\AgentEconomy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 80  
**Complexity**: 7 (moderate)

## Overview

Agent economy and accounting engine.
Manages credits, bidding, and automated payments between agents.

## Classes (1)

### `AgentEconomy`

Manages internal marketplace credits and task bidding.

**Methods** (7):
- `__init__(self)`
- `_initialize_genesis_block(self)`
- `_hash_block(self, block)`
- `get_balance(self, agent_id)`
- `transfer_credits(self, sender, receiver, amount, reason)`
- `_record_transaction(self, sender, receiver, amount, reason)`
- `place_bid(self, agent_id, task_id, bid_amount)`

## Dependencies

**Imports** (8):
- `hashlib`
- `json`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
