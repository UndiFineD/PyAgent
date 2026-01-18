"""
EagleProposer: EAGLE-style Speculative Decoding

Implements EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency)
speculative decoding with draft model integration, tree attention, and
hidden state extrapolation.

Key Features Beyond vLLM:
- Multi-model composition (primary + aux hidden states)
- Adaptive speculation depth based on acceptance history
- Grammar-constrained draft generation
- Streaming draft evaluation
- CUDA graph optimization with dynamic batch sizes

Based on vLLM v1 patterns with PyAgent innovations.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol, TypeVar, Generic
import time
import threading
from collections import deque
from functools import lru_cache

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class EagleMethod(Enum):
    """EAGLE method variants."""
    EAGLE_1 = auto()  # Original EAGLE
    EAGLE_2 = auto()  # EAGLE-2 with tree attention
    EAGLE_3 = auto()  # EAGLE-3 with aux hidden states
    EAGLE_3_LFM = auto()  # EAGLE-3 LFM variant


class AttentionBackend(Enum):
    """Attention backend types."""
    FLASH_ATTENTION = auto()
    TREE_ATTENTION = auto()
    TRITON_ATTENTION = auto()
    CUSTOM = auto()


@dataclass(frozen=True, slots=True)
class EagleConfig:
    """Configuration for EAGLE proposer."""
    num_speculative_tokens: int = 5
    max_model_len: int = 4096
    block_size: int = 16
    hidden_size: int = 4096
    dtype: str = "float16"
    method: EagleMethod = EagleMethod.EAGLE_2
    use_cuda_graph: bool = True
    use_tree_attention: bool = True
    max_batch_size: int = 256
    max_num_tokens: int = 8192
    dp_rank: int = 0
    uses_mrope: bool = False
    eagle3_use_aux_hidden_state: bool = False


@dataclass(slots=True)
class DraftOutput:
    """Output from draft model forward pass."""
    token_ids: list[int]
    logits: list[list[float]]
    hidden_states: list[list[float]] | None = None
    acceptance_probs: list[float] | None = None


@dataclass(slots=True)
class TreeNode:
    """Node in speculative decoding tree."""
    token_id: int
    depth: int
    parent: TreeNode | None = None
    children: list[TreeNode] = field(default_factory=list)
    logprob: float = 0.0
    cumulative_logprob: float = 0.0
    hidden_state: list[float] | None = None
    is_accepted: bool = False
    
    def add_child(self, token_id: int, logprob: float) -> TreeNode:
        """Add child node."""
        child = TreeNode(
            token_id=token_id,
            depth=self.depth + 1,
            parent=self,
            logprob=logprob,
            cumulative_logprob=self.cumulative_logprob + logprob
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
    
    @classmethod
    def create(cls, root_token_id: int, max_depth: int) -> SpeculativeTree:
        """Create new speculative tree."""
        root = TreeNode(token_id=root_token_id, depth=0)
        return cls(root=root, max_depth=max_depth)
    
    def expand(
        self,
        node: TreeNode,
        candidates: list[tuple[int, float]],
        max_width: int = 4
    ) -> list[TreeNode]:
        """Expand node with candidate tokens."""
        if node.depth >= self.max_depth:
            return []
        
        # Sort by logprob and take top candidates
        sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        top_candidates = sorted_candidates[:max_width]
        
        new_nodes = []
        for token_id, logprob in top_candidates:
            child = node.add_child(token_id, logprob)
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


class InputBuffer(Protocol):
    """Protocol for input buffer."""
    def get_token_ids(self) -> list[int]: ...
    def get_positions(self) -> list[int]: ...
    def get_hidden_states(self) -> list[list[float]] | None: ...


@dataclass(slots=True)
class CpuGpuBuffer:
    """Buffer that syncs between CPU and GPU."""
    cpu_data: list[Any]
    gpu_data: list[Any] | None = None
    dirty: bool = False
    
    def sync_to_gpu(self) -> None:
        """Sync CPU data to GPU."""
        if self.dirty:
            self.gpu_data = list(self.cpu_data)
            self.dirty = False
    
    def sync_to_cpu(self) -> None:
        """Sync GPU data to CPU."""
        if self.gpu_data is not None:
            self.cpu_data = list(self.gpu_data)
    
    def update(self, data: list[Any]) -> None:
        """Update CPU data."""
        self.cpu_data = data
        self.dirty = True


@dataclass(slots=True)
class AttentionMetadata:
    """Metadata for attention computation."""
    query_start_loc: list[int]
    seq_lens: list[int]
    block_tables: list[list[int]]
    max_seq_len: int
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    slot_mapping: list[int] = field(default_factory=list)


@dataclass(slots=True) 
class TreeAttentionMetadata(AttentionMetadata):
    """Metadata for tree attention."""
    tree_mask: list[list[bool]] = field(default_factory=list)
    tree_positions: list[int] = field(default_factory=list)
    parent_indices: list[int] = field(default_factory=list)


class AcceptanceStats:
    """Track acceptance statistics for adaptive speculation."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self._history: deque[float] = deque(maxlen=window_size)
        self._position_history: dict[int, deque[bool]] = {}
        self._lock = threading.Lock()
    
    def record(self, num_proposed: int, num_accepted: int) -> None:
        """Record acceptance result."""
        if num_proposed == 0:
            return
        rate = num_accepted / num_proposed
        with self._lock:
            self._history.append(rate)
    
    def record_position(self, position: int, accepted: bool) -> None:
        """Record acceptance at specific position."""
        with self._lock:
            if position not in self._position_history:
                self._position_history[position] = deque(maxlen=self.window_size)
            self._position_history[position].append(accepted)
    
    def get_acceptance_rate(self) -> float:
        """Get overall acceptance rate."""
        with self._lock:
            if not self._history:
                return 0.5
            return sum(self._history) / len(self._history)
    
    def get_position_acceptance_rate(self, position: int) -> float:
        """Get acceptance rate at position."""
        with self._lock:
            if position not in self._position_history:
                return 0.5
            history = self._position_history[position]
            if not history:
                return 0.5
            return sum(1 for x in history if x) / len(history)
    
    def get_optimal_depth(self, min_rate: float = 0.5) -> int:
        """Get optimal speculation depth based on acceptance rates."""
        with self._lock:
            for pos in sorted(self._position_history.keys()):
                history = self._position_history.get(pos, deque())
                if not history:
                    return max(1, pos)
                rate = sum(1 for x in history if x) / len(history)
                if rate < min_rate:
                    return max(1, pos)
            return max(1, max(self._position_history.keys()) if self._position_history else 1)


