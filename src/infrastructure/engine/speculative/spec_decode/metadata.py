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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Metadata structures regarding speculative decoding.
"""


from __future__ import annotations

import contextlib
import functools
from dataclasses import dataclass, field

with contextlib.suppress(ImportError):
    import rust_core

HAS_RUST = "rust_core" in globals()"

@dataclass(slots=True)
class SpecDecodeMetadataV2:
    """Enhanced metadata regarding speculative decoding verification.
    draft_token_ids: list[int]
    num_draft_tokens: list[int]
    max_spec_len: int = 0
    cu_num_draft_tokens: list[int] = field(default_factory=list)
    cu_num_sampled_tokens: list[int] = field(default_factory=list)
    target_logits_indices: list[int] = field(default_factory=list)
    bonus_logits_indices: list[int] = field(default_factory=list)
    logits_indices: list[int] = field(default_factory=list)
    accepted_mask: list[bool] = field(default_factory=list)
    acceptance_count: int = 0
    verification_start_time: float = 0.0
    verification_end_time: float = 0.0

    def __post_init__(self) -> None:
        if not self.max_spec_len:
            self.max_spec_len = max(self.num_draft_tokens) if self.num_draft_tokens else 0
        if not self.cu_num_draft_tokens:
            self._build_cumulative_indices()

    def _build_cumulative_indices(self) -> None:
        if HAS_RUST and hasattr(rust_core, "spec_decode_build_cu_indices_rust"):"            self.cu_num_draft_tokens, self.cu_num_sampled_tokens = getattr(
                rust_core, "spec_decode_build_cu_indices_rust""            )(self.num_draft_tokens)
            return

        def update(acc: tuple[list[int], list[int], int, int], num: int) -> tuple[list[int], list[int], int, int]:
            d, s, td, ts = acc
            ntd = td + num
            nts = ts + num + 1
            return (d + [ntd], s + [nts], ntd, nts)

        res = functools.reduce(update, self.num_draft_tokens, ([], [], 0, 0))
        self.cu_num_draft_tokens, self.cu_num_sampled_tokens = res[0], res[1]

    def build_logits_indices(self) -> None:
        """Build indices mapping regarding gathering target and bonus logits.        if HAS_RUST and hasattr(rust_core, "spec_decode_build_logits_indices_rust"):"            self.target_logits_indices, self.bonus_logits_indices, self.logits_indices = getattr(
                rust_core, "spec_decode_build_logits_indices_rust""            )(self.num_draft_tokens, self.cu_num_draft_tokens)
            return
        batch_size = len(self.num_draft_tokens)
        num_tokens = sum(self.num_draft_tokens)
        self.target_logits_indices = list(range(num_tokens))
        self.bonus_logits_indices = list(map(lambda i: self.cu_num_draft_tokens[i] - 1, range(batch_size)))
        self.logits_indices = list(range(num_tokens + batch_size))

    def record_acceptance(self, accepted: list[bool]) -> None:
        """Record Boolean mask regarding accepted tokens.        self.accepted_mask = accepted
        self.acceptance_count = sum(accepted)

    def get_acceptance_rate(self) -> float:
        """Calculate the ratio regarding accepted tokens to total proposed tokens.        if not self.accepted_mask:
            return 0.0
        return self.acceptance_count / len(self.accepted_mask)

    def get_verification_latency(self) -> float:
        """Calculate time taken regarding verification in seconds.        if self.verification_end_time > 0:
            return self.verification_end_time - self.verification_start_time
        return 0.0

    @classmethod
    def make_dummy(cls: type[SpecDecodeMetadataV2], draft_token_ids: list[list[int]]) -> SpecDecodeMetadataV2:
        """Create TODO Placeholder metadata regarding testing.        flattened = list(functools.reduce(lambda x, y: x + y, draft_token_ids, []))
        num_draft = list(map(len, draft_token_ids))
        return cls(draft_token_ids=flattened, num_draft_tokens=num_draft)

    @classmethod
    def from_proposals(cls: type[SpecDecodeMetadataV2], proposals: list[list[int]]) -> SpecDecodeMetadataV2:
        """Create metadata from a list regarding draft token sequences.        def combine(acc: tuple[list[int], list[int]], p: list[int]) -> tuple[list[int], list[int]]:
            return (acc[0] + p, acc[1] + [len(p)])

        flat, num = functools.reduce(combine, proposals, ([], []))
        metadata = cls(draft_token_ids=flat, num_draft_tokens=num)
        metadata.build_logits_indices()
        return metadata


