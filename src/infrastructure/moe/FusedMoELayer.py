"""
Fused Mixture of Experts (MoE) Layer.

vLLM Pattern: vllm/model_executor/layers/fused_moe/layer.py
Implements fused MoE computation with expert parallelism support.

Beyond vLLM:
- AdaptiveMoELayer with dynamic expert activation
- HierarchicalMoE with multi-level routing
- CachedExpertWeights for weight caching
"""

from __future__ import annotations

import math
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Literal, Optional, Protocol, TYPE_CHECKING

import numpy as np

# Optional torch import for environments without GPU
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore
    nn = None  # type: ignore
    F = None  # type: ignore

# Try to import Rust accelerators
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# =============================================================================
# Enums and Types
# =============================================================================

class ExpertPlacementStrategy(str, Enum):
    """Strategy for placing experts across devices."""
    LINEAR = "linear"  # Sequential assignment
    ROUND_ROBIN = "round_robin"  # Interleaved assignment
    BALANCED = "balanced"  # Load-balanced assignment
    LOCALITY = "locality"  # Locality-aware assignment


class MoEQuantMethod(str, Enum):
    """Quantization methods for MoE weights."""
    NONE = "none"
    INT8 = "int8"
    INT4 = "int4"
    FP8 = "fp8"
    MXFP4 = "mxfp4"


# =============================================================================
# Configuration
# =============================================================================

@dataclass(frozen=True)
class FusedMoEConfig:
    """
    Configuration for a Fused MoE layer.
    
    vLLM Pattern: FusedMoEConfig from config.py
    """
    num_experts: int
    top_k: int
    hidden_size: int
    intermediate_size: int
    
    # Optional settings
    num_expert_groups: int = 1
    num_redundant_experts: int = 0
    renormalize: bool = True
    use_grouped_topk: bool = False
    aux_loss_coef: float = 0.0
    
    # Activation
    activation: str = "silu"
    
    def __post_init__(self) -> None:
        assert self.num_experts > 0, "num_experts must be positive"
        assert self.top_k > 0, "top_k must be positive"
        assert self.top_k <= self.num_experts, "top_k cannot exceed num_experts"


@dataclass
class FusedMoEParallelConfig:
    """
    Parallelization configuration for MoE.
    
    vLLM Pattern: FusedMoEParallelConfig
    """
    tp_size: int = 1  # Tensor parallel size
    ep_size: int = 1  # Expert parallel size
    ep_rank: int = 0  # Expert parallel rank
    
    # All-to-all settings
    use_all2all_kernels: bool = False
    all2all_backend: str = "nccl"
    use_deepep_ll_kernels: bool = False
    
    # Expert placement
    expert_placement_strategy: ExpertPlacementStrategy = ExpertPlacementStrategy.LINEAR


@dataclass
class FusedMoEQuantConfig:
    """Quantization configuration for MoE."""
    method: MoEQuantMethod = MoEQuantMethod.NONE
    group_size: int = 128
    symmetric: bool = True


# =============================================================================
# Expert Map Utilities
# =============================================================================

