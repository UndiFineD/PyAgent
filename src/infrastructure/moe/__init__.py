"""
Mixture of Experts (MoE) Infrastructure.

Phase 38: Advanced MoE patterns from vLLM with beyond-vLLM innovations.

Modules:
    FusedMoELayer: Fused mixture of experts with expert parallelism
    ExpertRouter: Token-to-expert routing with load balancing
    MoEConfig: Configuration for MoE layers
"""

from src.infrastructure.moe.FusedMoELayer import (
    FusedMoEConfig,
    FusedMoEParallelConfig,
    ExpertPlacementStrategy,
    FusedMoEMethodBase,
    UnquantizedFusedMoEMethod,
    FusedMoELayer,
    SparseDispatcher,
    DenseDispatcher,
)

from src.infrastructure.moe.ExpertRouter import (
    RoutingMethod,
    RouterConfig,
    RouterOutput,
    TopKRouter,
    ExpertChoiceRouter,
    SoftMoERouter,
    AdaptiveRouter,
    RoutingSimulator,
)

__all__ = [
    # FusedMoELayer
    "FusedMoEConfig",
    "FusedMoEParallelConfig",
    "ExpertPlacementStrategy",
    "FusedMoEMethodBase",
    "UnquantizedFusedMoEMethod",
    "FusedMoELayer",
    "SparseDispatcher",
    "DenseDispatcher",
    # ExpertRouter
    "RoutingMethod",
    "RouterConfig",
    "RouterOutput",
    "TopKRouter",
    "ExpertChoiceRouter",
    "SoftMoERouter",
    "AdaptiveRouter",
    "RoutingSimulator",
]
