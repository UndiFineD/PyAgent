"""
N-gram Proposer for Speculative Decoding.

Refactored to modular package structure for Phase 317.
"""

from src.infrastructure.sampling.ngram.types import (
    MatchingStrategy, NgramConfig, ProposalStats
)
from src.infrastructure.sampling.ngram.index import SuffixIndex, SuffixTreeProposer
from src.infrastructure.sampling.ngram.proposer import NgramProposer, AdaptiveNgramProposer
from src.infrastructure.sampling.ngram.factory import create_ngram_proposer

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