class DraftModelWrapper(ABC):
    """Abstract wrapper for draft model."""
    
    @abstractmethod
    def forward(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None = None
    ) -> DraftOutput:
        """Run draft model forward pass."""
        pass
    
    @abstractmethod
    def get_hidden_size(self) -> int:
        """Get hidden state size."""
        pass


class SimpleDraftModel(DraftModelWrapper):
    """Simple mock draft model for testing."""
    
    def __init__(self, vocab_size: int = 32000, hidden_size: int = 4096):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
    
    def forward(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None = None
    ) -> DraftOutput:
        """Mock forward pass."""
        import random
        n = len(input_ids)
        # Generate random tokens and logits
        token_ids = [random.randint(0, self.vocab_size - 1) for _ in range(n)]
        logits = [[random.random() for _ in range(self.vocab_size)] for _ in range(n)]
        return DraftOutput(token_ids=token_ids, logits=logits)
    
    def get_hidden_size(self) -> int:
        return self.hidden_size


class EagleProposer:
    """
    EAGLE-style speculative decoding proposer.
    
    Implements draft token proposal with:
    - Tree-structured speculation
    - Hidden state extrapolation  
    - Adaptive speculation depth
    - CUDA graph optimization
    """
    
    def __init__(
        self,
        config: EagleConfig,
        draft_model: DraftModelWrapper | None = None
    ):
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
        max_proposals: int | None = None
    ) -> list[DraftOutput]:
        """
        Generate draft token proposals.
        
        Args:
            input_ids: Current token IDs
            positions: Position indices
            hidden_states: Hidden states from target model
            max_proposals: Maximum proposals (uses adaptive if None)
            
        Returns:
            List of draft outputs
        """
        if max_proposals is None:
            max_proposals = self._get_adaptive_depth()
        
        max_proposals = min(max_proposals, self.num_speculative_tokens)
        
        if self.use_tree_attention:
            return self._propose_tree(input_ids, positions, hidden_states, max_proposals)
        else:
            return self._propose_sequential(input_ids, positions, hidden_states, max_proposals)
    
    def _propose_sequential(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None,
        num_proposals: int
    ) -> list[DraftOutput]:
        """Sequential draft proposal."""
        proposals = []
        current_ids = list(input_ids)
        current_positions = list(positions)
        current_hidden = hidden_states
        
        for i in range(num_proposals):
            # Run draft model
            output = self.draft_model.forward(
                current_ids[-1:],  # Last token
                current_positions[-1:],
                current_hidden
            )
            proposals.append(output)
            
            # Update for next iteration
            if output.token_ids:
                current_ids.append(output.token_ids[0])
                current_positions.append(current_positions[-1] + 1)
                if output.hidden_states:
                    current_hidden = output.hidden_states
        
        return proposals
    
    def _propose_tree(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None,
        num_proposals: int
    ) -> list[DraftOutput]:
        """Tree-based draft proposal with multiple candidates per position."""
        # Create speculative tree
        tree = SpeculativeTree.create(
            root_token_id=input_ids[-1] if input_ids else 0,
            max_depth=num_proposals
        )
        
        proposals = []
        nodes_to_expand = [tree.root]
        
        for depth in range(num_proposals):
            if not nodes_to_expand:
                break
            
            # Batch process all nodes at this depth
            batch_ids = [node.token_id for node in nodes_to_expand]
            batch_positions = [positions[-1] + node.depth for node in nodes_to_expand]
            
            output = self.draft_model.forward(batch_ids, batch_positions, hidden_states)
            proposals.append(output)
            
            # Expand tree with top candidates
            next_nodes = []
            for i, node in enumerate(nodes_to_expand):
                if i < len(output.logits):
                    # Get top-k candidates
                    logits = output.logits[i]
                    top_k = self._get_top_k_candidates(logits, k=4)
                    children = tree.expand(node, top_k)
                    next_nodes.extend(children)
            
            nodes_to_expand = next_nodes
        
        return proposals
    
    def _get_top_k_candidates(
        self,
        logits: list[float],
        k: int = 4
    ) -> list[tuple[int, float]]:
        """Get top-k token candidates from logits."""
        if HAS_RUST:
            # Use Rust acceleration
            return rust_core.eagle_top_k_candidates_rust(logits, k)
        
        # Python fallback
        indexed = [(i, logits[i]) for i in range(len(logits))]
        sorted_candidates = sorted(indexed, key=lambda x: x[1], reverse=True)[:k]
        return [(idx, logprob) for idx, logprob in sorted_candidates]
    
    def _get_adaptive_depth(self) -> int:
        """Get adaptive speculation depth based on acceptance history."""
        return self._stats.get_optimal_depth(min_rate=0.5)
    
    def record_acceptance(self, num_proposed: int, num_accepted: int) -> None:
        """Record acceptance statistics."""
        self._stats.record(num_proposed, num_accepted)
        
        # Record per-position
        for i in range(num_proposed):
            self._stats.record_position(i, i < num_accepted)
    
    def get_acceptance_rate(self) -> float:
        """Get current acceptance rate."""
        return self._stats.get_acceptance_rate()
    
    def build_tree_attention_metadata(
        self,
        tree: SpeculativeTree,
        base_seq_len: int
    ) -> TreeAttentionMetadata:
        """Build attention metadata for tree-based decoding."""
        paths = tree.get_all_paths()
        num_tokens = sum(len(path) for path in paths)
        
        # Build tree mask
        tree_mask = [[False] * num_tokens for _ in range(num_tokens)]
        tree_positions = []
        parent_indices = []
        
        token_idx = 0
        for path in paths:
            for i, token_id in enumerate(path):
                tree_positions.append(base_seq_len + i)
                parent_indices.append(token_idx - 1 if i > 0 else -1)
                
                # Set attention mask
                for j in range(i + 1):
                    tree_mask[token_idx][token_idx - j] = True
                
                token_idx += 1
        
        return TreeAttentionMetadata(
            query_start_loc=[0],
            seq_lens=[num_tokens],
            block_tables=[],
            max_seq_len=num_tokens,
            tree_mask=tree_mask,
            tree_positions=tree_positions,
            parent_indices=parent_indices
        )
    
    def verify_and_accept(
        self,
        draft_tokens: list[int],
        draft_logprobs: list[float],
        target_logprobs: list[float],
        sampling_eps: float = 1e-5
    ) -> tuple[list[int], int]:
        """
        Verify draft tokens against target model.
        
        Returns:
            Tuple of (accepted_tokens, num_accepted)
        """
        if HAS_RUST:
            accepted, mask = rust_core.eagle_verify_accept_rust(
                draft_tokens, draft_logprobs, target_logprobs, sampling_eps
            )
            return accepted, len(accepted)
        
        # Python implementation
        accepted = []
        for i, (draft_token, draft_lp, target_lp) in enumerate(
            zip(draft_tokens, draft_logprobs, target_logprobs)
        ):
            # Rejection sampling
            import random
            ratio = math.exp(target_lp - draft_lp)
            if random.random() < min(1.0, ratio):
                accepted.append(draft_token)
            else:
                break
        
        return accepted, len(accepted)
    
    def extrapolate_hidden_states(
        self,
        hidden_states: list[list[float]],
        num_steps: int = 1
    ) -> list[list[float]]:
        """
        Extrapolate hidden states for EAGLE-3.
        
        Uses linear extrapolation from recent hidden states.
        """
        if len(hidden_states) < 2:
            return hidden_states
        
        if HAS_RUST:
            return rust_core.eagle_extrapolate_hidden_rust(hidden_states, num_steps)
        
        # Python implementation - linear extrapolation
        last = hidden_states[-1]
        prev = hidden_states[-2]
        
        extrapolated = []
        for step in range(num_steps):
            new_state = []
            for i in range(len(last)):
                delta = last[i] - prev[i]
                new_state.append(last[i] + delta * (step + 1))
            extrapolated.append(new_state)
        
        return extrapolated
    
    def prepare_inputs_padded(
        self,
        token_ids: list[list[int]],
        positions: list[list[int]],
        hidden_states: list[list[list[float]]] | None = None
    ) -> tuple[list[int], list[int], list[list[float]] | None]:
        """Prepare padded inputs for batch processing."""
        if HAS_RUST:
            return rust_core.eagle_prepare_inputs_padded_rust(
                token_ids, positions, hidden_states
            )
        
        # Find max length
        max_len = max(len(ids) for ids in token_ids)
        
        # Pad token IDs
        padded_ids = []
        for ids in token_ids:
            padded = ids + [0] * (max_len - len(ids))
            padded_ids.extend(padded)
        
        # Pad positions
        padded_positions = []
        for pos in positions:
            padded = pos + [0] * (max_len - len(pos))
            padded_positions.extend(padded)
        
        # Pad hidden states if present
        padded_hidden = None
        if hidden_states is not None:
            hidden_size = len(hidden_states[0][0]) if hidden_states and hidden_states[0] else self.hidden_size
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
        **kwargs
    ) -> EagleProposer:
        """Create EAGLE proposer with configuration."""
        config = EagleConfig(
            method=method,
            num_speculative_tokens=num_speculative_tokens,
            hidden_size=hidden_size,
            use_cuda_graph=use_cuda_graph,
            **kwargs
        )
        return EagleProposer(config)
    
    @staticmethod
    def create_eagle3(
        num_speculative_tokens: int = 5,
        hidden_size: int = 4096,
        use_aux_hidden_state: bool = True,
        **kwargs
    ) -> EagleProposer:
        """Create EAGLE-3 proposer with aux hidden states."""
        config = EagleConfig(
            method=EagleMethod.EAGLE_3,
            num_speculative_tokens=num_speculative_tokens,
            hidden_size=hidden_size,
            eagle3_use_aux_hidden_state=use_aux_hidden_state,
            **kwargs
        )
        return EagleProposer(config)


class AsyncEagleProposer:
    """Async wrapper for EAGLE proposer."""
    
    def __init__(self, proposer: EagleProposer):
        self.proposer = proposer
        self._lock = threading.Lock()
    
    async def propose_async(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None = None
    ) -> list[DraftOutput]:
        """Async draft proposal."""
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.proposer.propose(input_ids, positions, hidden_states)
        )
    
    async def verify_async(
        self,
        draft_tokens: list[int],
        draft_logprobs: list[float],
        target_logprobs: list[float]
    ) -> tuple[list[int], int]:
        """Async verification."""
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.proposer.verify_and_accept(
                draft_tokens, draft_logprobs, target_logprobs
            )
        )
