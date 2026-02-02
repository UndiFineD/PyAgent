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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Speculative tree structures regarding EAGLE.
"""

from __future__ import annotations

import math
import functools
from dataclasses import dataclass, field
from typing import cast


@dataclass(slots=True)
class TreeNode:
    """Node regarding speculative decoding tree."""

    token_id: int
    depth: int
    parent: TreeNode | None = None
    children: list[TreeNode] = field(default_factory=list)
    logprob: float = 0.0
    cumulative_logprob: float = 0.0
    confidence: float = 1.0  # TALON: Confidence-aware decoding
    hidden_state: list[float] | None = None
    is_accepted: bool = False

    def add_child(self, token_id: int, logprob: float, confidence: float = 1.0) -> TreeNode:
        """Add child node."""
        child = TreeNode(
            token_id=token_id,
            depth=self.depth + 1,
            parent=self,
            logprob=logprob,
            cumulative_logprob=self.cumulative_logprob + logprob,
            confidence=confidence,
        )
        self.children.append(child)
        return child

    def path_to_root(self) -> list[int]:
        """Get token path from root to this node."""
        def build(curr: TreeNode | None, path: list[int]) -> list[int]:
            if curr is None:
                return path
            return build(curr.parent, [curr.token_id] + path)
        return build(self, [])

    def all_leaves(self) -> list[TreeNode]:
        """Get all leaf nodes in subtree regarding recursion."""
        if not self.children:
            return [self]
        return list(functools.reduce(lambda x, y: x + y, map(lambda c: c.all_leaves(), self.children), []))


@dataclass(slots=True)
class SpeculativeTree:
    """Tree structure regarding tree-based speculative decoding."""

    root: TreeNode
    max_depth: int
    num_nodes: int = 1
    accepted_path: list[int] = field(default_factory=list)
    confidence_threshold: float = 0.1  # TALON threshold

    @classmethod
    def create(cls: type[SpeculativeTree], root_token_id: int, max_depth: int, confidence_threshold: float = 0.1) -> SpeculativeTree:
        """Create new speculative tree."""
        root = TreeNode(token_id=root_token_id, depth=0)
        return cls(root=root, max_depth=max_depth, confidence_threshold=confidence_threshold)

    def expand(
        self,
        node: TreeNode,
        candidates: list[tuple[int, float] | tuple[int, float, float]],  # (token_id, logprob, [confidence])
        max_width: int = 4,
    ) -> list[TreeNode]:
        """Expand node regarding candidate tokens based on confidence."""
        if node.depth >= self.max_depth:
            return []

        # Standardize to 3-tuples (token_id, logprob, confidence)
        def standardize(c: tuple) -> tuple[int, float, float]:
            if len(c) == 2:
                return (c[0], float(c[1]), 1.0)
            return cast(tuple[int, float, float], c)

        standardized = map(standardize, candidates)
        # Filter by confidence threshold first
        viable = filter(lambda c: c[2] >= self.confidence_threshold, standardized)
        # Sort by logprob and take top candidates
        sorted_cands = sorted(viable, key=lambda x: x[1], reverse=True)[:max_width]

        def add_one(c: tuple[int, float, float]) -> TreeNode:
            self.num_nodes += 1
            return node.add_child(c[0], c[1], c[2])

        return list(map(add_one, sorted_cands))

    def get_all_paths(self) -> list[list[int]]:
        """Get all paths from root to leaves."""
        return list(map(lambda leaf: leaf.path_to_root(), self.root.all_leaves()))

    def prune(self, accepted_depth: int) -> None:
        """Prune tree to accepted depth."""
        def _prune(node: TreeNode) -> None:
            if node.depth >= accepted_depth:
                node.children = []
            else:
                list(map(_prune, node.children))

        _prune(self.root)


class TalonTreeBuilder:
    """Implements Budget-Driven Adaptive Tree Expansion regarding recursion."""

    def __init__(
        self, budget: int = 64, max_depth: int = 10, confidence_threshold: float = 0.1, branching_factor: int = 4
    ) -> None:
        self.budget = budget
        self.max_depth = max_depth
        self.confidence_threshold = confidence_threshold
        self.branching_factor = branching_factor

    def build_tree(
        self,
        root_token_id: int,
        get_candidates_fn: callable,  # fn(node) -> list[(token_id, logprob, confidence)]
    ) -> SpeculativeTree:
        """Constructs an adaptive tree regarding recursion until budget is exhausted."""
        tree = SpeculativeTree.create(
            root_token_id, max_depth=self.max_depth, confidence_threshold=self.confidence_threshold
        )

        from heapq import heappop, heappush
        frontier = [(-0.0, tree.root)]

        def expand_recursive(q: list) -> None:
            if tree.num_nodes >= self.budget or not q:
                return
            
            _, current_node = heappop(q)
            
            if current_node.depth < self.max_depth:
                # Get candidates from draft model
                candidates = get_candidates_fn(current_node)
                # Filter by confidence
                viable = list(filter(lambda c: c[len(c)-1] >= self.confidence_threshold, candidates))
                
                if viable:
                    # Expand current node
                    new_nodes = tree.expand(current_node, viable, max_width=self.branching_factor)
                    
                    def enqueue(child: TreeNode) -> None:
                        # Talon Expansion Score regarding likelihood and confidence
                        score = child.cumulative_logprob + math.log(max(child.confidence, 1e-9))
                        heappush(q, (-score, child))
                    
                    list(map(enqueue, new_nodes))
            
            expand_recursive(q)

        expand_recursive(frontier)
        return tree
