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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Tree structure for speculative tokens."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class SpeculativeToken:
    """A single speculative token with metadata."""

    token_id: int
    position: int
    parent_idx: int  # Index of parent in tree
    probability: float = 0.0
    depth: int = 0


@dataclass
class SpeculativeTree:
    """
    Tree structure for speculative tokens.

    Represents a tree of candidate tokens where each node
    can have multiple children (branching speculation).
    """

    tokens: List[SpeculativeToken] = field(default_factory=list)
    root_position: int = 0
    max_depth: int = 0

    def add_token(
        self,
        token_id: int,
        position: int,
        parent_idx: int,
        probability: float = 0.0,
    ) -> int:
        """Add a token to the tree, return its index."""
        depth = 0
        if parent_idx >= 0 and parent_idx < len(self.tokens):
            depth = self.tokens[parent_idx].depth + 1

        self.max_depth = max(self.max_depth, depth)

        token = SpeculativeToken(
            token_id=token_id,
            position=position,
            parent_idx=parent_idx,
            probability=probability,
            depth=depth,
        )
        self.tokens.append(token)
        return len(self.tokens) - 1

    def get_path_to_root(self, idx: int) -> List[int]:
        """Get path from token to root (reversed)."""
        path = []
        while idx >= 0 and idx < len(self.tokens):
            path.append(self.tokens[idx].token_id)
            idx = self.tokens[idx].parent_idx
        return path[::-1]

    def get_children(self, idx: int) -> List[int]:
        """Get indices of children for a node."""
        return [i for i, t in enumerate(self.tokens) if t.parent_idx == idx]

    def get_leaves(self) -> List[int]:
        """Get indices of leaf nodes."""
        children_of = set(t.parent_idx for t in self.tokens)
        return [i for i in range(len(self.tokens)) if i not in children_of]

    def to_sequences(self) -> List[List[int]]:
        """Convert tree to list of token sequences (root to each leaf)."""
        sequences = []
        for leaf_idx in self.get_leaves():
            sequences.append(self.get_path_to_root(leaf_idx))
        return sequences

    def __len__(self) -> int:
        return len(self.tokens)
