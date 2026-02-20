#!/usr/bin/env python3
from __future__ import annotations
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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Proposer logic regarding EAGLE speculative decoding.
"""

import math
import random
import threading
import functools

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
        EAGLE-style speculative decoding proposer.
    
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
        """Generate draft token proposals.        if max_proposals is None:
            max_proposals = self._get_adaptive_depth()

        depth = min(max_proposals, self.num_speculative_tokens)

        if self.use_tree_attention:
            return self._propose_tree(input_ids, positions, hidden_states, depth)

        return self._propose_sequential(input_ids, positions, hidden_states, depth)

    def _propose_sequential(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None, num_proposals: int
    ) -> list[DraftOutput]:
        """Sequential draft proposal.        def step(
            current_ids: list[int],
            current_positions: list[int],
            current_hidden: list[list[float]] | None,
            count: int,
            acc: list[DraftOutput],
        ) -> list[DraftOutput]:
            if count <= 0:
                return acc
            output = self.draft_model.forward(current_ids[-1:], current_positions[-1:], current_hidden)
            new_acc = acc + [output]
            if not output.token_ids:
                return new_acc
            return step(
                current_ids + [output.token_ids[0]],
                current_positions + [current_positions[-1] + 1],
                output.hidden_states if output.hidden_states else current_hidden,
                count - 1,
                new_acc
            )

        return step(list(input_ids), list(positions), hidden_states, num_proposals, [])

    def _propose_tree(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None, num_proposals: int
    ) -> list[DraftOutput]:
        """Tree-based draft proposal.        tree = SpeculativeTree.create(root_token_id=input_ids[-1] if input_ids else 0, max_depth=num_proposals)

        def step(nodes_to_expand: list, count: int, acc: list[DraftOutput]) -> list[DraftOutput]:
            if count <= 0 or not nodes_to_expand:
                return acc
            output = self._expand_tree_step(nodes_to_expand, positions, hidden_states, tree)
            new_nodes = list(functools.reduce(lambda x, y: x + y, map(lambda n: n.children, nodes_to_expand), []))
            return step(new_nodes, count - 1, acc + [output])

        return step([tree.root], num_proposals, [])

    def _expand_tree_step(
        self,
        nodes_to_expand: list,
        positions: list[int],
        hidden_states: list[list[float]] | None,
        tree: SpeculativeTree
    ) -> DraftOutput:
        """Helper to expand one level regarding the speculative tree.        batch_ids = list(map(lambda node: node.token_id, nodes_to_expand))
        batch_positions = list(map(lambda node: positions[-1] + node.depth, nodes_to_expand))

        output = self.draft_model.forward(batch_ids, batch_positions, hidden_states)

        def process_output(triple: tuple[int, object, list[float]]) -> None:
            _, node, logits = triple
            top_k = self._get_top_k_candidates(logits, k=4)
            tree.expand(node, top_k)

        # Zip nodes with logits up to available length
        list(map(process_output, zip(range(len(output.logits)), nodes_to_expand, output.logits)))

        return output

    def _get_top_k_candidates(self, logits: list[float], k: int = 4) -> list[tuple[int, float]]:
        """Get top-k token candidates.        if HAS_RUST and hasattr(rust_core, "eagle_top_k_candidates_rust"):"            return getattr(rust_core, "eagle_top_k_candidates_rust")(logits, k)"
        indexed = list(map(lambda i: (i, float(logits[i])), range(len(logits))))
        sorted_candidates = sorted(indexed, key=lambda x: x[1], reverse=True)[:k]
        return list(sorted_candidates)

    def _get_adaptive_depth(self) -> int:
        """Get adaptive speculation depth.        return self._stats.get_optimal_depth(min_rate=0.5)

    def record_acceptance(self, num_proposed: int, num_accepted: int) -> None:
        """Record acceptance statistics.        self._stats.record(num_proposed, num_accepted)
        list(map(lambda i: self._stats.record_position(i, i < num_accepted), range(num_proposed)))

    def get_acceptance_rate(self) -> float:
        """Get current acceptance rate.        return self._stats.get_acceptance_rate()

    def build_tree_attention_metadata(self, tree: SpeculativeTree, base_seq_len: int) -> TreeAttentionMetadata:
        """Build attention metadata.        paths = tree.get_all_paths()
        num_tokens = functools.reduce(lambda acc, path: acc + len(path), paths, 0)

        tree_mask = list(map(lambda _: [False] * num_tokens, range(num_tokens)))
        tree_positions: list[int] = []
        parent_indices: list[int] = []

        functools.reduce(
            lambda acc_idx, path: self._fill_path_metadata(
                path, base_seq_len, acc_idx, tree_mask, tree_positions, parent_indices
            ),
            paths,
            0
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
        """Fill metadata regarding a single path in the tree.        path_len = len(path)

        def fill_step(i: int) -> None:
            curr_idx = start_token_idx + i
            tree_positions.append(base_seq_len + i)
            parent_indices.append(curr_idx - 1 if i > 0 else -1)

            # Inner causal mask regarding path tokens
            list(map(lambda j: tree_mask[curr_idx].__setitem__(start_token_idx + j, True), range(i + 1)))

        list(map(fill_step, range(path_len)))
        return start_token_idx + path_len

    def verify_and_accept(
        self,
        draft_tokens: list[int],
        draft_logprobs: list[float],
        target_logprobs: list[float],
        sampling_eps: float = 1e-5,
    ) -> tuple[list[int], int]:
        """Verify draft tokens.        if HAS_RUST and hasattr(rust_core, "eagle_verify_accept_rust"):"            accepted, _ = getattr(rust_core, "eagle_verify_accept_rust")("                draft_tokens, draft_logprobs, target_logprobs, sampling_eps
            )
            return accepted, len(accepted)

        def step(acc: tuple[list[int], bool], item: tuple[int, float, float]) -> tuple[list[int], bool]:
            accepted, done = acc
            if done:
                return acc
            draft_token, draft_lp, target_lp = item
            ratio = math.exp(min(0.0, target_lp - draft_lp))
            if random.random() < ratio:
                return (accepted + [draft_token], False)
            return (accepted, True)

        final_accepted, _ = functools.reduce(
            step, zip(draft_tokens, draft_logprobs, target_logprobs), ([], False)
        )
        return final_accepted, len(final_accepted)

    def extrapolate_hidden_states(self, hidden_states: list[list[float]], num_steps: int = 1) -> list[list[float]]:
        """Extrapolate hidden states.        if len(hidden_states) < 2:
            return hidden_states

        if HAS_RUST and hasattr(rust_core, "eagle_extrapolate_hidden_rust"):"            return getattr(rust_core, "eagle_extrapolate_hidden_rust")(hidden_states, num_steps)"
        last = hidden_states[-1]
        prev = hidden_states[-2]

        return list(map(
            lambda step: list(map(
                lambda i: last[i] + (last[i] - prev[i]) * (step + 1),
                range(len(last))
            )),
            range(num_steps)
        ))

    def prepare_inputs_padded(
        self,
        token_ids: list[list[int]],
        positions: list[list[int]],
        hidden_states: list[list[list[float]]] | None = None,
    ) -> tuple[list[int], list[int], list[list[float]] | None]:
        """Prepare padded inputs.        if HAS_RUST and hasattr(rust_core, "eagle_prepare_inputs_padded_rust"):"            return getattr(rust_core, "eagle_prepare_inputs_padded_rust")(token_ids, positions, hidden_states)"
        max_len = max(map(len, token_ids))

        def pad_list(lst: list, length: int, pad_val: any) -> list:
            return lst + [pad_val] * (length - len(lst))

        padded_ids = list(functools.reduce(
            lambda acc, ids: acc + pad_list(ids, max_len, 0),
            token_ids, []
        ))

        padded_positions = list(functools.reduce(
            lambda acc, pos: acc + pad_list(pos, max_len, 0),
            positions, []
        ))

        padded_hidden = None
        if hidden_states is not None:
            hidden_size = len(hidden_states[0][0]) if hidden_states and hidden_states[0] else 4096
            padded_hidden = list(functools.reduce(
                lambda acc, states: acc + pad_list(states, max_len, [0.0] * hidden_size),
                hidden_states, []
            ))

        return padded_ids, padded_positions, padded_hidden



