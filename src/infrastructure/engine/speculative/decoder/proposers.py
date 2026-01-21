# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Implementations of speculative token proposers."""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import time
from .tree import SpeculativeTree


@dataclass
class ProposerStats:
    """Statistics for a proposer."""
    proposals_made: int = 0
    tokens_proposed: int = 0
    tokens_accepted: int = 0
    proposal_time_ms: float = 0.0

    @property
    def acceptance_rate(self) -> float:
        if self.tokens_proposed == 0:
            return 0.0
        return self.tokens_accepted / self.tokens_proposed

    @property
    def avg_proposal_time_ms(self) -> float:
        if self.proposals_made == 0:
            return 0.0
        return self.proposal_time_ms / self.proposals_made


class SpeculativeProposer(ABC):
    """Abstract base class for speculative token proposers."""

    def __init__(self, vocab_size: int, max_speculation_depth: int = 5):
        self.vocab_size = vocab_size
        self.max_speculation_depth = max_speculation_depth
        self.stats = ProposerStats()

    @abstractmethod
    def propose(
        self,
        input_ids: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        num_candidates: int = 5
    ) -> SpeculativeTree:
        """Propose speculative tokens."""
        pass

    @abstractmethod
    def update(self, accepted_tokens: List[int], rejected_at: int) -> None:
        """Update proposer state after verification."""
        pass

    def get_stats(self) -> ProposerStats:
        """Get copy of proposer statistics."""
        return ProposerStats(
            proposals_made=self.stats.proposals_made,
            tokens_proposed=self.stats.tokens_proposed,
            tokens_accepted=self.stats.tokens_accepted,
            proposal_time_ms=self.stats.proposal_time_ms,
        )

    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = ProposerStats()


class NgramProposer(SpeculativeProposer):
    """N-gram based speculative proposer."""

    def __init__(self, vocab_size: int, max_speculation_depth: int = 5, ngram_order: int = 4, min_count: int = 1):
        super().__init__(vocab_size, max_speculation_depth)
        self.ngram_order = ngram_order
        self.min_count = min_count
        self._ngram_tables = {n: {} for n in range(1, ngram_order + 1)}

    def _update_ngrams(self, tokens: List[int]):
        """Update ngram tables with newly seen tokens."""
        for n in range(1, self.ngram_order + 1):
            table = self._ngram_tables[n]
            for i in range(len(tokens) - n):
                context = tuple(tokens[i:i + n])
                next_token = tokens[i + n]
                if context not in table:
                    table[context] = {}
                table[context][next_token] = table[context].get(next_token, 0) + 1

    def _get_predictions(self, context: List[int], top_k: int = 5) -> List[Tuple[int, float]]:
        """Get best token predictions for the current context."""
        predictions: Dict[int, float] = {}
        for n in range(self.ngram_order, 0, -1):
            if len(context) >= n:
                ctx = tuple(context[-n:])
                table = self._ngram_tables[n]
                if ctx in table:
                    counts = table[ctx]
                    total = sum(counts.values())
                    for token, count in counts.items():
                        if count >= self.min_count:
                            prob = (count / total) * (n / self.ngram_order)
                            predictions[token] = max(predictions.get(token, 0), prob)
        return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def propose(
        self,
        input_ids: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        num_candidates: int = 5
    ) -> SpeculativeTree:
        """Propose speculative tokens using n-gram lookup."""
        start = time.perf_counter()
        tokens = input_ids.tolist()
        self._update_ngrams(tokens)

        tree = SpeculativeTree(root_position=len(tokens))

        def expand_node(parent_idx: int, context: List[int], depth: int):
            if depth >= self.max_speculation_depth:
                return

            preds = self._get_predictions(context, num_candidates)
            for token_id, prob in preds:
                idx = tree.add_token(token_id, len(tokens) + depth, parent_idx, prob)
                # Simple recursive expansion for branching (limited depth)
                if depth < 2:
                    expand_node(idx, context + [token_id], depth + 1)

        expand_node(-1, tokens, 0)

        self.stats.proposals_made += 1
        self.stats.tokens_proposed += len(tree)
        self.stats.proposal_time_ms += (time.perf_counter() - start) * 1000
        return tree

    def update(self, accepted_tokens: List[int], rejected_at: int):
        """Update statistics."""
        self.stats.tokens_accepted += len(accepted_tokens)


class MedusaProposer(SpeculativeProposer):
    """Medusa-style multi-head prediction proposer."""

    def __init__(self, vocab_size: int, max_speculation_depth: int = 5, num_heads: int = 4, top_k_per_head: int = 5):
        super().__init__(vocab_size, max_speculation_depth)
        self.num_heads = min(num_heads, max_speculation_depth)
        # Placeholder weights
        self._head_weights = [np.random.randn(vocab_size) * 0.01 for _ in range(self.num_heads)]

    def _sample_from_head(self, head_idx: int, top_k: int = 5) -> List[Tuple[int, float]]:
        """Sample top-k tokens from a specific head."""
        logits = self._head_weights[head_idx]
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)

        top_k_indices = np.argpartition(probs, -top_k)[-top_k:]
        top_k_indices = top_k_indices[np.argsort(probs[top_k_indices])[::-1]]
        return [(int(idx), float(probs[idx])) for idx in top_k_indices]

    def propose(
        self,
        input_ids: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        num_candidates: int = 5
    ) -> SpeculativeTree:
        """Propose speculative tokens using Medusa heads."""
        start = time.perf_counter()
        tree = SpeculativeTree(root_position=len(input_ids))

        # Branching at first level
        for token_id, prob in self._sample_from_head(0, num_candidates):
            current_idx = tree.add_token(token_id, len(input_ids), -1, prob)

            # Greedy prediction for subsequent tokens in path
            for h in range(1, self.num_heads):
                samples = self._sample_from_head(h, top_k=1)
                if not samples:
                    break
                current_idx = tree.add_token(samples[0][0], len(input_ids) + h, current_idx, samples[0][1])

        self.stats.proposals_made += 1
        self.stats.tokens_proposed += len(tree)
        self.stats.proposal_time_ms += (time.perf_counter() - start) * 1000
        return tree

    def update(self, accepted_tokens: List[int], rejected_at: int):
        """Update statistics."""
        self.stats.tokens_accepted += len(accepted_tokens)
