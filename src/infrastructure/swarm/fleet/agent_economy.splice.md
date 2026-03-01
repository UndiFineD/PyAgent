# Class Breakdown: agent_economy

**File**: `src\infrastructure\swarm\fleet\agent_economy.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MarketPricingEngine`

**Line**: 32  
**Methods**: 1

Calculates dynamic pricing based on system load, hardware specs, and model types.

[TIP] **Suggested split**: Move to `marketpricingengine.py`

---

### 2. `AgentEconomy`

**Line**: 66  
**Methods**: 8

Manages internal marketplace credits and task bidding.

[TIP] **Suggested split**: Move to `agenteconomy.py`

---

### 3. `AuctionOrchestrator`

**Line**: 152  
**Methods**: 6

Orchestrates auctions for task allocation across the swarm.

[TIP] **Suggested split**: Move to `auctionorchestrator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
