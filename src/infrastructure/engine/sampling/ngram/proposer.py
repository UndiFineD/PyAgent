# SPDX-License-Identifier: Apache-2.0
"""
N-gram Proposers - Implementation of speculative decoding token proposers.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import contextlib

import numpy as np

from src.infrastructure.engine.sampling.ngram.types import (
    MatchingStrategy, NgramConfig, ProposalStats
)
from src.infrastructure.engine.sampling.ngram.index import SuffixIndex
from src.infrastructure.engine.sampling.ngram.accelerators import HAS_RUST

# Try to import rust_core if available via accelerators module context
with contextlib.suppress(ImportError):
    import rust_core

if TYPE_CHECKING:
    from numpy.typing import NDArray

logger = logging.getLogger(__name__)


class NgramProposer:
    """
    N-gram based speculative token proposer.
    
    Uses n-gram matching on prompt/context to propose
    likely continuations without running a draft model.
    """
    
    def __init__(self, config: NgramConfig | None = None):
        self.config = config or NgramConfig()
        self.stats = ProposalStats()
        self._suffix_index = SuffixIndex(self.config.max_n) if self.config.use_suffix_tree else None
        self._cached_tokens: list[int] | None = None
    
    def propose(
        self,
        tokens: list[int] | NDArray[np.int32],
        num_proposals: int | None = None,
    ) -> list[int]:
        """
        Propose speculative tokens based on n-gram matching.
        """
        if num_proposals is None:
            num_proposals = self.config.num_speculative_tokens
        
        tokens_list = list(tokens)
        n_tokens = len(tokens_list)
        
        if n_tokens < self.config.min_n:
            return []
        
        # Use Rust if available
        if HAS_RUST and hasattr(rust_core, 'advanced_ngram_propose_rust'):
            result = rust_core.advanced_ngram_propose_rust(
                tokens_list,
                self.config.min_n,
                self.config.max_n,
                num_proposals,
            )
            return list(result) if result else []
        
        # Build/update suffix index if using
        if self._suffix_index is not None and self._cached_tokens != tokens_list:
            self._suffix_index.build(tokens_list)
            self._cached_tokens = tokens_list.copy()

        # Find best match
        best_proposal: list[int] = []
        best_score = -1.0
        best_ngram_size = 0
        best_position = -1
        
        # Try n-gram sizes from largest to smallest
        for n in range(self.config.max_n, self.config.min_n - 1, -1):
            if n > n_tokens:
                continue
            
            # Get the current n-gram (last n tokens)
            current_ngram = tuple(tokens_list[-(n):])
            
            # Find matches
            if self._suffix_index is not None:
                matches = self._suffix_index.lookup(current_ngram[:-1])
            else:
                matches = self._find_matches_linear(tokens_list, current_ngram[:-1])
            
            # Filter out the current position
            matches = [m for m in matches if m + n - 1 < n_tokens - 1]
            
            if not matches:
                continue
            
            # Score and select best match
            for match_pos in matches:
                proposal = self._get_continuation(
                    tokens_list, match_pos + n - 1, num_proposals
                )
                
                if not proposal:
                    continue
                
                score = self._score_match(
                    proposal, match_pos, n_tokens, n
                )
                
                if score > best_score:
                    best_score = score
                    best_proposal = proposal
                    best_ngram_size = n
                    best_position = match_pos
        
        # Update stats
        self.stats.update(
            len(best_proposal),
            best_ngram_size if best_ngram_size > 0 else self.config.min_n,
            best_position,
        )
        
        return best_proposal
    
    def _find_matches_linear(
        self,
        tokens: list[int],
        ngram: tuple[int, ...],
    ) -> list[int]:
        """Linear search for n-gram matches."""
        n = len(ngram)
        return [
            i
            for i in range(len(tokens) - n + 1)
            if tuple(tokens[i : i + n]) == ngram
        ]

    def _get_continuation(
        self,
        tokens: list[int],
        position: int,
        k: int,
    ) -> list[int]:
        """Get k tokens following a position."""
        start = position + 1
        end = min(start + k, len(tokens))
        return tokens[start:end]
    
    def _score_match(
        self,
        proposal: list[int],
        position: int,
        total_length: int,
        ngram_size: int,
    ) -> float:
        """Score a match based on strategy and configuration."""
        if not proposal:
            return -1.0
        
        base_score = len(proposal)  # Length of continuation
        
        if self.config.strategy == MatchingStrategy.FIRST:
            return base_score
        
        elif self.config.strategy == MatchingStrategy.LONGEST:
            return base_score * 10  # Prioritize length
        
        elif self.config.strategy == MatchingStrategy.RECENT:
            recency = position / max(1, total_length)
            return base_score * (1 + recency * self.config.recency_weight)
        
        elif self.config.strategy == MatchingStrategy.WEIGHTED:
            recency = position / max(1, total_length)
            ngram_bonus = ngram_size / self.config.max_n
            return base_score * (1 + recency * self.config.recency_weight + ngram_bonus)
        
        return base_score
    
    def batch_propose(
        self,
        batch_tokens: list[list[int]],
        num_proposals: int | None = None,
    ) -> list[list[int]]:
        """Batch proposal for multiple sequences."""
        if num_proposals is None:
            num_proposals = self.config.num_speculative_tokens
        
        if HAS_RUST and hasattr(rust_core, 'batch_ngram_propose_rust'):
            return [
                list(p) for p in getattr(rust_core, 'batch_ngram_propose_rust')(
                    batch_tokens,
                    self.config.min_n,
                    self.config.max_n,
                    num_proposals,
                )
            ]
        
        return [self.propose(tokens, num_proposals) for tokens in batch_tokens]
    
    def get_stats(self) -> ProposalStats:
        """Get proposal statistics."""
        return self.stats
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats.reset()
    
    def clear_cache(self) -> None:
        """Clear suffix index cache."""
        if self._suffix_index is not None:
            self._suffix_index.clear()
        self._cached_tokens = None


class AdaptiveNgramProposer(NgramProposer):
    """
    Adaptive n-gram proposer that adjusts parameters based on performance.
    """
    
    def __init__(self, config: NgramConfig | None = None):
        super().__init__(config)
        self._acceptance_history: list[float] = []
        self._adaptive_n: int = self.config.max_n
    
    def propose(
        self,
        tokens: list[int] | NDArray[np.int32],
        num_proposals: int | None = None,
    ) -> list[int]:
        """Propose with adaptive n-gram sizing."""
        original_max_n = self.config.max_n
        self.config = NgramConfig(
            min_n=self.config.min_n,
            max_n=self._adaptive_n,
            num_speculative_tokens=self.config.num_speculative_tokens,
            max_model_len=self.config.max_model_len,
            strategy=self.config.strategy,
            recency_weight=self.config.recency_weight,
        )
        
        result = super().propose(tokens, num_proposals)
        
        # Restore original config
        self.config = NgramConfig(
            min_n=self.config.min_n,
            max_n=original_max_n,
            num_speculative_tokens=self.config.num_speculative_tokens,
            max_model_len=self.config.max_model_len,
            strategy=self.config.strategy,
            recency_weight=self.config.recency_weight,
        )
        
        return result
    
    def update_acceptance(self, acceptance_rate: float) -> None:
        """Update with acceptance feedback."""
        self._acceptance_history.append(acceptance_rate)
        if len(self._acceptance_history) > 20:
            self._acceptance_history.pop(0)
        
        if len(self._acceptance_history) >= 5:
            avg_acceptance = np.mean(self._acceptance_history[-5:])
            if avg_acceptance < 0.3:
                self._adaptive_n = min(self._adaptive_n + 1, self.config.max_n + 2)
            elif avg_acceptance > 0.7:
                self._adaptive_n = max(self._adaptive_n - 1, self.config.min_n)
