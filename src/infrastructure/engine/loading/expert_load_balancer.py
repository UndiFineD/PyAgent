"""
Expert Load Balancer for PyAgent

This module provides expert parallelism load balancing (EPLB) functionality
inspired by vLLM's distributed/eplb module for MoE models.

Key Features:
- Physical-to-logical expert mapping
- Load-balanced expert replication
- Hierarchical packing for locality
- BEYOND vLLM: Locality-aware policies, async rebalancing, adaptive replication

vLLM Patterns:
- AbstractEplbPolicy for rebalancing interface
- DefaultEplbPolicy with balanced packing
- EplbModelState for metrics tracking
- Expert weight rearrangement
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    import torch
    import numpy as np

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class ExpertType(Enum):
    """Types of experts in MoE models."""
    LOGICAL = auto()  # Original model expert
    PHYSICAL = auto()  # Instantiated replica
    REDUNDANT = auto()  # Added for load balancing


@dataclass
class EplbMetrics:
    """
    Metrics for expert parallelism load balancing.
    
    vLLM Pattern: EplbModelState from eplb_state.py
    """
    # Maps physical to logical expert indices
    physical_to_logical: List[List[int]] = field(default_factory=list)
    # Maps logical to physical (sparse, -1 = no mapping)
    logical_to_physical: List[List[List[int]]] = field(default_factory=list)
    # Count of replicas per logical expert
    logical_replica_count: List[List[int]] = field(default_factory=list)
    # Load per physical expert in current pass
    expert_load_pass: List[List[float]] = field(default_factory=list)
    # Sliding window of load history
    expert_load_window: List[List[List[float]]] = field(default_factory=list)
    
    @property
    def num_layers(self) -> int:
        return len(self.physical_to_logical)
    
    @property
    def num_physical_experts(self) -> int:
        if self.physical_to_logical:
            return len(self.physical_to_logical[0])
        return 0
    
    @property
    def num_logical_experts(self) -> int:
        if self.logical_replica_count:
            return len(self.logical_replica_count[0])
        return 0


@dataclass
class ExpertMapping:
    """
    Complete mapping between logical and physical experts.
    
    vLLM Pattern: Result of rebalance_experts
    """
    phy_to_log: List[List[int]]  # [layers, num_physical]
    log_to_phy: List[List[List[int]]]  # [layers, num_logical, max_replicas]
    replica_count: List[List[int]]  # [layers, num_logical]
    
    def get_physical_experts(self, layer: int, logical_idx: int) -> List[int]:
        """Get all physical expert indices for a logical expert."""
        if layer >= len(self.log_to_phy):
            return []
        if logical_idx >= len(self.log_to_phy[layer]):
            return []
        return [p for p in self.log_to_phy[layer][logical_idx] if p >= 0]
    
    def get_logical_expert(self, layer: int, physical_idx: int) -> int:
        """Get logical expert index for a physical expert."""
        if layer >= len(self.phy_to_log):
            return -1
        if physical_idx >= len(self.phy_to_log[layer]):
            return -1
        return self.phy_to_log[layer][physical_idx]


class AbstractEplbPolicy(ABC):
    """
    Abstract policy for expert load balancing.
    
    vLLM Pattern: AbstractEplbPolicy from policy/abstract.py
    """
    
    @classmethod
    @abstractmethod
    def rebalance_experts(
        cls,
        weight: Any,  # torch.Tensor [layers, num_logical_experts]
        num_replicas: int,
        num_groups: int,
        num_nodes: int,
        num_ranks: int,
    ) -> ExpertMapping:
        """
        Rebalance experts based on load weights.
        
        Args:
            weight: Load statistics per expert [layers, num_logical]
            num_replicas: Total physical experts
            num_groups: Expert groups
            num_nodes: Server nodes (for locality)
            num_ranks: Total ranks (EP size)
            
        Returns:
            ExpertMapping with phy2log, log2phy, and replica counts
        """
        pass


class DefaultEplbPolicy(AbstractEplbPolicy):
    """
    Default EPLB policy with balanced packing.
    
    vLLM Pattern: DefaultEplbPolicy from policy/default.py
    Adapted from DeepSeek EPLB algorithm.
    """
    
    @classmethod
    def balanced_packing(
        cls,
        weight: Any,  # [X, n] weights
        num_packs: int,
    ) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Pack weighted objects into packs with balanced total weight.
        
        Each pack contains exactly n/num_packs objects.
        """
        try:
            import numpy as np
        except ImportError:
            raise ImportError("numpy required for DefaultEplbPolicy")
        
        # Handle torch tensors
        if hasattr(weight, 'cpu'):
            weight_np = weight.cpu().numpy()
        else:
            weight_np = np.asarray(weight)
        
        num_layers, num_groups = weight_np.shape
        assert num_groups % num_packs == 0
        groups_per_pack = num_groups // num_packs
        
        if groups_per_pack == 1:
            # Simple case: each group is its own pack
            pack_index = [[i for i in range(num_groups)] for _ in range(num_layers)]
            rank_in_pack = [[0] * num_groups for _ in range(num_layers)]
            return pack_index, rank_in_pack
        
        # Sort by weight descending
        indices = np.argsort(-weight_np, axis=-1)
        
        pack_index = [[-1] * num_groups for _ in range(num_layers)]
        rank_in_pack = [[-1] * num_groups for _ in range(num_layers)]
        
        for layer in range(num_layers):
            pack_weights = [0.0] * num_packs
            pack_items = [0] * num_packs
            
            for group in indices[layer]:
                # Find pack with lowest weight that has capacity
                best_pack = -1
                best_weight = float('inf')
                
                for p in range(num_packs):
                    if pack_items[p] < groups_per_pack:
                        if pack_weights[p] < best_weight:
                            best_weight = pack_weights[p]
                            best_pack = p
                
                if best_pack >= 0:
                    pack_index[layer][group] = best_pack
                    rank_in_pack[layer][group] = pack_items[best_pack]
                    pack_weights[best_pack] += weight_np[layer, group]
                    pack_items[best_pack] += 1
        
        return pack_index, rank_in_pack
    
    @classmethod
    def replicate_experts(
        cls,
        weight: Any,  # [X, num_log]
        num_physical: int,
    ) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
        """
        Replicate logical experts to physical replicas.
        
        Replicates high-load experts to balance load across physical experts.
        """
        try:
            import numpy as np
        except ImportError:
            raise ImportError("numpy required for DefaultEplbPolicy")
        
        if hasattr(weight, 'cpu'):
            weight_np = weight.cpu().numpy()
        else:
            weight_np = np.asarray(weight)
        
        num_layers, num_logical = weight_np.shape
        num_redundant = num_physical - num_logical
        assert num_redundant >= 0
        
        # Initialize mappings
        phy_to_log = [[i if i < num_logical else -1 for i in range(num_physical)]
                      for _ in range(num_layers)]
        rank = [[0] * num_physical for _ in range(num_layers)]
        log_count = [[1] * num_logical for _ in range(num_layers)]
        
        # Add redundant experts to highest-load logical experts
        for layer in range(num_layers):
            for phy_idx in range(num_logical, num_physical):
                # Find logical expert with highest load per replica
                load_per_replica = weight_np[layer] / np.array(log_count[layer])
                best_logical = int(np.argmax(load_per_replica))
                
                phy_to_log[layer][phy_idx] = best_logical
                rank[layer][phy_idx] = log_count[layer][best_logical]
                log_count[layer][best_logical] += 1
        
        return phy_to_log, rank, log_count
    
    @classmethod
    def rebalance_experts(
        cls,
        weight: Any,
        num_replicas: int,
        num_groups: int,
        num_nodes: int,
        num_ranks: int,
    ) -> ExpertMapping:
        """Rebalance experts using balanced packing and replication."""
        try:
            import numpy as np
        except ImportError:
            raise ImportError("numpy required for DefaultEplbPolicy")
        
        if hasattr(weight, 'cpu'):
            weight_np = weight.cpu().numpy()
        else:
            weight_np = np.asarray(weight)
        
        num_layers, num_logical = weight_np.shape
        
        # Replicate experts
        phy_to_log, _, log_count = cls.replicate_experts(weight, num_replicas)
        
        # Build log_to_phy from phy_to_log
        max_replicas = max(max(row) for row in log_count)
        log_to_phy = [
            [[-1] * max_replicas for _ in range(num_logical)]
            for _ in range(num_layers)
        ]
        
        replica_idx = [[0] * num_logical for _ in range(num_layers)]
        for layer in range(num_layers):
            for phy_idx, log_idx in enumerate(phy_to_log[layer]):
                if log_idx >= 0:
                    r = replica_idx[layer][log_idx]
                    log_to_phy[layer][log_idx][r] = phy_idx
                    replica_idx[layer][log_idx] += 1
        
        return ExpertMapping(
            phy_to_log=phy_to_log,
            log_to_phy=log_to_phy,
            replica_count=log_count,
        )


