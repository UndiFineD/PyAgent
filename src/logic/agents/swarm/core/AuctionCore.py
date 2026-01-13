
"""
Core logic for Swarm Resource Auctioning (Phase 184).
Implements the VCG auction model for truthful bidding.
"""

from typing import List, Dict, Any

class AuctionCore:
    @staticmethod
    def calculate_vcg_auction(bids: List[Dict[str, Any]], slots: int) -> List[Dict[str, Any]]:
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