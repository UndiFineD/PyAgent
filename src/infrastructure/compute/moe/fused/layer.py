from __future__ import annotations
import threading
import numpy as np
from typing import Any, Optional
from .config import FusedMoEConfig, FusedMoEParallelConfig, FusedMoEQuantConfig
from .method import FusedMoEMethodBase, UnquantizedFusedMoEMethod
from .utils import determine_expert_map
from .dispatcher import SparseDispatcher

class FusedMoELayer:
    """Fused Mixture of Experts layer."""
    
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
        batch_size, hidden_size = x.shape
        
        if router_logits is None:
            if self.router_weight is None:
                self.router_weight = np.random.randn(
                    self.config.num_experts, hidden_size
                ).astype(np.float32) * 0.01
            router_logits = x @ self.router_weight.T
        
        output = self.method.apply(
            x,
            router_logits,
            self.config.top_k,
            self.config.renormalize,
            self.weights,
        )
        
        self._update_stats(router_logits)
        
        return output
    
    def _update_stats(self, router_logits: np.ndarray) -> None:
        top_k_indices = np.argsort(router_logits, axis=-1)[:, -self.config.top_k:]
        
        with self._lock:
            for idx in top_k_indices.flatten():
                self._expert_counts[idx] += 1
            self._total_tokens += router_logits.shape[0]
    
    def get_expert_utilization(self) -> dict[str, Any]:
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
        if self._total_tokens == 0:
            return 0.0
        
        freq = self._expert_counts / (self._total_tokens * self.config.top_k)
        ideal = 1.0 / self.config.num_experts
        return float(np.sum((freq - ideal) ** 2))