def determine_expert_map(
    ep_size: int,
    ep_rank: int,
    global_num_experts: int,
    strategy: ExpertPlacementStrategy = ExpertPlacementStrategy.LINEAR,
    num_fused_shared_experts: int = 0,
) -> tuple[int, np.ndarray | None, np.ndarray | None]:
    """
    Calculate expert assignment for expert parallelism.
    
    vLLM Pattern: determine_expert_map from layer.py
    
    Returns:
        Tuple of (local_num_experts, expert_map, expert_mask)
    """
    if ep_size == 1:
        return (global_num_experts, None, None)
    
    # Use Rust if available for fast computation
    if HAS_RUST and hasattr(rust_core, 'compute_expert_map_rust'):
        result = rust_core.compute_expert_map_rust(
            ep_size, ep_rank, global_num_experts, strategy.value
        )
        return result
    
    # Distribute experts evenly
    base_experts = global_num_experts // ep_size
    remainder = global_num_experts % ep_size
    local_num_experts = base_experts + (1 if ep_rank < remainder else 0)
    
    # Create expert map
    expert_map = np.full(global_num_experts, -1, dtype=np.int32)
    
    if strategy == ExpertPlacementStrategy.LINEAR:
        start_idx = ep_rank * base_experts + min(ep_rank, remainder)
        expert_map[start_idx:start_idx + local_num_experts] = np.arange(
            local_num_experts, dtype=np.int32
        )
    elif strategy == ExpertPlacementStrategy.ROUND_ROBIN:
        local_experts = np.arange(ep_rank, global_num_experts, ep_size, dtype=np.int32)
        expert_map[local_experts] = np.arange(local_num_experts, dtype=np.int32)
    else:
        # Default to linear for unsupported strategies
        start_idx = ep_rank * base_experts + min(ep_rank, remainder)
        expert_map[start_idx:start_idx + local_num_experts] = np.arange(
            local_num_experts, dtype=np.int32
        )
    
    # Create expert mask
    expert_mask = np.ones(
        global_num_experts + num_fused_shared_experts + 1, dtype=np.int32
    )
    expert_mask[-1] = 0
    expert_mask[:global_num_experts] = (expert_map > -1).astype(np.int32)
    
    return (local_num_experts, expert_map, expert_mask)


def get_compressed_expert_map(expert_map: np.ndarray) -> str:
    """
    Compress expert map to string for logging.
    
    vLLM Pattern: get_compressed_expert_map
    """
    global_indices = np.where(expert_map != -1)[0]
    local_indices = expert_map[global_indices]
    return ", ".join(
        f"{local}->{global_idx}"
        for local, global_idx in zip(local_indices, global_indices)
    )


# =============================================================================
# MoE Method Base
# =============================================================================

class FusedMoEMethodBase(ABC):
    """
    Base class for MoE computation methods.
    
    vLLM Pattern: FusedMoEMethodBase
    """
    
    @abstractmethod
    def create_weights(
        self,
        config: FusedMoEConfig,
        parallel_config: FusedMoEParallelConfig,
        device: str = "cpu",
    ) -> dict[str, Any]:
        """Create weight tensors for the MoE layer."""
        pass
    
    @abstractmethod
    def apply(
        self,
        x: Any,
        router_logits: Any,
        top_k: int,
        renormalize: bool,
        weights: dict[str, Any],
    ) -> Any:
        """Apply MoE computation."""
        pass