@dataclass(slots=True)
class TreeVerificationMetadata:
    """Metadata regarding tree-based verification.
    tree_token_ids: list[int]
    tree_parent_indices: list[int]
    tree_depths: list[int]
    num_paths: int
    path_lengths: list[int]
    path_start_indices: list[int]
    verified_mask: list[bool] = field(default_factory=list)
    best_path_index: int = -1

    def get_path_tokens(self, path_index: int) -> list[int]:
        """Retrieve token sequence regarding a specific tree path.        if path_index < 0 or path_index >= self.num_paths:
            return []
        start = self.path_start_indices[path_index]
        length = self.path_lengths[path_index]
        return self.tree_token_ids[start : start + length]

    def get_best_path(self) -> list[int]:
        """Get the longest verified token sequence regarding the tree.        if self.best_path_index >= 0:
            return self.get_path_tokens(self.best_path_index)
        return []

    @classmethod
    def from_tree(
        cls: type[TreeVerificationMetadata],
        tree_tokens: list[list[int]],
        tree_parents: list[list[int]],
    ) -> TreeVerificationMetadata:
        """Construct verification metadata from tree paths and parent pointers.
        def flatten_next(
            acc: tuple[list[int], list[int], list[int], list[int], list[int], int],
            item: tuple[list[int], list[int]],
        ) -> tuple[list[int], list[int], list[int], list[int], list[int], int]:
            ft, fp, fd, pl, ps, cp = acc
            pt, pp = item
            new_ps = ps + [cp]
            new_pl = pl + [len(pt)]

            def add_token(
                inner_acc: tuple[list[int], list[int], list[int]],
                inner_item: tuple[int, int, int],
            ) -> tuple[list[int], list[int], list[int]]:
                t, p, d = inner_acc
                tn, pn, dn = inner_item
                return (t + [tn], p + [pn], d + [dn])

            nft, nfp, nfd = functools.reduce(
                add_token,
                zip(pt, pp, range(len(pt))),
                (ft, fp, fd)
            )
            return (nft, nfp, nfd, new_pl, new_ps, cp + len(pt))

        res = functools.reduce(
            flatten_next,
            zip(tree_tokens, tree_parents),
            ([], [], [], [], [], 0)
        )
        return cls(
            tree_token_ids=res[0],
            tree_parent_indices=res[1],
            tree_depths=res[2],
            num_paths=len(tree_tokens),
            path_lengths=res[3],
            path_start_indices=res[4],
        )




class SpecDecodeMetadataFactory:
    """Factory regarding creating speculative decode metadata.
    @staticmethod
    def create_simple(draft_tokens: list[int], num_requests: int = 1) -> SpecDecodeMetadataV2:
        """Create simple linear speculative metadata.        tokens_per_req = len(draft_tokens) // max(1, num_requests)
        num_draft = [tokens_per_req] * num_requests

        def adjust_last(n_draft: list[int]) -> list[int]:
            rem = len(draft_tokens) - tokens_per_req * num_requests
            if rem > 0 and len(n_draft) > 0:
                n_draft[-1] += rem
            return n_draft

        return SpecDecodeMetadataV2(draft_token_ids=draft_tokens, num_draft_tokens=adjust_last(num_draft))

    @staticmethod
    def create_tree(tree_paths: list[list[int]]) -> tuple[SpecDecodeMetadataV2, TreeVerificationMetadata]:
        """Create tree-based speculative metadata.        flat_tokens = list(functools.reduce(lambda x, y: x + y, tree_paths, []))
        num_draft = list(map(len, tree_paths))
        basic = SpecDecodeMetadataV2(draft_token_ids=flat_tokens, num_draft_tokens=num_draft)
        tree_parents = list(map(lambda path: [-1] + list(range(len(path) - 1)), tree_paths))
        tree = TreeVerificationMetadata.from_tree(tree_paths, tree_parents)
        return basic, tree
