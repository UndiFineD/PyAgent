"""
Expert Router for Mixture of Experts.

vLLM Pattern: Routing logic from fused_moe/layer.py
Implements various routing strategies for token-to-expert assignment.

Beyond vLLM:
- AdaptiveRouter with learned routing thresholds
- SoftMoE with soft expert assignment
- ExpertChoiceRouter for expert-centric routing
"""

from __future__ import annotations

import math
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional, TYPE_CHECKING

import numpy as np

# Optional torch import
try:
    import torch
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore
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

class RoutingMethod(str, Enum):
    """Routing method for token-to-expert assignment."""
    TOP_K = "top_k"  # Standard top-k routing
    EXPERT_CHOICE = "expert_choice"  # Expert chooses tokens
    SOFT_MOE = "soft_moe"  # Soft assignment
    GROUPED_TOP_K = "grouped_top_k"  # Grouped top-k
    ADAPTIVE = "adaptive"  # Learned adaptive routing


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class RouterConfig:
    """Configuration for expert router."""
    num_experts: int
    top_k: int
    hidden_size: int
    
    # Routing settings
    method: RoutingMethod = RoutingMethod.TOP_K
    renormalize: bool = True
    
    # Load balancing
    aux_loss_coef: float = 0.01
    z_loss_coef: float = 0.001
    
    # Grouped routing
    num_expert_groups: int = 1
    topk_group: int = 1
    
    # Capacity limits
    capacity_factor: float = 1.25
    drop_tokens: bool = False
    
    # Noise for exploration
    noise_std: float = 0.0


# =============================================================================
# Router Output
# =============================================================================

@dataclass
class RouterOutput:
    """Output from router forward pass."""
    expert_indices: np.ndarray  # [batch, top_k] - selected expert indices
    expert_weights: np.ndarray  # [batch, top_k] - routing weights
    router_logits: np.ndarray  # [batch, num_experts] - raw logits
    
    # Optional auxiliary outputs
    aux_loss: float = 0.0  # Load balancing loss
    z_loss: float = 0.0  # Router z-loss
    dropped_tokens: int = 0  # Number of dropped tokens
    
    # Per-expert statistics
    expert_counts: np.ndarray | None = None  # [num_experts] - token counts


# =============================================================================
# Router Base Class
# =============================================================================

class RouterBase(ABC):
    """Base class for expert routers."""
    
    def __init__(self, config: RouterConfig) -> None:
        self.config = config
        
        # Router weight
        self.weight = np.random.randn(
            config.num_experts, config.hidden_size
        ).astype(np.float32) * (1.0 / math.sqrt(config.hidden_size))
        
        # Statistics tracking
        self._total_tokens = 0
        self._expert_counts = np.zeros(config.num_experts, dtype=np.int64)
        self._lock = threading.Lock()
    
    @abstractmethod
    def forward(self, x: np.ndarray) -> RouterOutput:
        """
        Route tokens to experts.
        
        Args:
            x: Input hidden states [batch, hidden_size]
        
        Returns:
            RouterOutput with expert assignments and weights
        """
        pass
    
    def compute_router_logits(self, x: np.ndarray) -> np.ndarray:
        """Compute router logits."""
        logits = x @ self.weight.T
        
        # Add noise for exploration during training
        if self.config.noise_std > 0:
            noise = np.random.randn(*logits.shape) * self.config.noise_std
            logits = logits + noise.astype(np.float32)
        
        return logits
    
    def compute_aux_loss(
        self,
        router_logits: np.ndarray,
        expert_indices: np.ndarray,
    ) -> float:
        """
        Compute auxiliary load balancing loss.
        
        vLLM Pattern: aux_loss computation in MoE layers
        """
        if self.config.aux_loss_coef == 0:
            return 0.0
        
        batch_size = router_logits.shape[0]
        num_experts = self.config.num_experts
        
        # Expert selection frequency
        expert_mask = np.zeros((batch_size, num_experts), dtype=np.float32)
        for i in range(batch_size):
            for k in range(self.config.top_k):
                expert_mask[i, expert_indices[i, k]] = 1.0
        
        # Mean routing probability
        routing_probs = np.exp(router_logits - router_logits.max(axis=-1, keepdims=True))
        routing_probs = routing_probs / routing_probs.sum(axis=-1, keepdims=True)
        
        # Load balance loss: encourage uniform distribution
        expert_fraction = expert_mask.mean(axis=0)
        prob_fraction = routing_probs.mean(axis=0)
        
        aux_loss = num_experts * np.sum(expert_fraction * prob_fraction)
        
        return float(aux_loss * self.config.aux_loss_coef)
    
    def compute_z_loss(self, router_logits: np.ndarray) -> float:
        """
        Compute router z-loss to prevent logit explosion.
        
        vLLM Pattern: z_loss for numerical stability
        """
        if self.config.z_loss_coef == 0:
            return 0.0
        
        # Mean of squared max logits
        z_loss = np.mean(np.max(router_logits, axis=-1) ** 2)
        
        return float(z_loss * self.config.z_loss_coef)
    
    def update_stats(self, expert_indices: np.ndarray) -> None:
        """Update routing statistics."""
        with self._lock:
            self._total_tokens += expert_indices.shape[0]
            for idx in expert_indices.flatten():
                self._expert_counts[idx] += 1
    
    def get_stats(self) -> dict[str, Any]:
        """Get routing statistics."""
        with self._lock:
            if self._total_tokens == 0:
                return {"expert_utilization": []}
            
            expected = self._total_tokens * self.config.top_k / self.config.num_experts
            utilization = (self._expert_counts / expected).tolist()
            
            return {
                "total_tokens": self._total_tokens,
                "expert_counts": self._expert_counts.tolist(),
                "expert_utilization": utilization,
            }


