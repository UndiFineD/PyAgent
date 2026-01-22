#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Core logic for Swarm Resource Auctioning.
Implements the VCG auction model for truthful bidding.
"""

from typing import Any, List, Dict, Optional
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

class AuctionCore(BaseCore):
    """Authoritative engine for VCG-based resource auctions."""

    @staticmethod
    def calculate_vcg_auction(
        bids: List[Dict[str, Any]], slots: int
    ) -> List[Dict[str, Any]]:
        if rc:
            try:
                return rc.calculate_vcg_auction(bids, slots)
            except Exception:
                pass
        
        if not bids: return []
        sorted_bids = sorted(bids, key=lambda x: x["amount"], reverse=True)
        winners = sorted_bids[:slots]
        clearing_price = sorted_bids[slots]["amount"] if len(sorted_bids) > slots else 0.0
        for w in winners: w["price_paid"] = clearing_price
        return winners

    @staticmethod
    def enforce_vram_quota(
        agent_vram_request: float, total_available: float, quota_percent: float = 0.2
    ) -> bool:
        if rc:
            try:
                return rc.enforce_vram_quota(agent_vram_request, total_available, quota_percent)
            except Exception:
                pass
        return agent_vram_request <= (total_available * quota_percent)
