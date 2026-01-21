# SPDX-License-Identifier: Apache-2.0
"""
N-gram Proposer Package - Speculative decoding via pattern matching.
"""

from src.infrastructure.engine.sampling.ngram.types import (
    MatchingStrategy, NgramConfig, ProposalStats
)
from src.infrastructure.engine.sampling.ngram.index import SuffixIndex, SuffixTreeProposer
from src.infrastructure.engine.sampling.ngram.proposer import NgramProposer, AdaptiveNgramProposer
from src.infrastructure.engine.sampling.ngram.factory import create_ngram_proposer

__all__ = [
    "MatchingStrategy",
    "NgramConfig",
    "ProposalStats",
    "SuffixIndex",
    "NgramProposer",
    "AdaptiveNgramProposer",
    "SuffixTreeProposer",
    "create_ngram_proposer",
]
