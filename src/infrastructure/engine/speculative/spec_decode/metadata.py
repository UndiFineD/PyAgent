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
Metadata structures for speculative decoding.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field

with contextlib.suppress(ImportError):
    import rust_core

HAS_RUST = "rust_core" in globals()


@dataclass(slots=True)
class SpecDecodeMetadataV2:
    """Enhanced metadata for speculative decoding verification."""

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

    def __post_init__(self):
        if not self.max_spec_len:
            self.max_spec_len = max(self.num_draft_tokens) if self.num_draft_tokens else 0
        if not self.cu_num_draft_tokens:
            self._build_cumulative_indices()

    def _build_cumulative_indices(self) -> None:
        if HAS_RUST and hasattr(rust_core, "spec_decode_build_cu_indices_rust"):
            self.cu_num_draft_tokens, self.cu_num_sampled_tokens = getattr(
                rust_core, "spec_decode_build_cu_indices_rust"
            )(self.num_draft_tokens)
            return
        cu_draft = []
        cu_sampled = []
        total_draft = 0
        total_sampled = 0
        for num_draft in self.num_draft_tokens:
            total_draft += num_draft
            total_sampled += num_draft + 1
            cu_draft.append(total_draft)
            cu_sampled.append(total_sampled)
        self.cu_num_draft_tokens = cu_draft
        self.cu_num_sampled_tokens = cu_sampled

    def build_logits_indices(self) -> None:
        if HAS_RUST and hasattr(rust_core, "spec_decode_build_logits_indices_rust"):
            self.target_logits_indices, self.bonus_logits_indices, self.logits_indices = getattr(
                rust_core, "spec_decode_build_logits_indices_rust"
            )(self.num_draft_tokens, self.cu_num_draft_tokens)
            return
        batch_size = len(self.num_draft_tokens)
        num_tokens = sum(self.num_draft_tokens)
        self.target_logits_indices = list(range(num_tokens))
        self.bonus_logits_indices = [self.cu_num_draft_tokens[i] - 1 for i in range(batch_size)]
        self.logits_indices = list(range(num_tokens + batch_size))

    def record_acceptance(self, accepted: list[bool]) -> None:
        self.accepted_mask = accepted
        self.acceptance_count = sum(accepted)

    def get_acceptance_rate(self) -> float:
        if not self.accepted_mask:
            return 0.0
        return self.acceptance_count / len(self.accepted_mask)

    def get_verification_latency(self) -> float:
        if self.verification_end_time > 0:
            return self.verification_end_time - self.verification_start_time
        return 0.0

    @classmethod
    def make_dummy(cls, draft_token_ids: list[list[int]]) -> SpecDecodeMetadataV2:
        flattened = [t for tokens in draft_token_ids for t in tokens]
        num_draft = [len(tokens) for tokens in draft_token_ids]
        return cls(draft_token_ids=flattened, num_draft_tokens=num_draft)

    @classmethod
    def from_proposals(cls, proposals: list[list[int]]) -> SpecDecodeMetadataV2:
        flattened = []
        num_draft = []
        for proposal in proposals:
            flattened.extend(proposal)
            num_draft.append(len(proposal))
        metadata = cls(draft_token_ids=flattened, num_draft_tokens=num_draft)
        metadata.build_logits_indices()
        return metadata


@dataclass(slots=True)
class TreeVerificationMetadata:
    """Metadata for tree-based verification."""

    tree_token_ids: list[int]
    tree_parent_indices: list[int]
    tree_depths: list[int]
    num_paths: int
    path_lengths: list[int]
    path_start_indices: list[int]
    verified_mask: list[bool] = field(default_factory=list)
    best_path_index: int = -1

    def get_path_tokens(self, path_index: int) -> list[int]:
        if path_index < 0 or path_index >= self.num_paths:
            return []
        start = self.path_start_indices[path_index]
        length = self.path_lengths[path_index]
        return self.tree_token_ids[start : start + length]

    def get_best_path(self) -> list[int]:
        if self.best_path_index >= 0:
            return self.get_path_tokens(self.best_path_index)
        return []

    @classmethod
    def from_tree(cls, tree_tokens: list[list[int]], tree_parents: list[list[int]]) -> TreeVerificationMetadata:
        flat_tokens, flat_parents, flat_depths = [], [], []
        path_lengths, path_starts = [], []
        current_pos = 0
        for path_tokens, path_parents in zip(tree_tokens, tree_parents):
            path_starts.append(current_pos)
            path_lengths.append(len(path_tokens))
            for i, (token, parent) in enumerate(zip(path_tokens, path_parents)):
                flat_tokens.append(token)
                flat_parents.append(parent)
                flat_depths.append(i)
            current_pos += len(path_tokens)
        return cls(
            tree_token_ids=flat_tokens,
            tree_parent_indices=flat_parents,
            tree_depths=flat_depths,
            num_paths=len(tree_tokens),
            path_lengths=path_lengths,
            path_start_indices=path_starts,
        )


class SpecDecodeMetadataFactory:
    """Factory for creating speculative decode metadata."""

    @staticmethod
    def create_simple(draft_tokens: list[int], num_requests: int = 1) -> SpecDecodeMetadataV2:
        tokens_per_request = len(draft_tokens) // max(1, num_requests)
        num_draft = [tokens_per_request] * num_requests
        remaining = len(draft_tokens) - tokens_per_request * num_requests
        if remaining > 0 and num_requests > 0:
            num_draft[-1] += remaining
        return SpecDecodeMetadataV2(draft_token_ids=draft_tokens, num_draft_tokens=num_draft)

    @staticmethod
    def create_tree(tree_paths: list[list[int]]) -> tuple[SpecDecodeMetadataV2, TreeVerificationMetadata]:
        flat_tokens = [t for path in tree_paths for t in path]
        num_draft = [len(path) for path in tree_paths]
        basic = SpecDecodeMetadataV2(draft_token_ids=flat_tokens, num_draft_tokens=num_draft)
        tree_parents = [[-1] + list(range(len(path) - 1)) for path in tree_paths]
        tree = TreeVerificationMetadata.from_tree(tree_paths, tree_parents)
        return basic, tree