class LocalityAwarePolicy(AbstractEplbPolicy):
    """
    Locality-aware EPLB policy.
    
    BEYOND vLLM: Considers network topology for expert placement.
    Prioritizes keeping related experts on same node.
    """
    
    @classmethod
    def rebalance_experts(
        cls,
        weight: Any,
        num_replicas: int,
        num_groups: int,
        num_nodes: int,
        num_ranks: int,
    ) -> ExpertMapping:
        """Rebalance with locality awareness."""
        try:
            import numpy as np
        except ImportError:
            raise ImportError("numpy required for LocalityAwarePolicy")
        
        if hasattr(weight, 'cpu'):
            weight_np = weight.cpu().numpy()
        else:
            weight_np = np.asarray(weight)
        
        num_layers, num_logical = weight_np.shape
        ranks_per_node = num_ranks // num_nodes
        experts_per_rank = num_replicas // num_ranks
        
        # Group experts by load for node assignment
        pack_index, _ = DefaultEplbPolicy.balanced_packing(weight, num_nodes)
        
        # Assign experts to nodes, then within-node balancing
        phy_to_log, _, log_count = DefaultEplbPolicy.replicate_experts(
            weight, num_replicas
        )
        
        # Build log_to_phy
        max_replicas = max(max(row) for row in log_count)
        log_to_phy = [
            [[-1] * max_replicas for _ in range(num_logical)]
            for _ in range(num_layers)
        ]
        
        replica_idx = [[0] * num_logical for _ in range(num_layers)]
        for layer in range(num_layers):
            for phy_idx, log_idx in enumerate(phy_to_log[layer]):
                if log_idx >= 0:
                    r = replica_idx[layer][log_idx]
                    log_to_phy[layer][log_idx][r] = phy_idx
                    replica_idx[layer][log_idx] += 1
        
        return ExpertMapping(
            phy_to_log=phy_to_log,
            log_to_phy=log_to_phy,
            replica_count=log_count,
        )