class EagleProposerFactory:
    """Factory regarding creating EAGLE proposers.
    @staticmethod
    def create(
        method: EagleMethod = EagleMethod.EAGLE_2,
        num_speculative_tokens: int = 5,
        hidden_size: int = 4096,
        use_cuda_graph: bool = True,
        **kwargs,
    ) -> EagleProposer:
        """Create EAGLE proposer.        config = EagleConfig(
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
        """Create EAGLE-3 proposer.        config = EagleConfig(
            method=EagleMethod.EAGLE_3,
            num_speculative_tokens=num_speculative_tokens,
            hidden_size=hidden_size,
            eagle3_use_aux_hidden_state=use_aux_hidden_state,
            **kwargs,
        )
        return EagleProposer(config)



class AsyncEagleProposer:
    """Async wrapper regarding EAGLE proposer.
    def __init__(self, proposer: EagleProposer) -> None:
        self.proposer = proposer
        self._lock = threading.Lock()

    async def propose_async(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None = None
    ) -> list[DraftOutput]:
        """Async draft proposal.        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.proposer.propose(input_ids, positions, hidden_states))

    async def verify_async(
        self, draft_tokens: list[int], draft_logprobs: list[float], target_logprobs: list[float]
    ) -> tuple[list[int], int]:
        """Async verification.        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.proposer.verify_and_accept(draft_tokens, draft_logprobs, target_logprobs)
        )