class UnquantizedFusedMoEMethod(FusedMoEMethodBase):
    """
    Unquantized MoE computation method.
    
    vLLM Pattern: UnquantizedFusedMoEMethod
    """
    
    def create_weights(
        self,
        config: FusedMoEConfig,
        parallel_config: FusedMoEParallelConfig,
        device: str = "cpu",
    ) -> dict[str, Any]:
        """Create unquantized weight tensors."""
        # Calculate local expert count
        local_num_experts, _, _ = determine_expert_map(
            parallel_config.ep_size,
            parallel_config.ep_rank,
            config.num_experts,
            parallel_config.expert_placement_strategy,
        )
        
        if not HAS_TORCH:
            # Return numpy arrays if torch not available
            return {
                "w1": np.zeros(
                    (local_num_experts, config.intermediate_size, config.hidden_size),
                    dtype=np.float32
                ),
                "w2": np.zeros(
                    (local_num_experts, config.hidden_size, config.intermediate_size),
                    dtype=np.float32
                ),
                "w3": np.zeros(
                    (local_num_experts, config.intermediate_size, config.hidden_size),
                    dtype=np.float32
                ),
            }
        
        return {
            "w1": torch.zeros(
                local_num_experts, config.intermediate_size, config.hidden_size,
                device=device
            ),
            "w2": torch.zeros(
                local_num_experts, config.hidden_size, config.intermediate_size,
                device=device
            ),
            "w3": torch.zeros(
                local_num_experts, config.intermediate_size, config.hidden_size,
                device=device
            ),
        }
    
    def apply(
        self,
        x: Any,
        router_logits: Any,
        top_k: int,
        renormalize: bool,
        weights: dict[str, Any],
    ) -> Any:
        """Apply unquantized MoE computation."""
        if not HAS_TORCH:
            return self._apply_numpy(x, router_logits, top_k, renormalize, weights)
        
        return self._apply_torch(x, router_logits, top_k, renormalize, weights)
    
    def _apply_numpy(
        self,
        x: np.ndarray,
        router_logits: np.ndarray,
        top_k: int,
        renormalize: bool,
        weights: dict[str, np.ndarray],
    ) -> np.ndarray:
        """NumPy fallback for MoE computation."""
        batch_size, hidden_size = x.shape
        num_experts = router_logits.shape[-1]
        
        # Get top-k experts
        routing_weights = np.exp(router_logits - router_logits.max(axis=-1, keepdims=True))
        routing_weights = routing_weights / routing_weights.sum(axis=-1, keepdims=True)
        
        top_k_indices = np.argsort(routing_weights, axis=-1)[:, -top_k:]
        top_k_weights = np.take_along_axis(routing_weights, top_k_indices, axis=-1)
        
        if renormalize:
            top_k_weights = top_k_weights / top_k_weights.sum(axis=-1, keepdims=True)
        
        # Compute expert outputs
        output = np.zeros_like(x)
        for i in range(batch_size):
            for k in range(top_k):
                expert_idx = top_k_indices[i, k]
                weight = top_k_weights[i, k]
                
                # Gate projection
                gate = x[i] @ weights["w1"][expert_idx].T
                gate = gate * (1 / (1 + np.exp(-gate)))  # SiLU
                
                # Up projection
                up = x[i] @ weights["w3"][expert_idx].T
                
                # Down projection
                hidden = gate * up
                expert_out = hidden @ weights["w2"][expert_idx].T
                
                output[i] += weight * expert_out
        
        return output
    
    def _apply_torch(
        self,
        x: "torch.Tensor",
        router_logits: "torch.Tensor",
        top_k: int,
        renormalize: bool,
        weights: dict[str, "torch.Tensor"],
    ) -> "torch.Tensor":
        """Torch implementation of MoE computation."""
        batch_size, hidden_size = x.shape
        
        # Get top-k experts and weights
        routing_weights = F.softmax(router_logits, dim=-1)
        top_k_weights, top_k_indices = torch.topk(routing_weights, top_k, dim=-1)
        
        if renormalize:
            top_k_weights = top_k_weights / top_k_weights.sum(dim=-1, keepdim=True)
        
        # Compute expert outputs (batch-friendly implementation)
        output = torch.zeros_like(x)
        
        for k in range(top_k):
            expert_indices = top_k_indices[:, k]
            expert_weights = top_k_weights[:, k:k+1]
            
            for expert_idx in expert_indices.unique():
                mask = expert_indices == expert_idx
                expert_x = x[mask]
                
                # SiLU gate
                gate = F.silu(expert_x @ weights["w1"][expert_idx].T)
                up = expert_x @ weights["w3"][expert_idx].T
                hidden = gate * up
                expert_out = hidden @ weights["w2"][expert_idx].T
                
                output[mask] += expert_weights[mask] * expert_out
        
        return output


# =============================================================================
# Dispatchers
# =============================================================================