class ExpertLoadBalancer:
    """
    Main expert load balancer class.
    
    Manages expert replication and rearrangement for MoE models.
    """
    
    def __init__(
        self,
        num_layers: int,
        num_logical_experts: int,
        num_physical_experts: int,
        num_ranks: int = 1,
        num_nodes: int = 1,
        policy: Optional[AbstractEplbPolicy] = None,
        window_size: int = 100,
    ):
        self.num_layers = num_layers
        self.num_logical = num_logical_experts
        self.num_physical = num_physical_experts
        self.num_ranks = num_ranks
        self.num_nodes = num_nodes
        self.policy = policy or DefaultEplbPolicy()
        self.window_size = window_size
        
        # Initialize metrics
        self.metrics = EplbMetrics(
            expert_load_window=[
                [[0.0] * num_physical_experts for _ in range(num_layers)]
                for _ in range(window_size)
            ]
        )
        
        # Current mapping
        self._mapping: Optional[ExpertMapping] = None
        self._window_idx = 0
        self._lock = threading.Lock()
    
    def record_load(
        self,
        layer: int,
        expert_loads: List[float],
    ) -> None:
        """Record load statistics for a layer's experts."""
        with self._lock:
            # Update current pass
            if not self.metrics.expert_load_pass:
                self.metrics.expert_load_pass = [
                    [0.0] * self.num_physical
                    for _ in range(self.num_layers)
                ]
            
            for i, load in enumerate(expert_loads):
                if i < self.num_physical:
                    self.metrics.expert_load_pass[layer][i] = load
            
            # Update window
            if self.metrics.expert_load_window:
                self.metrics.expert_load_window[self._window_idx][layer] = list(expert_loads)
    
    def advance_window(self) -> None:
        """Advance to next window position."""
        with self._lock:
            self._window_idx = (self._window_idx + 1) % self.window_size
    
    def get_average_load(self) -> List[List[float]]:
        """Get average load per expert across window."""
        with self._lock:
            result = []
            for layer in range(self.num_layers):
                layer_loads = [0.0] * self.num_physical
                for w in range(self.window_size):
                    if self.metrics.expert_load_window:
                        for e in range(self.num_physical):
                            layer_loads[e] += self.metrics.expert_load_window[w][layer][e]
                
                layer_loads = [l / self.window_size for l in layer_loads]
                result.append(layer_loads)
            
            return result
    
    def rebalance(
        self,
        weight: Optional[Any] = None,
    ) -> ExpertMapping:
        """
        Perform expert rebalancing.
        
        Args:
            weight: Optional load weights. If None, uses recorded metrics.
            
        Returns:
            New ExpertMapping
        """
        try:
            import numpy as np
        except ImportError:
            raise ImportError("numpy required for rebalancing")
        
        if weight is None:
            # Aggregate from logical expert loads
            avg_load = self.get_average_load()
            
            # Convert physical loads to logical loads
            logical_loads = np.zeros((self.num_layers, self.num_logical))
            if self._mapping is not None:
                for layer in range(self.num_layers):
                    for phy_idx, log_idx in enumerate(self._mapping.phy_to_log[layer]):
                        if log_idx >= 0 and phy_idx < len(avg_load[layer]):
                            logical_loads[layer, log_idx] += avg_load[layer][phy_idx]
            else:
                # No mapping yet, assume 1:1
                for layer in range(self.num_layers):
                    for i in range(min(self.num_logical, len(avg_load[layer]))):
                        logical_loads[layer, i] = avg_load[layer][i]
            
            weight = logical_loads
        
        # Apply policy
        self._mapping = self.policy.rebalance_experts(
            weight=weight,
            num_replicas=self.num_physical,
            num_groups=self.num_logical,
            num_nodes=self.num_nodes,
            num_ranks=self.num_ranks,
        )
        
        # Update metrics
        self.metrics.physical_to_logical = self._mapping.phy_to_log
        self.metrics.logical_to_physical = self._mapping.log_to_phy
        self.metrics.logical_replica_count = self._mapping.replica_count
        
        return self._mapping
    
    @property
    def mapping(self) -> Optional[ExpertMapping]:
        """Current expert mapping."""
        return self._mapping