# =============================================================================
# Top-K Router
# =============================================================================

class TopKRouter(RouterBase):
    """
    Standard top-k router.
    
    vLLM Pattern: Default routing in FusedMoE
    """
    
    def forward(self, x: np.ndarray) -> RouterOutput:
        """Route using top-k selection."""
        batch_size = x.shape[0]
        
        # Compute logits
        router_logits = self.compute_router_logits(x)
        
        # Get top-k experts
        if HAS_RUST and hasattr(rust_core, 'topk_routing_rust'):
            expert_indices, expert_weights = rust_core.topk_routing_rust(
                router_logits, self.config.top_k, self.config.renormalize
            )
        else:
            expert_indices, expert_weights = self._topk_numpy(router_logits)
        
        # Update statistics
        self.update_stats(expert_indices)
        
        # Compute losses
        aux_loss = self.compute_aux_loss(router_logits, expert_indices)
        z_loss = self.compute_z_loss(router_logits)
        
        return RouterOutput(
            expert_indices=expert_indices,
            expert_weights=expert_weights,
            router_logits=router_logits,
            aux_loss=aux_loss,
            z_loss=z_loss,
            expert_counts=self._expert_counts.copy(),
        )
    
    def _topk_numpy(
        self,
        router_logits: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """NumPy implementation of top-k selection."""
        # Softmax
        routing_weights = np.exp(router_logits - router_logits.max(axis=-1, keepdims=True))
        routing_weights = routing_weights / routing_weights.sum(axis=-1, keepdims=True)
        
        # Top-k selection
        expert_indices = np.argsort(routing_weights, axis=-1)[:, -self.config.top_k:]
        expert_indices = expert_indices[:, ::-1]  # Descending order
        
        expert_weights = np.take_along_axis(routing_weights, expert_indices, axis=-1)
        
        # Renormalize
        if self.config.renormalize:
            expert_weights = expert_weights / expert_weights.sum(axis=-1, keepdims=True)
        
        return expert_indices, expert_weights


# =============================================================================
# Grouped Top-K Router
# =============================================================================

class GroupedTopKRouter(RouterBase):
    """
    Grouped top-k router for expert groups.
    
    vLLM Pattern: grouped_topk from fused_moe.py
    """
    
    def forward(self, x: np.ndarray) -> RouterOutput:
        """Route using grouped top-k selection."""
        batch_size = x.shape[0]
        num_experts = self.config.num_experts
        num_groups = self.config.num_expert_groups
        experts_per_group = num_experts // num_groups
        
        # Compute logits
        router_logits = self.compute_router_logits(x)
        
        # Reshape for group processing
        logits_grouped = router_logits.reshape(batch_size, num_groups, experts_per_group)
        
        # Select top-k groups first
        group_scores = logits_grouped.max(axis=-1)
        top_groups = np.argsort(group_scores, axis=-1)[:, -self.config.topk_group:]
        
        # Then select top-k experts within selected groups
        expert_indices = []
        expert_weights = []
        
        for i in range(batch_size):
            selected = []
            for g in top_groups[i]:
                group_logits = logits_grouped[i, g]
                top_in_group = np.argsort(group_logits)[-self.config.top_k:]
                selected.extend(g * experts_per_group + top_in_group)
            
            # Get final top-k from selected
            selected = np.array(selected)
            selected_scores = router_logits[i, selected]
            final_topk = np.argsort(selected_scores)[-self.config.top_k:]
            
            expert_indices.append(selected[final_topk][::-1])
            expert_weights.append(selected_scores[final_topk][::-1])
        
        expert_indices = np.array(expert_indices)
        expert_weights = np.array(expert_weights)
        
        # Apply softmax and renormalize
        expert_weights = np.exp(expert_weights - expert_weights.max(axis=-1, keepdims=True))
        if self.config.renormalize:
            expert_weights = expert_weights / expert_weights.sum(axis=-1, keepdims=True)
        
        # Update statistics
        self.update_stats(expert_indices)
        
        return RouterOutput(
            expert_indices=expert_indices,
            expert_weights=expert_weights,
            router_logits=router_logits,
            aux_loss=self.compute_aux_loss(router_logits, expert_indices),
            z_loss=self.compute_z_loss(router_logits),
        )


# =============================================================================
# Expert Choice Router
# =============================================================================

class ExpertChoiceRouter(RouterBase):
    """
    Expert-choice router where experts select tokens.
    
    Beyond vLLM: Inverse routing for better load balance.
    """
    
    def __init__(
        self,
        config: RouterConfig,
        tokens_per_expert: int | None = None,
    ) -> None:
        super().__init__(config)
        self.tokens_per_expert = tokens_per_expert
    
    def forward(self, x: np.ndarray) -> RouterOutput:
        """Route using expert choice."""
        batch_size = x.shape[0]
        num_experts = self.config.num_experts
        
        # Compute logits
        router_logits = self.compute_router_logits(x)
        
        # Each expert selects top tokens
        tokens_per_expert = self.tokens_per_expert or max(
            1, int(batch_size * self.config.top_k / num_experts * self.config.capacity_factor)
        )
        
        # Transpose: experts choose from tokens
        expert_logits = router_logits.T  # [num_experts, batch]
        
        # Each expert selects top tokens
        expert_token_indices = np.argsort(expert_logits, axis=-1)[:, -tokens_per_expert:]
        expert_token_weights = np.take_along_axis(expert_logits, expert_token_indices, axis=-1)
        
        # Softmax per expert
        expert_token_weights = np.exp(expert_token_weights - expert_token_weights.max(axis=-1, keepdims=True))
        expert_token_weights = expert_token_weights / expert_token_weights.sum(axis=-1, keepdims=True)
        
        # Convert back to token-centric format
        # Each token may be selected by multiple experts
        expert_indices = np.full((batch_size, num_experts), -1, dtype=np.int32)
        expert_weights = np.zeros((batch_size, num_experts), dtype=np.float32)
        
        for expert_idx in range(num_experts):
            for pos, token_idx in enumerate(expert_token_indices[expert_idx]):
                # Find first empty slot
                for k in range(num_experts):
                    if expert_indices[token_idx, k] == -1:
                        expert_indices[token_idx, k] = expert_idx
                        expert_weights[token_idx, k] = expert_token_weights[expert_idx, pos]
                        break
        
        # Keep only top_k per token
        final_indices = []
        final_weights = []
        for i in range(batch_size):
            valid = expert_indices[i] >= 0
            valid_indices = expert_indices[i, valid]
            valid_weights = expert_weights[i, valid]
            
            if len(valid_indices) > self.config.top_k:
                top_k_pos = np.argsort(valid_weights)[-self.config.top_k:]
                final_indices.append(valid_indices[top_k_pos][::-1])
                final_weights.append(valid_weights[top_k_pos][::-1])
            else:
                # Pad with zeros if needed
                padded_indices = np.zeros(self.config.top_k, dtype=np.int32)
                padded_weights = np.zeros(self.config.top_k, dtype=np.float32)
                padded_indices[:len(valid_indices)] = valid_indices
                padded_weights[:len(valid_weights)] = valid_weights
                final_indices.append(padded_indices)
                final_weights.append(padded_weights)
        
        expert_indices = np.array(final_indices)
        expert_weights = np.array(final_weights)
        
        # Renormalize
        if self.config.renormalize:
            weight_sum = expert_weights.sum(axis=-1, keepdims=True)
            weight_sum = np.maximum(weight_sum, 1e-8)
            expert_weights = expert_weights / weight_sum
        
        self.update_stats(expert_indices)
        
        return RouterOutput(
            expert_indices=expert_indices,
            expert_weights=expert_weights,
            router_logits=router_logits,
        )


# =============================================================================
# Soft MoE Router
# =============================================================================

class SoftMoERouter(RouterBase):
    """
    Soft MoE router with differentiable soft assignments.
    
    Beyond vLLM: Fully differentiable routing without discrete selection.
    """
    
    def __init__(
        self,
        config: RouterConfig,
        temperature: float = 1.0,
    ) -> None:
        super().__init__(config)
        self.temperature = temperature
    
    def forward(self, x: np.ndarray) -> RouterOutput:
        """Soft routing with all experts weighted."""
        # Compute logits
        router_logits = self.compute_router_logits(x)
        
        # Soft assignment (full softmax)
        scaled_logits = router_logits / self.temperature
        all_weights = np.exp(scaled_logits - scaled_logits.max(axis=-1, keepdims=True))
        all_weights = all_weights / all_weights.sum(axis=-1, keepdims=True)
        
        # Still select top-k for sparse computation
        expert_indices = np.argsort(all_weights, axis=-1)[:, -self.config.top_k:][:, ::-1]
        expert_weights = np.take_along_axis(all_weights, expert_indices, axis=-1)
        
        # Renormalize selected
        if self.config.renormalize:
            expert_weights = expert_weights / expert_weights.sum(axis=-1, keepdims=True)
        
        self.update_stats(expert_indices)
        
        return RouterOutput(
            expert_indices=expert_indices,
            expert_weights=expert_weights,
            router_logits=router_logits,
        )


# =============================================================================
# Beyond vLLM: Adaptive Router
# =============================================================================

class AdaptiveRouter(RouterBase):
    """
    Adaptive router with learned routing thresholds.
    
    Beyond vLLM: Dynamic k selection based on input.
    """
    
    def __init__(
        self,
        config: RouterConfig,
        min_k: int = 1,
        max_k: int | None = None,
    ) -> None:
        super().__init__(config)
        self.min_k = min_k
        self.max_k = max_k or config.top_k
        
        # Learned threshold for each expert
        self.thresholds = np.zeros(config.num_experts, dtype=np.float32)
        
        # K predictor
        self.k_weight = np.random.randn(config.hidden_size).astype(np.float32) * 0.01
    
    def predict_k(self, x: np.ndarray) -> np.ndarray:
        """Predict optimal k per token."""
        # Simple: use projection to predict k
        k_logits = x @ self.k_weight
        k_probs = 1 / (1 + np.exp(-k_logits))  # Sigmoid
        
        # Scale to [min_k, max_k]
        k_values = self.min_k + k_probs * (self.max_k - self.min_k)
        return np.round(k_values).astype(np.int32)
    
    def forward(self, x: np.ndarray) -> RouterOutput:
        """Adaptive routing with per-token k."""
        batch_size = x.shape[0]
        
        # Compute logits
        router_logits = self.compute_router_logits(x)
        
        # Predict k per token
        k_per_token = self.predict_k(x)
        k_per_token = np.clip(k_per_token, self.min_k, self.max_k)
        
        # Apply threshold
        routing_weights = np.exp(router_logits - router_logits.max(axis=-1, keepdims=True))
        routing_weights = routing_weights / routing_weights.sum(axis=-1, keepdims=True)
        
        # Select with variable k (pad to max_k)
        expert_indices = np.zeros((batch_size, self.max_k), dtype=np.int32)
        expert_weights = np.zeros((batch_size, self.max_k), dtype=np.float32)
        
        for i in range(batch_size):
            k = k_per_token[i]
            sorted_idx = np.argsort(routing_weights[i])[::-1]
            expert_indices[i, :k] = sorted_idx[:k]
            expert_weights[i, :k] = routing_weights[i, sorted_idx[:k]]
        
        # Renormalize
        if self.config.renormalize:
            weight_sum = expert_weights.sum(axis=-1, keepdims=True)
            weight_sum = np.maximum(weight_sum, 1e-8)
            expert_weights = expert_weights / weight_sum
        
        self.update_stats(expert_indices)
        
        return RouterOutput(
            expert_indices=expert_indices,
            expert_weights=expert_weights,
            router_logits=router_logits,
        )


# =============================================================================
# Routing Simulator
# =============================================================================

class RoutingSimulator:
    """
    Simulate routing behavior for analysis.
    
    vLLM Pattern: RoutingSimulator from routing_simulator.py
    """
    
    def __init__(
        self,
        num_experts: int,
        num_tokens: int,
        top_k: int,
    ) -> None:
        self.num_experts = num_experts
        self.num_tokens = num_tokens
        self.top_k = top_k
        
        # Generate random routing patterns
        self.routing_history: list[np.ndarray] = []
    
    def simulate_uniform(self) -> np.ndarray:
        """Simulate uniform routing."""
        routing = np.random.randint(0, self.num_experts, (self.num_tokens, self.top_k))
        self.routing_history.append(routing)
        return routing
    
    def simulate_skewed(self, skew_factor: float = 2.0) -> np.ndarray:
        """Simulate skewed routing (some experts get more traffic)."""
        # Power-law distribution
        probs = np.arange(1, self.num_experts + 1, dtype=np.float32) ** (-skew_factor)
        probs = probs / probs.sum()
        
        routing = np.random.choice(
            self.num_experts,
            size=(self.num_tokens, self.top_k),
            p=probs,
        )
        self.routing_history.append(routing)
        return routing
    
    def analyze_load_balance(self, routing: np.ndarray) -> dict[str, Any]:
        """Analyze load balance of routing pattern."""
        expert_counts = np.bincount(routing.flatten(), minlength=self.num_experts)
        expected = self.num_tokens * self.top_k / self.num_experts
        
        return {
            "expert_counts": expert_counts.tolist(),
            "expected_per_expert": expected,
            "max_load": int(expert_counts.max()),
            "min_load": int(expert_counts.min()),
            "load_imbalance": float((expert_counts.max() - expert_counts.min()) / expected),
            "coefficient_of_variation": float(expert_counts.std() / expert_counts.mean()),
        }
    
    def estimate_communication_cost(
        self,
        routing: np.ndarray,
        num_devices: int,
    ) -> dict[str, Any]:
        """Estimate all-to-all communication cost."""
        experts_per_device = self.num_experts // num_devices
        tokens_per_device = self.num_tokens // num_devices
        
        # Count cross-device transfers
        cross_device = 0
        for device_idx in range(num_devices):
            token_start = device_idx * tokens_per_device
            token_end = token_start + tokens_per_device
            
            device_routing = routing[token_start:token_end]
            device_experts_start = device_idx * experts_per_device
            device_experts_end = device_experts_start + experts_per_device
            
            # Count tokens going to other devices
            for expert_idx in device_routing.flatten():
                if not (device_experts_start <= expert_idx < device_experts_end):
                    cross_device += 1
        
        total_assignments = self.num_tokens * self.top_k
        
        return {
            "total_assignments": total_assignments,
            "cross_device_transfers": cross_device,
            "local_assignments": total_assignments - cross_device,
            "communication_ratio": cross_device / total_assignments,
        }
