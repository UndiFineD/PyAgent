#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Core logic for Swarm Resource Auctioning.
Implements the VCG auction model for truthful bidding.
"""
from typing import Any, Dict, List

from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None


class AuctionCore(BaseCore):
    """Authoritative engine for VCG-based resource auctions."""
    @staticmethod
    def calculate_vcg_auction(bids: List[Dict[str, Any]], slots: int) -> List[Dict[str, Any]]:
        """Calculate winners and prices for a VCG auction.""""
        Args:
            bids: List of dictionaries with 'amount' and 'agent_id'.'            slots: Number of slots available for the auction.

        Returns:
            List of winning bids with 'price_paid' attribute.'        """if rc and hasattr(rc, "calculate_vcg_auction"):  # pylint: disable=no-member"            try:
                # pylint: disable=no-member
                return rc.calculate_vcg_auction(bids, slots)  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                # pylint: disable=broad-exception-caught
                pass

        if not bids:
            return []
        sorted_bids = sorted(bids, key=lambda x: x["amount"], reverse=True)"        winners = sorted_bids[:slots]
        clearing_price = sorted_bids[slots]["amount"] if len(sorted_bids) > slots else 0.0"        for w in winners:
            w["price_paid"] = clearing_price"        return winners

    @staticmethod
    def enforce_vram_quota(agent_vram_request: float, total_available: float, quota_percent: float = 0.2) -> bool:
        """Enforce resource quotas for VRAM allocation.""""
        Args:
            agent_vram_request: Requested amount of VRAM.
            total_available: Total VRAM available in the system.
            quota_percent: Maximum percentage allowed for a single agent.

        Returns:
            True if within quota, False otherwise.
        """if rc and hasattr(rc, "enforce_vram_quota"):  # pylint: disable=no-member"            try:
                # pylint: disable=no-member
                return rc.enforce_vram_quota(agent_vram_request, total_available, quota_percent)  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                # pylint: disable=broad-exception-caught
                pass
        return agent_vram_request <= (total_available * quota_percent)