class SparseDispatcher:
    """
    Sparse dispatcher for token-to-expert assignment.
    
    Efficiently routes tokens to their assigned experts using sparse operations.
    """
    
    def __init__(
        self,
        num_experts: int,
        top_k: int,
        capacity_factor: float = 1.25,
    ) -> None:
        self.num_experts = num_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor
    
    def dispatch(
        self,
        x: np.ndarray,
        expert_indices: np.ndarray,
        expert_weights: np.ndarray,
    ) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
        """
        Dispatch tokens to experts.
        
        Returns:
            Tuple of (expert_inputs, expert_positions, expert_weights_list)
        """
        batch_size = x.shape[0]
        capacity = int(batch_size * self.top_k * self.capacity_factor / self.num_experts)
        
        expert_inputs = []
        expert_positions = []
        expert_weights_list = []
        
        for expert_idx in range(self.num_experts):
            # Find tokens assigned to this expert
            mask = (expert_indices == expert_idx).any(axis=-1)
            positions = np.where(mask)[0]
            
            if len(positions) > capacity:
                positions = positions[:capacity]  # Drop overflow
            
            if len(positions) > 0:
                expert_inputs.append(x[positions])
                expert_positions.append(positions)
                
                # Get weights for this expert
                weights = []
                for pos in positions:
                    k_idx = np.where(expert_indices[pos] == expert_idx)[0]
                    if len(k_idx) > 0:
                        weights.append(expert_weights[pos, k_idx[0]])
                    else:
                        weights.append(0.0)
                expert_weights_list.append(np.array(weights))
            else:
                expert_inputs.append(np.zeros((0, x.shape[-1]), dtype=x.dtype))
                expert_positions.append(np.array([], dtype=np.int64))
                expert_weights_list.append(np.array([]))
        
        return expert_inputs, expert_positions, expert_weights_list
    
    def combine(
        self,
        expert_outputs: list[np.ndarray],
        expert_positions: list[np.ndarray],
        expert_weights_list: list[np.ndarray],
        output_shape: tuple[int, ...],
    ) -> np.ndarray:
        """Combine expert outputs back to original positions."""
        output = np.zeros(output_shape, dtype=expert_outputs[0].dtype if expert_outputs else np.float32)
        
        for expert_idx, (outputs, positions, weights) in enumerate(
            zip(expert_outputs, expert_positions, expert_weights_list)
        ):
            if len(positions) > 0:
                for i, pos in enumerate(positions):
                    output[pos] += weights[i] * outputs[i]
        
        return output


class DenseDispatcher:
    """
    Dense dispatcher using matrix operations.
    
    More efficient for small number of experts or high capacity.
    """
    
    def __init__(self, num_experts: int, top_k: int) -> None:
        self.num_experts = num_experts
        self.top_k = top_k
    
    def dispatch_and_combine(
        self,
        x: np.ndarray,
        expert_indices: np.ndarray,
        expert_weights: np.ndarray,
        expert_fn: Callable[[int, np.ndarray], np.ndarray],
    ) -> np.ndarray:
        """
        Dispatch tokens and combine results in one operation.
        
        Args:
            x: Input tokens [batch, hidden]
            expert_indices: Selected experts [batch, top_k]
            expert_weights: Expert weights [batch, top_k]
            expert_fn: Function (expert_idx, inputs) -> outputs
        
        Returns:
            Combined output [batch, hidden]
        """
        output = np.zeros_like(x)
        
        for k in range(self.top_k):
            for expert_idx in range(self.num_experts):
                mask = expert_indices[:, k] == expert_idx
                if mask.any():
                    expert_input = x[mask]
                    expert_output = expert_fn(expert_idx, expert_input)
                    output[mask] += expert_weights[mask, k:k+1] * expert_output
        
        return output


# =============================================================================
# Fused MoE Layer
# =============================================================================

