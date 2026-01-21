# SPDX-License-Identifier: Apache-2.0
"""
N-gram Proposer Factory - Helper functions to instantiate proposers.
"""

from __future__ import annotations

from typing import Any

from src.infrastructure.engine.sampling.ngram.types import MatchingStrategy, NgramConfig
from src.infrastructure.engine.sampling.ngram.proposer import NgramProposer, AdaptiveNgramProposer


def create_ngram_proposer(
    strategy: str = "longest",
    use_suffix_tree: bool = True,
    adaptive: bool = False,
    **kwargs: Any,
) -> NgramProposer:
    """
    Factory function to create n-gram proposer.
    
    Args:
        strategy: "first", "longest", "recent", "weighted"
        use_suffix_tree: Use suffix tree indexing
        adaptive: Use adaptive n-gram sizing
        **kwargs: Additional NgramConfig parameters
    """
    strategy_map = {
        "first": MatchingStrategy.FIRST,
        "longest": MatchingStrategy.LONGEST,
        "recent": MatchingStrategy.RECENT,
        "weighted": MatchingStrategy.WEIGHTED,
    }
    
    config = NgramConfig(
        strategy=strategy_map.get(strategy, MatchingStrategy.LONGEST),
        use_suffix_tree=use_suffix_tree,
        **kwargs,
    )
    
    if adaptive:
        return AdaptiveNgramProposer(config)
    return NgramProposer(config)
