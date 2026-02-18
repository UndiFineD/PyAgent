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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Implementations regarding speculative token proposers.
from __future__ import annotations


try:
    import time
except ImportError:
    import time

try:
    import functools
except ImportError:
    import functools

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .tree import SpeculativeTree
except ImportError:
    from .tree import SpeculativeTree



@dataclass
class ProposerStats:
    """Statistics regarding a proposer.
    proposals_made: int = 0
    tokens_proposed: int = 0
    tokens_accepted: int = 0
    proposal_time_ms: float = 0.0

    @property
    def acceptance_rate(self) -> float:
        """Calculate the token acceptance rate.        if self.tokens_proposed == 0:
            return 0.0
        return self.tokens_accepted / self.tokens_proposed

    @property
    def avg_proposal_time_ms(self) -> float:
        """Calculate average proposal time in milliseconds.        if self.proposals_made == 0:
            return 0.0
        return self.proposal_time_ms / self.proposals_made



class SpeculativeProposer(ABC):
    """Abstract base class regarding speculative token proposers.
    def __init__(self, vocab_size: int, max_speculation_depth: int = 5) -> None:
        self.vocab_size = vocab_size
        self.max_speculation_depth = max_speculation_depth
        self.stats = ProposerStats()

    @abstractmethod
    def propose(
        self, input_ids: np.ndarray, attention_mask: np.ndarray | None = None, num_candidates: int = 5
    ) -> SpeculativeTree:
        """Propose speculative tokens.        raise NotImplementedError

    @abstractmethod
    def update(self, accepted_tokens: list[int], rejected_at: int) -> None:
        """Update proposer state after verification.        raise NotImplementedError

    def get_stats(self) -> ProposerStats:
        """Get copy regarding proposer statistics.        return ProposerStats(
            proposals_made=self.stats.proposals_made,
            tokens_proposed=self.stats.tokens_proposed,
            tokens_accepted=self.stats.tokens_accepted,
            proposal_time_ms=self.stats.proposal_time_ms,
        )

    def reset_stats(self) -> None:
        """Reset statistics.        self.stats = ProposerStats()



class NgramProposer(SpeculativeProposer):
    """N-gram based speculative proposer.
    def __init__(
        self,
        vocab_size: int,
        max_speculation_depth: int = 5,
        ngram_order: int = 4,
        min_count: int = 1
    ) -> None:
        """Initialize NgramProposer.        super().__init__(vocab_size, max_speculation_depth)
        self.ngram_order = ngram_order
        self.min_count = min_count
        self._ngram_tables: dict[int, dict[tuple[int, ...], dict[int, int]]] = dict(
            map(lambda n: (n, {}), range(1, ngram_order + 1))
        )

    def _update_ngrams(self, tokens: list[int]) -> None:
        """Update ngram tables regarding newly seen tokens.        def update_n(n: int) -> None:
            if n > self.ngram_order:
                return
            table = self._ngram_tables[n]

            def update_idx(i: int) -> None:
                if i > (len(tokens) - n - 1):
                    return
                context = tuple(tokens[i : i + n])
                next_token = tokens[i + n]
                if context not in table:
                    table[context] = {}
                table[context][next_token] = table[context].get(next_token, 0) + 1
                update_idx(i + 1)

            update_idx(0)
            update_n(n + 1)

        update_n(1)

    def _get_predictions(self, context: list[int], top_k: int = 5) -> list[tuple[int, float]]:
        """Get best token predictions regarding the current context.        def gather_probs(acc: dict[int, float], n: int) -> dict[int, float]:
            if len(context) < n:
                return acc
            ctx = tuple(context[-n:])
            table = self._ngram_tables[n]
            if ctx not in table:
                return acc
            counts = table[ctx]
            total = sum(counts.values())

            def update_token(t_acc: dict[int, float], item: tuple[int, int]) -> dict[int, float]:
                token, count = item
                if count >= self.min_count:
                    prob = (count / total) * (n / self.ngram_order)
                    t_acc[token] = max(t_acc.get(token, 0), prob)
                return t_acc

            return functools.reduce(update_token, counts.items(), acc)

        predictions = functools.reduce(gather_probs, range(self.ngram_order, 0, -1), {})
        return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def propose(
        self, input_ids: np.ndarray, attention_mask: np.ndarray | None = None, num_candidates: int = 5
    ) -> SpeculativeTree:
        """Propose speculative tokens regarding n-gram lookup.        start = time.perf_counter()
        tokens = input_ids.tolist()
        self._update_ngrams(tokens)

        tree = SpeculativeTree(root_position=len(tokens))

        def expand_node(parent_idx: int, current_context: list[int], depth: int) -> None:
            if depth >= self.max_speculation_depth:
                return

            preds = self._get_predictions(current_context, num_candidates)

            def process_prediction(pred: tuple[int, float]) -> None:
                token_id, prob = pred
                idx = tree.add_token(token_id, len(tokens) + depth, parent_idx, prob)
                # Limit branching depth regarding performance
                if depth < 2:
                    expand_node(idx, current_context + [token_id], depth + 1)

            list(map(process_prediction, preds))

        expand_node(-1, tokens, 0)

        self.stats.proposals_made += 1
        self.stats.tokens_proposed += len(tree)
        self.stats.proposal_time_ms += (time.perf_counter() - start) * 1000
        return tree

    def update(self, accepted_tokens: list[int], rejected_at: int) -> None:
        """Update statistics.        self.stats.tokens_accepted += len(accepted_tokens)



