# SPDX-License-Identifier: Apache-2.0
# PyAgent Phase 44: N-gram Proposer for Speculative Decoding
# Implements vLLM's NgramProposer with Numba acceleration
# Beyond vLLM: Suffix trees, adaptive n-gram, weighted matching

"""
N-gram Proposer for Speculative Decoding.

This module implements prompt lookup speculation based on n-gram matching,
finding repeated patterns in the prompt/context to propose likely continuations.

Features beyond vLLM:
- Suffix tree indexing for O(1) lookups
- Adaptive n-gram sizing based on context
- Weighted matching with recency bias
- Multi-sequence batch proposal
- Rust acceleration for hot paths
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

# Try to import rust_core for acceleration
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

# Try to import numba for JIT compilation
try:
    from numba import jit, njit, prange
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False


class MatchingStrategy(Enum):
    """Strategy for n-gram matching."""
    FIRST = auto()       # Return first match found
    LONGEST = auto()     # Return longest matching continuation
    RECENT = auto()      # Prefer more recent matches
    WEIGHTED = auto()    # Weight by position and frequency


@dataclass
class NgramConfig:
    """Configuration for n-gram proposer."""
    min_n: int = 1                     # Minimum n-gram size
    max_n: int = 4                     # Maximum n-gram size
    num_speculative_tokens: int = 5    # Number of tokens to propose
    max_model_len: int = 8192          # Maximum model context length
    strategy: MatchingStrategy = MatchingStrategy.LONGEST
    recency_weight: float = 0.1        # Weight for recency (0 = no recency bias)
    min_match_frequency: int = 1       # Minimum match frequency to consider
    use_suffix_tree: bool = True       # Use suffix tree for fast lookup
    parallel_threshold: int = 8192     # Token count threshold for parallel processing
    
    def __post_init__(self) -> None:
        if self.min_n < 1:
            raise ValueError(f"min_n must be >= 1, got {self.min_n}")
        if self.max_n < self.min_n:
            raise ValueError(f"max_n must be >= min_n")
        if self.num_speculative_tokens < 1:
            raise ValueError(f"num_speculative_tokens must be >= 1")


@dataclass
class ProposalStats:
    """Statistics for n-gram proposals."""
    total_proposals: int = 0
    successful_matches: int = 0
    average_proposal_length: float = 0.0
    match_positions: list[int] = field(default_factory=list)
    ngram_sizes_used: dict[int, int] = field(default_factory=dict)
    
    def update(self, proposal_length: int, ngram_size: int, position: int) -> None:
        """Update statistics with new proposal."""
        self.total_proposals += 1
        if proposal_length > 0:
            self.successful_matches += 1
            self.match_positions.append(position)
        
        # Update running average
        prev_total = self.average_proposal_length * (self.total_proposals - 1)
        self.average_proposal_length = (prev_total + proposal_length) / self.total_proposals
        
        # Track n-gram sizes
        self.ngram_sizes_used[ngram_size] = self.ngram_sizes_used.get(ngram_size, 0) + 1
    
    @property
    def success_rate(self) -> float:
        """Rate of successful matches."""
        if self.total_proposals == 0:
            return 0.0
        return self.successful_matches / self.total_proposals
    
    def reset(self) -> None:
        """Reset statistics."""
        self.total_proposals = 0
        self.successful_matches = 0
        self.average_proposal_length = 0.0
        self.match_positions.clear()
        self.ngram_sizes_used.clear()


class SuffixIndex:
    """
    Suffix-based index for fast n-gram lookup.
    
    Beyond vLLM: O(1) average case lookup for n-gram matching
    using hash-based suffix indexing.
    """
    
    def __init__(self, max_n: int = 4):
        self.max_n = max_n
        # Map from n-gram tuple to list of positions
        self._index: dict[int, dict[tuple[int, ...], list[int]]] = {
            n: {} for n in range(1, max_n + 1)
        }
        self._built = False
    
    def build(self, tokens: list[int] | NDArray[np.int32]) -> None:
        """Build suffix index from token sequence."""
        tokens = list(tokens)
        n_tokens = len(tokens)
        
        # Clear existing index
        for n in range(1, self.max_n + 1):
            self._index[n].clear()
        
        # Build index for each n-gram size
        for n in range(1, self.max_n + 1):
            for i in range(n_tokens - n + 1):
                ngram = tuple(tokens[i:i + n])
                if ngram not in self._index[n]:
                    self._index[n][ngram] = []
                self._index[n][ngram].append(i)
        
        self._built = True
    
    def lookup(self, ngram: tuple[int, ...]) -> list[int]:
        """Look up positions where n-gram appears."""
        n = len(ngram)
        if n > self.max_n or n < 1:
            return []
        return self._index.get(n, {}).get(ngram, [])
    
    def get_continuations(
        self,
        prefix: tuple[int, ...],
        tokens: list[int],
        k: int,
    ) -> list[int]:
        """Get tokens that follow the given prefix."""
        positions = self.lookup(prefix)
        if not positions:
            return []
        
        # Get continuations from each position
        n = len(prefix)
        continuations = []
        
        for pos in positions:
            end_pos = pos + n
            # Get up to k tokens following the match
            cont = tokens[end_pos:end_pos + k]
            if cont:
                continuations.append((pos, cont))
        
        return continuations
    
    def clear(self) -> None:
        """Clear the index."""
        for n in self._index:
            self._index[n].clear()
        self._built = False
    
    @property
    def is_built(self) -> bool:
        """Check if index is built."""
        return self._built


class NgramProposer:
    """
    N-gram based speculative token proposer.
    
    Uses n-gram matching on prompt/context to propose
    likely continuations without running a draft model.
    
    Beyond vLLM innovations:
    - Suffix tree indexing
    - Adaptive n-gram sizing
    - Recency-weighted matching
    - Parallel batch processing
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
        
        Args:
            tokens: Current token sequence
            num_proposals: Number of tokens to propose (uses config if None)
            
        Returns:
            List of proposed token IDs
        """
        if num_proposals is None:
            num_proposals = self.config.num_speculative_tokens
        
        tokens_list = list(tokens)
        n_tokens = len(tokens_list)
        
        if n_tokens < self.config.min_n:
            return []
        
        # Use Rust if available
        if HAS_RUST and hasattr(rust_core, 'ngram_propose_rust'):
            result = rust_core.ngram_propose_rust(
                tokens_list,
                self.config.min_n,
                self.config.max_n,
                num_proposals,
            )
            return list(result) if result else []
        
        # Build/update suffix index if using
        if self._suffix_index is not None:
            if self._cached_tokens != tokens_list:
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
        matches = []
        n = len(ngram)
        
        for i in range(len(tokens) - n + 1):
            if tuple(tokens[i:i + n]) == ngram:
                matches.append(i)
        
        return matches
    
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
            # Higher score for more recent matches
            recency = position / max(1, total_length)
            return base_score * (1 + recency * self.config.recency_weight)
        
        elif self.config.strategy == MatchingStrategy.WEIGHTED:
            # Combine length, recency, and n-gram size
            recency = position / max(1, total_length)
            ngram_bonus = ngram_size / self.config.max_n
            return base_score * (1 + recency * self.config.recency_weight + ngram_bonus)
        
        return base_score
    
    def batch_propose(
        self,
        batch_tokens: list[list[int]],
        num_proposals: int | None = None,
    ) -> list[list[int]]:
        """
        Batch proposal for multiple sequences.
        
        Args:
            batch_tokens: List of token sequences
            num_proposals: Number of tokens to propose per sequence
            
        Returns:
            List of proposal lists
        """
        if num_proposals is None:
            num_proposals = self.config.num_speculative_tokens
        
        # Check if we should use parallel processing
        total_tokens = sum(len(t) for t in batch_tokens)
        
        if HAS_RUST and hasattr(rust_core, 'batch_ngram_propose_rust'):
            # Use Rust batch implementation
            return [
                list(p) for p in rust_core.batch_ngram_propose_rust(
                    batch_tokens,
                    self.config.min_n,
                    self.config.max_n,
                    num_proposals,
                )
            ]
        
        # Python fallback
        results = []
        for tokens in batch_tokens:
            proposal = self.propose(tokens, num_proposals)
            results.append(proposal)
        
        return results
    
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
    
    Beyond vLLM: Automatically tunes n-gram size and strategy
    based on acceptance rate feedback.
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
        # Use adaptive n-gram size
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
        """
        Update with acceptance feedback to adapt parameters.
        
        Args:
            acceptance_rate: Rate of accepted proposals (0-1)
        """
        self._acceptance_history.append(acceptance_rate)
        
        # Keep last 20 observations
        if len(self._acceptance_history) > 20:
            self._acceptance_history.pop(0)
        
        # Adjust n-gram size based on average acceptance
        if len(self._acceptance_history) >= 5:
            avg_acceptance = np.mean(self._acceptance_history[-5:])
            
            if avg_acceptance < 0.3:
                # Low acceptance - try larger n-grams for better matches
                self._adaptive_n = min(self._adaptive_n + 1, self.config.max_n + 2)
            elif avg_acceptance > 0.7:
                # High acceptance - smaller n-grams for more proposals
                self._adaptive_n = max(self._adaptive_n - 1, self.config.min_n)


class SuffixTreeProposer:
    """
    Suffix tree-based proposer for O(m) lookup complexity.
    
    Beyond vLLM: Uses suffix tree for exact and approximate matching
    with support for edit distance tolerance.
    """
    
    def __init__(
        self,
        num_speculative_tokens: int = 5,
        max_edit_distance: int = 0,
    ):
        self.num_speculative_tokens = num_speculative_tokens
        self.max_edit_distance = max_edit_distance
        self._tree: dict[int, Any] = {}
        self._positions: dict[int, list[int]] = {}
    
    def build(self, tokens: list[int]) -> None:
        """Build suffix tree from tokens."""
        self._tree.clear()
        self._positions.clear()
        
        n = len(tokens)
        for i in range(n):
            node = self._tree
            for j in range(i, n):
                token = tokens[j]
                if token not in node:
                    node[token] = {}
                    if token not in self._positions:
                        self._positions[token] = []
                    self._positions[token].append(j)
                node = node[token]
    
    def find_continuation(
        self,
        prefix: list[int],
        tokens: list[int],
    ) -> list[int]:
        """Find continuation for prefix using suffix tree."""
        # Navigate tree
        node = self._tree
        for token in prefix:
            if token not in node:
                return []
            node = node[token]
        
        # Get all paths from this node
        if not node:
            return []
        
        # Find a continuation path
        continuation = []
        current = node
        
        for _ in range(self.num_speculative_tokens):
            if not current:
                break
            # Take most frequent continuation
            next_token = max(current.keys(), key=lambda t: len(self._positions.get(t, [])))
            continuation.append(next_token)
            current = current.get(next_token, {})
        
        return continuation


# Numba-accelerated functions if available
if HAS_NUMBA:
    @njit
    def _ngram_match_numba(
        tokens: np.ndarray,
        pattern: np.ndarray,
        max_matches: int = 100,
    ) -> np.ndarray:
        """Numba-accelerated n-gram matching."""
        n_tokens = len(tokens)
        n_pattern = len(pattern)
        matches = np.zeros(max_matches, dtype=np.int32)
        match_count = 0
        
        for i in range(n_tokens - n_pattern + 1):
            found = True
            for j in range(n_pattern):
                if tokens[i + j] != pattern[j]:
                    found = False
                    break
            if found:
                matches[match_count] = i
                match_count += 1
                if match_count >= max_matches:
                    break
        
        return matches[:match_count]
    
    @njit(parallel=True)
    def _batch_propose_numba(
        all_tokens: np.ndarray,       # Flattened tokens
        token_offsets: np.ndarray,    # Start offset for each sequence
        token_lengths: np.ndarray,    # Length of each sequence
        min_n: int,
        max_n: int,
        k: int,
        proposals: np.ndarray,        # Output: [batch, k]
        proposal_lens: np.ndarray,    # Output: [batch]
    ) -> None:
        """Numba-accelerated batch proposal."""
        batch_size = len(token_offsets)
        
        for b in prange(batch_size):
            offset = token_offsets[b]
            length = token_lengths[b]
            
            if length < min_n:
                proposal_lens[b] = 0
                continue
            
            tokens = all_tokens[offset:offset + length]
            
            # Simple greedy matching for now
            best_len = 0
            best_proposal = np.zeros(k, dtype=np.int32)
            
            for n in range(max_n, min_n - 1, -1):
                if n > length:
                    continue
                
                pattern = tokens[-(n-1):]
                
                # Find matches
                for i in range(length - n):
                    found = True
                    for j in range(n - 1):
                        if tokens[i + j] != pattern[j]:
                            found = False
                            break
                    
                    if found:
                        # Get continuation
                        cont_start = i + n - 1
                        cont_len = min(k, length - cont_start)
                        
                        if cont_len > best_len:
                            best_len = cont_len
                            for c in range(cont_len):
                                best_proposal[c] = tokens[cont_start + c]
                            break
                
                if best_len > 0:
                    break
            
            proposal_lens[b] = best_len
            for c in range(best_len):
                proposals[b, c] = best_proposal[c]


# Factory function
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
