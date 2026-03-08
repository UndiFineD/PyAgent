
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/core/AuctionCore.description.md

# AuctionCore

**File**: `src\logic\agents\swarm\core\AuctionCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 40  
**Complexity**: 2 (simple)

## Overview

Core logic for Swarm Resource Auctioning (Phase 184).
Implements the VCG auction model for truthful bidding.

## Classes (1)

### `AuctionCore`

Class AuctionCore implementation.

**Methods** (2):
- `calculate_vcg_auction(bids, slots)`
- `enforce_vram_quota(agent_vram_request, total_available, quota_percent)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/core/AuctionCore.improvements.md

# Improvements for AuctionCore

**File**: `src\logic\agents\swarm\core\AuctionCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: AuctionCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AuctionCore_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
Core logic for Swarm Resource Auctioning (Phase 184).
Implements the VCG auction model for truthful bidding.
"""

from typing import List, Dict, Any

class AuctionCore:
    @staticmethod
    def calculate_vcg_auction(bids: list[dict[str, Any]], slots: int) -> list[dict[str, Any]]:
        """
        Simple VCG-inspired auction. 
        Winners are the top 'slots' bidders.
        Price paid by winner i = The negative externality they impose on others.
        (Simplified: Winner i pays the bid of the first loser).
        """
        if not bids:
            return []
            
        sorted_bids = sorted(bids, key=lambda x: x['amount'], reverse=True)
        winners = sorted_bids[:slots]
        
        if len(sorted_bids) > slots:
            clearing_price = sorted_bids[slots]['amount']
        else:
            clearing_price = 0.0
            
        for w in winners:
            w['price_paid'] = clearing_price
            
        return winners

    @staticmethod
    def enforce_vram_quota(agent_vram_request: float, total_available: float, quota_percent: float = 0.2) -> bool:
        """
        Checks if a request exceeds the per-agent quota (default 20%).
        """
        quota = total_available * quota_percent
        return agent_vram_request <= quota