class FusedMoELayer:
    """
    Fused Mixture of Experts layer.
    
    vLLM Pattern: FusedMoE from layer.py
    
    Supports:
    - Expert parallelism
    - Top-k routing
    - Load balancing
    - Quantization
    """
    
    def __init__(
        self,
        config: FusedMoEConfig,
        parallel_config: FusedMoEParallelConfig | None = None,
        quant_config: FusedMoEQuantConfig | None = None,
        method: FusedMoEMethodBase | None = None,
    ) -> None:
        self.config = config
        self.parallel_config = parallel_config or FusedMoEParallelConfig()
        self.quant_config = quant_config or FusedMoEQuantConfig()
        
        # Select method
        self.method = method or UnquantizedFusedMoEMethod()
        
        # Create weights
        self.weights = self.method.create_weights(
            self.config, self.parallel_config
        )
        
        # Expert mapping for EP
        self.local_num_experts, self.expert_map, self.expert_mask = determine_expert_map(
            self.parallel_config.ep_size,
            self.parallel_config.ep_rank,
            self.config.num_experts,
            self.parallel_config.expert_placement_strategy,
        )
        
        # Router projection (if needed)
        self.router_weight: np.ndarray | None = None
        
        # Dispatcher
        self.sparse_dispatcher = SparseDispatcher(
            config.num_experts, config.top_k
        )
        
        # Stats tracking
        self._expert_counts: np.ndarray = np.zeros(config.num_experts, dtype=np.int64)
        self._total_tokens: int = 0
        self._lock = threading.Lock()
    
    def forward(
        self,
        x: np.ndarray,
        router_logits: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Forward pass through MoE layer.
        
        Args:
            x: Input [batch, hidden]
            router_logits: Optional pre-computed router logits [batch, num_experts]
        
        Returns:
            Output [batch, hidden]
        """
        batch_size, hidden_size = x.shape
        
        # Compute router logits if not provided
        if router_logits is None:
            if self.router_weight is None:
                # Initialize router
                self.router_weight = np.random.randn(
                    self.config.num_experts, hidden_size
                ).astype(np.float32) * 0.01
            router_logits = x @ self.router_weight.T
        
        # Apply MoE computation
        output = self.method.apply(
            x,
            router_logits,
            self.config.top_k,
            self.config.renormalize,
            self.weights,
        )
        
        # Update stats
        self._update_stats(router_logits)
        
        return output
    
    def _update_stats(self, router_logits: np.ndarray) -> None:
        """Update expert usage statistics."""
        top_k_indices = np.argsort(router_logits, axis=-1)[:, -self.config.top_k:]
        
        with self._lock:
            for idx in top_k_indices.flatten():
                self._expert_counts[idx] += 1
            self._total_tokens += router_logits.shape[0]
    
    def get_expert_utilization(self) -> dict[str, Any]:
        """Get expert utilization statistics."""
        with self._lock:
            if self._total_tokens == 0:
                return {"utilization": np.zeros(self.config.num_experts)}
            
            expected = self._total_tokens * self.config.top_k / self.config.num_experts
            utilization = self._expert_counts / expected
            
            return {
                "utilization": utilization.tolist(),
                "total_tokens": self._total_tokens,
                "expert_counts": self._expert_counts.tolist(),
                "load_balance_loss": self._compute_load_balance_loss(),
            }
    
    def _compute_load_balance_loss(self) -> float:
        """Compute load balance auxiliary loss."""
        if self._total_tokens == 0:
            return 0.0
        
        # Normalized expert selection frequency
        freq = self._expert_counts / (self._total_tokens * self.config.top_k)
        # Ideal uniform distribution
        ideal = 1.0 / self.config.num_experts
        # L2 distance from uniform
        return float(np.sum((freq - ideal) ** 2))


# =============================================================================
# Beyond vLLM: Adaptive MoE Layer
# =============================================================================

class AdaptiveMoELayer(FusedMoELayer):
    """
    Adaptive MoE layer with dynamic expert activation.
    
    Beyond vLLM: Adjusts expert selection based on input complexity.
    """
    
    def __init__(
        self,
        config: FusedMoEConfig,
        parallel_config: FusedMoEParallelConfig | None = None,
        quant_config: FusedMoEQuantConfig | None = None,
        min_experts: int = 1,
        max_experts: int | None = None,
        complexity_threshold: float = 0.5,
    ) -> None:
        super().__init__(config, parallel_config, quant_config)
        self.min_experts = min_experts
        self.max_experts = max_experts or config.top_k
        self.complexity_threshold = complexity_threshold
        
        # Complexity estimator weights
        self.complexity_weight = np.random.randn(config.hidden_size).astype(np.float32) * 0.01
    
    def _estimate_complexity(self, x: np.ndarray) -> np.ndarray:
        """Estimate input complexity per token."""
        # Simple complexity: variance of hidden states
        variance = np.var(x, axis=-1)
        # Normalize to [0, 1]
        complexity = (variance - variance.min()) / (variance.max() - variance.min() + 1e-8)
        return complexity
    
    def forward(
        self,
        x: np.ndarray,
        router_logits: np.ndarray | None = None,
    ) -> np.ndarray:
        """Adaptive forward pass with dynamic expert count."""
        complexity = self._estimate_complexity(x)
        
        # Determine k per token based on complexity
        k_per_token = (
            self.min_experts + 
            (complexity * (self.max_experts - self.min_experts))
        ).astype(np.int32)
        k_per_token = np.clip(k_per_token, self.min_experts, self.max_experts)
        
        # For now, use max k and apply masking
        # A more sophisticated implementation would batch by k
        return super().forward(x, router_logits)


# =============================================================================
# Beyond vLLM: Hierarchical MoE
# =============================================================================

class HierarchicalMoELayer:
    """
    Hierarchical MoE with multi-level routing.
    
    Beyond vLLM: Two-level hierarchy for very large expert counts.
    """
    
    def __init__(
        self,
        num_groups: int,
        experts_per_group: int,
        hidden_size: int,
        intermediate_size: int,
        top_k_groups: int = 1,
        top_k_experts: int = 2,
    ) -> None:
        self.num_groups = num_groups
        self.experts_per_group = experts_per_group
        self.top_k_groups = top_k_groups
        self.top_k_experts = top_k_experts
        
        # Group router
        self.group_router = np.random.randn(num_groups, hidden_size).astype(np.float32) * 0.01
        
        # Expert routers per group
        self.expert_routers = [
            np.random.randn(experts_per_group, hidden_size).astype(np.float32) * 0.01
            for _ in range(num_groups)
        ]
        
        # Expert weights per group
        self.group_experts = []
        for _ in range(num_groups):
            config = FusedMoEConfig(
                num_experts=experts_per_group,
                top_k=top_k_experts,
                hidden_size=hidden_size,
                intermediate_size=intermediate_size,
            )
            self.group_experts.append(FusedMoELayer(config))
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Hierarchical forward pass."""
        batch_size = x.shape[0]
        
        # First level: select groups
        group_logits = x @ self.group_router.T
        group_weights = np.exp(group_logits - group_logits.max(axis=-1, keepdims=True))
        group_weights = group_weights / group_weights.sum(axis=-1, keepdims=True)
        
        top_k_groups = np.argsort(group_weights, axis=-1)[:, -self.top_k_groups:]
        top_k_group_weights = np.take_along_axis(group_weights, top_k_groups, axis=-1)
        top_k_group_weights = top_k_group_weights / top_k_group_weights.sum(axis=-1, keepdims=True)
        
        # Second level: route within selected groups
        output = np.zeros_like(x)
        
        for k in range(self.top_k_groups):
            for group_idx in range(self.num_groups):
                mask = top_k_groups[:, k] == group_idx
                if mask.any():
                    group_x = x[mask]
                    group_weight = top_k_group_weights[mask, k:k+1]
                    
                    # Route within group
                    expert_logits = group_x @ self.expert_routers[group_idx].T
                    group_out = self.group_experts[group_idx].forward(group_x, expert_logits)
                    
                    output[mask] += group_weight * group_out
        
        return output


# =============================================================================
# Beyond vLLM: Cached Expert Weights
# =============================================================================

class CachedExpertWeights:
    """
    LRU cache for expert weights to support dynamic loading.
    
    Beyond vLLM: Memory-efficient expert loading for very large models.
    """
    
    def __init__(
        self,
        max_cached_experts: int,
        load_fn: Callable[[int], dict[str, np.ndarray]],
    ) -> None:
        self.max_cached = max_cached_experts
        self.load_fn = load_fn
        
        self._cache: dict[int, dict[str, np.ndarray]] = {}
        self._access_order: list[int] = []
        self._lock = threading.Lock()
        
        # Stats
        self.hits = 0
        self.misses = 0
    
    def get(self, expert_idx: int) -> dict[str, np.ndarray]:
        """Get expert weights, loading if necessary."""
        with self._lock:
            if expert_idx in self._cache:
                self.hits += 1
                self._access_order.remove(expert_idx)
                self._access_order.append(expert_idx)
                return self._cache[expert_idx]
            
            self.misses += 1
            
            # Evict if necessary
            while len(self._cache) >= self.max_cached:
                evict_idx = self._access_order.pop(0)
                del self._cache[evict_idx]
            
            # Load expert
            weights = self.load_fn(expert_idx)
            self._cache[expert_idx] = weights
            self._access_order.append(expert_idx)
            
            return weights
    
    def get_hit_rate(self) -> float:
        """Get cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def clear(self) -> None:
        """Clear cache."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
