#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Proposer logic for EAGLE speculative decoding.
"""

from __future__ import annotations

import math
import random
import threading
from typing import TYPE_CHECKING

from .base import TreeAttentionMetadata
from .config import EagleConfig, EagleMethod
from .models import DraftModelWrapper, DraftOutput, SimpleDraftModel
from .stats import AcceptanceStats
from .tree import SpeculativeTree

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class EagleProposer:
    """
    EAGLE-style speculative decoding proposer.
    """

    def __init__(self, config: EagleConfig, draft_model: DraftModelWrapper | None = None) -> None:
        self.config = config
        self.draft_model = draft_model or SimpleDraftModel(hidden_size=config.hidden_size)
        self.method = config.method
        self.num_speculative_tokens = config.num_speculative_tokens
        self.max_num_tokens = config.max_num_tokens
        self.hidden_size = config.hidden_size
        self.use_cuda_graph = config.use_cuda_graph
        self.use_tree_attention = config.use_tree_attention

        # Buffers
        self._input_ids_buffer: list[int] = []
        self._positions_buffer: list[int] = []
        self._hidden_states_buffer: list[list[float]] = []

        # Statistics
        self._stats = AcceptanceStats()

        # Tree attention builder
        self._tree_metadata_builder: TreeAttentionMetadata | None = None

        # CUDA graph state
        self._cuda_graph_compiled = False
        self._cuda_graph_batch_sizes: set[int] = set()

    def propose(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None = None,
        max_proposals: int | None = None,
    ) -> list[DraftOutput]:
        """Generate draft token proposals."""
        if max_proposals is None:
            max_proposals = self._get_adaptive_depth()

        max_proposals = min(max_proposals, self.num_speculative_tokens)

        if self.use_tree_attention:
            return self._propose_tree(input_ids, positions, hidden_states, max_proposals)

        return self._propose_sequential(input_ids, positions, hidden_states, max_proposals)

    def _propose_sequential(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None, num_proposals: int
    ) -> list[DraftOutput]:
        """Sequential draft proposal."""
        proposals = []
        current_ids = list(input_ids)
        current_positions = list(positions)
        current_hidden = hidden_states

        for _ in range(num_proposals):
            output = self.draft_model.forward(current_ids[-1:], current_positions[-1:], current_hidden)
            proposals.append(output)

            if output.token_ids:
                current_ids.append(output.token_ids[0])
                current_positions.append(current_positions[-1] + 1)
                if output.hidden_states:
                    current_hidden = output.hidden_states

        return proposals

    def _propose_tree(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None, num_proposals: int
    ) -> list[DraftOutput]:
        """Tree-based draft proposal."""
        tree = SpeculativeTree.create(root_token_id=input_ids[-1] if input_ids else 0, max_depth=num_proposals)

        proposals: list[DraftOutput] = []
        nodes_to_expand = [tree.root]

        for _ in range(num_proposals):
            if not nodes_to_expand:
                break

            output = self._expand_tree_step(nodes_to_expand, positions, hidden_states, tree)
            proposals.append(output)
            
            # Update nodes_to_expand for next step
            nodes_to_expand = [
                child for node in nodes_to_expand for child in node.children
            ]

        return proposals

    def _expand_tree_step(
        self,
        nodes_to_expand: list,
        positions: list[int],
        hidden_states: list[list[float]] | None,
        tree: SpeculativeTree
    ) -> DraftOutput:
        """Helper to expand one level of the speculative tree."""
        batch_ids = [node.token_id for node in nodes_to_expand]
        batch_positions = [positions[-1] + node.depth for node in nodes_to_expand]

        output = self.draft_model.forward(batch_ids, batch_positions, hidden_states)

        for i, node in enumerate(nodes_to_expand):
            if i < len(output.logits):
                logits = output.logits[i]
                top_k = self._get_top_k_candidates(logits, k=4)
                tree.expand(node, top_k)
        
        return output

    def _get_top_k_candidates(self, logits: list[float], k: int = 4) -> list[tuple[int, float]]:
        """Get top-k token candidates."""
        if HAS_RUST and hasattr(rust_core, "eagle_top_k_candidates_rust"):
            return getattr(rust_core, "eagle_top_k_candidates_rust")(logits, k)

        indexed = [(i, float(logits[i])) for i in range(len(logits))]
        sorted_candidates = sorted(indexed, key=lambda x: x[1], reverse=True)[:k]
        return list(sorted_candidates)

    def _get_adaptive_depth(self) -> int:
        """Get adaptive speculation depth."""
        return self._stats.get_optimal_depth(min_rate=0.5)

    def record_acceptance(self, num_proposed: int, num_accepted: int) -> None:
        """Record acceptance statistics."""
        self._stats.record(num_proposed, num_accepted)
        for i in range(num_proposed):
            self._stats.record_position(i, i < num_accepted)

    def get_acceptance_rate(self) -> float:
        """Get current acceptance rate."""
        return self._stats.get_acceptance_rate()

    def build_tree_attention_metadata(self, tree: SpeculativeTree, base_seq_len: int) -> TreeAttentionMetadata:
        """Build attention metadata."""
        paths = tree.get_all_paths()
        num_tokens = sum(len(path) for path in paths)

        tree_mask = [[False] * num_tokens for _ in range(num_tokens)]
        tree_positions: list[int] = []
        parent_indices: list[int] = []

        token_idx = 0
        for path in paths:
            token_idx = self._fill_path_metadata(
                path, base_seq_len, token_idx, tree_mask, tree_positions, parent_indices
            )

        return TreeAttentionMetadata(
            query_start_loc=[0],
            seq_lens=[num_tokens],
            block_tables=[],
            max_seq_len=num_tokens,
            tree_mask=tree_mask,
            tree_positions=tree_positions,
            parent_indices=parent_indices,
        )

    def _fill_path_metadata(
        self,
        path: list,
        base_seq_len: int,
        start_token_idx: int,
        tree_mask: list[list[bool]],
        tree_positions: list[int],
        parent_indices: list[int]
    ) -> int:
        """Fill metadata for a single path in the tree."""
        path_len = len(path)
        token_idx = start_token_idx
        for i in range(path_len):
            tree_positions.append(base_seq_len + i)
            parent_indices.append(token_idx - 1 if i > 0 else -1)
            # Optimization: Causal mask within path tokens
            for j in range(i + 1):
                tree_mask[token_idx][start_token_idx + j] = True
            token_idx += 1
        return token_idx

    def verify_and_accept(
        self,
        draft_tokens: list[int],
        draft_logprobs: list[float],
        target_logprobs: list[float],
        sampling_eps: float = 1e-5,
    ) -> tuple[list[int], int]:
        """Verify draft tokens."""
        if HAS_RUST and hasattr(rust_core, "eagle_verify_accept_rust"):
            accepted, _ = getattr(rust_core, "eagle_verify_accept_rust")(
                draft_tokens, draft_logprobs, target_logprobs, sampling_eps
            )
            return accepted, len(accepted)

        accepted = []
        for draft_token, draft_lp, target_lp in zip(draft_tokens, draft_logprobs, target_logprobs):
            ratio = math.exp(min(0.0, target_lp - draft_lp))
            if random.random() < ratio:
                accepted.append(draft_token)
            else:
                break
        return accepted, len(accepted)

    def extrapolate_hidden_states(self, hidden_states: list[list[float]], num_steps: int = 1) -> list[list[float]]:
        """Extrapolate hidden states."""
        if len(hidden_states) < 2:
            return hidden_states

        if HAS_RUST and hasattr(rust_core, "eagle_extrapolate_hidden_rust"):
            return getattr(rust_core, "eagle_extrapolate_hidden_rust")(hidden_states, num_steps)

        last = hidden_states[-1]
        prev = hidden_states[-2]

        extrapolated = []
        for step in range(num_steps):
            factor = step + 1
            new_state = [val_last + (val_last - prev[i]) * factor for i, val_last in enumerate(last)]
            extrapolated.append(new_state)
        return extrapolated

    def prepare_inputs_padded(
        self,
        token_ids: list[list[int]],
        positions: list[list[int]],
        hidden_states: list[list[list[float]]] | None = None,
    ) -> tuple[list[int], list[int], list[list[float]] | None]:
        """Prepare padded inputs."""
        if HAS_RUST and hasattr(rust_core, "eagle_prepare_inputs_padded_rust"):
            return getattr(rust_core, "eagle_prepare_inputs_padded_rust")(token_ids, positions, hidden_states)

        max_len = max(len(ids) for ids in token_ids)
        padded_ids = []
        for ids in token_ids:
            padded = ids + [0] * (max_len - len(ids))
            padded_ids.extend(padded)

        padded_positions = []
        for pos in positions:
            padded = pos + [0] * (max_len - len(pos))
            padded_positions.extend(padded)

        padded_hidden = None
        if hidden_states is not None:
            hidden_size = len(hidden_states[0][0]) if hidden_states and hidden_states[0] else 4096
            padded_hidden = []
            for states in hidden_states:
                padded = states + [[0.0] * hidden_size] * (max_len - len(states))
                padded_hidden.extend(padded)
        return padded_ids, padded_positions, padded_hidden


class EagleProposerFactory:
    """Factory for creating EAGLE proposers."""

    @staticmethod
    def create(
        method: EagleMethod = EagleMethod.EAGLE_2,
        num_speculative_tokens: int = 5,
        hidden_size: int = 4096,
        use_cuda_graph: bool = True,
        **kwargs,
    ) -> EagleProposer:
        """Create EAGLE proposer."""
        config = EagleConfig(
            method=method,
            num_speculative_tokens=num_speculative_tokens,
            hidden_size=hidden_size,
            use_cuda_graph=use_cuda_graph,
            **kwargs,
        )
        return EagleProposer(config)

    @staticmethod
    def create_eagle3(
        num_speculative_tokens: int = 5, hidden_size: int = 4096, use_aux_hidden_state: bool = True, **kwargs
    ) -> EagleProposer:
        """Create EAGLE-3 proposer."""
        config = EagleConfig(
            method=EagleMethod.EAGLE_3,
            num_speculative_tokens=num_speculative_tokens,
            hidden_size=hidden_size,
            eagle3_use_aux_hidden_state=use_aux_hidden_state,
            **kwargs,
        )
        return EagleProposer(config)


class AsyncEagleProposer:
    """Async wrapper for EAGLE proposer."""

    def __init__(self, proposer: EagleProposer) -> None:
        self.proposer = proposer
        self._lock = threading.Lock()

    async def propose_async(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None = None
    ) -> list[DraftOutput]:
        """Async draft proposal."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.proposer.propose(input_ids, positions, hidden_states))

    async def verify_async(
        self, draft_tokens: list[int], draft_logprobs: list[float], target_logprobs: list[float]
    ) -> tuple[list[int], int]:
        """Async verification."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.proposer.verify_and_accept(draft_tokens, draft_logprobs, target_logprobs)
        )
