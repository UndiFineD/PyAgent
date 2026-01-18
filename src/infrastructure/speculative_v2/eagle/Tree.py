# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Speculative tree structures for EAGLE.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True)
class TreeNode:
    """Node in speculative decoding tree."""
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
            confidence=confidence
        )
        self.children.append(child)
        return child
    
    def path_to_root(self) -> list[int]:
        """Get token path from root to this node."""
        path = []
        node: TreeNode | None = self
        while node is not None:
            path.append(node.token_id)
            node = node.parent
        return list(reversed(path))
    
    def all_leaves(self) -> list[TreeNode]:
        """Get all leaf nodes in subtree."""
        if not self.children:
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.all_leaves())
        return leaves


@dataclass(slots=True)
class SpeculativeTree:
    """Tree structure for tree-based speculative decoding."""
    root: TreeNode
    max_depth: int
    num_nodes: int = 1
    accepted_path: list[int] = field(default_factory=list)
    confidence_threshold: float = 0.1  # TALON threshold
    
    @classmethod
    def create(cls, root_token_id: int, max_depth: int, confidence_threshold: float = 0.1) -> SpeculativeTree:
        """Create new speculative tree."""
        root = TreeNode(token_id=root_token_id, depth=0)
        return cls(root=root, max_depth=max_depth, confidence_threshold=confidence_threshold)
    
    def expand(
        self,
        node: TreeNode,
        candidates: list[tuple[int, float, float]],  # (token_id, logprob, confidence)
        max_width: int = 4
    ) -> list[TreeNode]:
        """Expand node with candidate tokens based on confidence.
        
        Matches TALON (arXiv:2601.07353) adaptive construction.
        """
        if node.depth >= self.max_depth:
            return []
        
        # Filter by confidence threshold first
        viable_candidates = [c for c in candidates if c[2] >= self.confidence_threshold]
        
        # Sort by logprob and take top candidates
        sorted_candidates = sorted(viable_candidates, key=lambda x: x[1], reverse=True)
        top_candidates = sorted_candidates[:max_width]
        
        new_nodes = []
        for token_id, logprob, confidence in top_candidates:
            child = node.add_child(token_id, logprob, confidence)
            new_nodes.append(child)
            self.num_nodes += 1
        
        return new_nodes
    
    def get_all_paths(self) -> list[list[int]]:
        """Get all paths from root to leaves."""
        return [leaf.path_to_root() for leaf in self.root.all_leaves()]
    
    def prune(self, accepted_depth: int) -> None:
        """Prune tree to accepted depth."""
        def _prune(node: TreeNode) -> None:
            if node.depth >= accepted_depth:
                node.children = []
            else:
                for child in node.children:
                    _prune(child)
        _prune(self.root)
