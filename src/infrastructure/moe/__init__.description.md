# __init__

**File**: `src\infrastructure\moe\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 16 imports  
**Lines**: 53  
**Complexity**: 0 (simple)

## Overview

Mixture of Experts (MoE) Infrastructure.

Phase 38: Advanced MoE patterns from vLLM with beyond-vLLM innovations.

Modules:
    FusedMoELayer: Fused mixture of experts with expert parallelism
    ExpertRouter: Token-to-expert routing with load balancing
    MoEConfig: Configuration for MoE layers

## Dependencies

**Imports** (16):
- `src.infrastructure.moe.ExpertRouter.AdaptiveRouter`
- `src.infrastructure.moe.ExpertRouter.ExpertChoiceRouter`
- `src.infrastructure.moe.ExpertRouter.RouterConfig`
- `src.infrastructure.moe.ExpertRouter.RouterOutput`
- `src.infrastructure.moe.ExpertRouter.RoutingMethod`
- `src.infrastructure.moe.ExpertRouter.RoutingSimulator`
- `src.infrastructure.moe.ExpertRouter.SoftMoERouter`
- `src.infrastructure.moe.ExpertRouter.TopKRouter`
- `src.infrastructure.moe.FusedMoELayer.DenseDispatcher`
- `src.infrastructure.moe.FusedMoELayer.ExpertPlacementStrategy`
- `src.infrastructure.moe.FusedMoELayer.FusedMoEConfig`
- `src.infrastructure.moe.FusedMoELayer.FusedMoELayer`
- `src.infrastructure.moe.FusedMoELayer.FusedMoEMethodBase`
- `src.infrastructure.moe.FusedMoELayer.FusedMoEParallelConfig`
- `src.infrastructure.moe.FusedMoELayer.SparseDispatcher`
- ... and 1 more

---
*Auto-generated documentation*