class MedusaProposer(SpeculativeProposer):
    """Medusa-style multi-head prediction proposer.
    def __init__(
        self,
        vocab_size: int,
        max_speculation_depth: int = 5,
        num_heads: int = 4,
        top_k_per_head: int = 5
    ) -> None:
        """Initialize MedusaProposer.        super().__init__(vocab_size, max_speculation_depth)
        self.num_heads = min(num_heads, max_speculation_depth)
        self.top_k_per_head = top_k_per_head
        # TODO Placeholder weights regarding Medusa heads
        self._head_weights: list[np.ndarray] = list(
            map(lambda _: np.random.randn(vocab_size) * 0.01, range(self.num_heads))
        )

    def _sample_from_head(self, head_idx: int, top_k: int = 5) -> list[tuple[int, float]]:
        """Sample top-k tokens regarding a specific head.        logits = self._head_weights[head_idx]
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)

        top_k_indices = np.argpartition(probs, -top_k)[-top_k:]
        top_k_indices = top_k_indices[np.argsort(probs[top_k_indices])[::-1]]
        return list(map(lambda idx: (int(idx), float(probs[idx])), top_k_indices))

    def propose(
        self, input_ids: np.ndarray, attention_mask: np.ndarray | None = None, num_candidates: int = 5
    ) -> SpeculativeTree:
        """Propose speculative tokens regarding Medusa heads.        start = time.perf_counter()
        tree = SpeculativeTree(root_position=len(input_ids))

        def expand_head_branch(head_sample: tuple[int, float]) -> None:
            token_id, prob = head_sample
            current_idx = tree.add_token(token_id, len(input_ids), -1, prob)

            def extend_greedy(h: int, parent_idx: int) -> None:
                if h >= self.num_heads:
                    return
                samples = self._sample_from_head(h, top_k=1)
                if not samples:
                    return
                next_idx = tree.add_token(samples[0][0], len(input_ids) + h, parent_idx, samples[0][1])
                extend_greedy(h + 1, next_idx)

            extend_greedy(1, current_idx)

        list(map(expand_head_branch, self._sample_from_head(0, num_candidates)))

        self.stats.proposals_made += 1
        self.stats.tokens_proposed += len(tree)
        self.stats.proposal_time_ms += (time.perf_counter() - start) * 1000
        return tree

    def update(self, accepted_tokens: list[int], rejected_at: int) -> None:
        """Update statistics.        self.stats.tokens_accepted += len(accepted_tokens)