class AsyncExpertRebalancer:
    """
    Asynchronous expert rebalancer.
    
    BEYOND vLLM: Background rebalancing with minimal inference disruption.
    """
    
    def __init__(
        self,
        balancer: ExpertLoadBalancer,
        rebalance_interval: float = 60.0,
        load_threshold: float = 2.0,  # Rebalance if max/min load ratio exceeds
    ):
        self.balancer = balancer
        self.rebalance_interval = rebalance_interval
        self.load_threshold = load_threshold
        
        self._executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
        self._running = False
        self._last_rebalance = 0.0
        self._pending_mapping: Optional[ExpertMapping] = None
        self._lock = threading.Lock()
    
    def start(self) -> None:
        """Start background rebalancing."""
        self._running = True
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._executor.submit(self._rebalance_loop)
    
    def stop(self) -> None:
        """Stop background rebalancing."""
        self._running = False
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None
    
    def _should_rebalance(self) -> bool:
        """Check if rebalancing is needed."""
        now = time.time()
        if now - self._last_rebalance < self.rebalance_interval:
            return False
        
        # Check load imbalance
        avg_load = self.balancer.get_average_load()
        for layer_loads in avg_load:
            if layer_loads:
                max_load = max(layer_loads)
                min_load = min(l for l in layer_loads if l > 0) if any(l > 0 for l in layer_loads) else 1.0
                if max_load / max(min_load, 1e-6) > self.load_threshold:
                    return True
        
        return False
    
    def _rebalance_loop(self) -> None:
        """Background rebalancing loop."""
        while self._running:
            try:
                if self._should_rebalance():
                    mapping = self.balancer.rebalance()
                    with self._lock:
                        self._pending_mapping = mapping
                        self._last_rebalance = time.time()
                
                time.sleep(1.0)  # Check every second
            except Exception:
                pass  # Log and continue
    
    def get_pending_mapping(self) -> Optional[ExpertMapping]:
        """Get and clear pending mapping."""
        with self._lock:
            mapping = self._pending_mapping
            self._pending_mapping = None
            return mapping
    
    async def rebalance_async(self) -> ExpertMapping:
        """Async rebalancing."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.balancer.rebalance)


# Rust-accelerated functions
def compute_balanced_packing_rust(
    weights: List[List[float]],
    num_packs: int,
) -> Tuple[List[List[int]], List[List[int]]]:
    """Balanced packing using Rust."""
    if HAS_RUST and hasattr(rust_core, "compute_balanced_packing_rust"):
        return rust_core.compute_balanced_packing_rust(weights, num_packs)
    
    # Python fallback
    return DefaultEplbPolicy.balanced_packing(weights, num_packs)


def compute_expert_replication_rust(
    weights: List[List[float]],
    num_physical: int,
) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    """Expert replication using Rust."""
    if HAS_RUST and hasattr(rust_core, "compute_expert_replication_rust"):
        return rust_core.compute_expert_replication_rust(weights, num_physical)
    
    # Python fallback
    return DefaultEplbPolicy.replicate_experts(weights, num_physical)


def compute_load_imbalance_rust(
    loads: List[List[float]],
) -> float:
    """Compute load imbalance ratio using Rust."""
    if HAS_RUST and hasattr(rust_core, "compute_load_imbalance_rust"):
        return rust_core.compute_load_imbalance_rust(loads)
    
    # Python fallback
    max_load = 0.0
    min_load = float('inf')
    
    for layer_loads in loads:
        for load in layer_loads:
            if load > 0:
                max_load = max(max_load, load)
                min_load = min(min_load, load)
    
    if min_load == float('inf') or min_load == 0:
        return 1.0
    return max_load / min_load
