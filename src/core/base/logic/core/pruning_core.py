"""
Core logic for Synaptic Pruning and Knowledge Decay.
(Facade for src.core.base.common.pruning_core)
"""

from src.core.base.common.pruning_core import PruningCore as StandardPruningCore


class PruningCore(StandardPruningCore):
    """
    Facade for StandardPruningCore to maintain backward compatibility.
    Pruning and decay logic is now centralized in the Infrastructure/Common tier.
    """
    pass
