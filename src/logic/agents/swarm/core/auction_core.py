# Facade for AuctionCore
from src.core.base.common.auction_core import AuctionCore as StandardAuctionCore

class AuctionCore(StandardAuctionCore):
    """Facade for AuctionCore to maintain backward compatibility."""
    pass

