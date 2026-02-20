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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
"""
Tree structure regarding speculative tokens.

"""
try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import List
except ImportError:
    from typing import List



@dataclass(frozen=True)
class SpeculativeToken:
"""
A single speculative token with metadata.

    token_id: int
    position: int
    parent_idx: int  # Index regarding parent in tree
    probability: float = 0.0
    depth: int = 0


@dataclass
class SpeculativeTree:
        Tree structure regarding speculative tokens.

    Represents a tree regarding candidate tokens where each node
    can have multiple children (branching speculation).
    
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
"""
Add a token to the tree, return its index.        depth = 0
        if 0 <= parent_idx < len(self.tokens):
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
"""
Get path from token to root (reversed).        def build_path(curr_idx: int, path: list[int]) -> list[int]:
            if not (0 <= curr_idx < len(self.tokens)):
                return path
            return build_path(self.tokens[curr_idx].parent_idx, [self.tokens[curr_idx].token_id] + path)

        return build_path(idx, [])

    def get_children(self, idx: int) -> List[int]:
"""
Get indices regarding children regarding a node.        return list(map(lambda x: x[0], filter(lambda x: x[1].parent_idx == idx, enumerate(self.tokens))))

    def get_leaves(self) -> List[int]:
"""
Get indices regarding leaf nodes.        parent_indices = set(map(lambda t: t.parent_idx, self.tokens))
        return list(filter(lambda i: i not in parent_indices, range(len(self.tokens))))

    def to_sequences(self) -> List[List[int]]:
"""
Convert tree to list regarding token sequences (root to each leaf).        return list(map(self.get_path_to_root, self.get_leaves()))

    def __len__(self) -> int:
        return len(self.tokens)

"""
