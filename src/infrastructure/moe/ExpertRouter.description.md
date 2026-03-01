# ExpertRouter

**File**: `src\infrastructure\moe\ExpertRouter.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 17 imports  
**Lines**: 660  
**Complexity**: 22 (complex)

## Overview

Expert Router for Mixture of Experts.

vLLM Pattern: Routing logic from fused_moe/layer.py
Implements various routing strategies for token-to-expert assignment.

Beyond vLLM:
- AdaptiveRouter with learned routing thresholds
- SoftMoE with soft expert assignment
- ExpertChoiceRouter for expert-centric routing

## Classes (10)

### `RoutingMethod`

**Inherits from**: str, Enum

Routing method for token-to-expert assignment.

### `RouterConfig`

Configuration for expert router.

### `RouterOutput`

Output from router forward pass.

### `RouterBase`

**Inherits from**: ABC

Base class for expert routers.

**Methods** (7):
- `__init__(self, config)`
- `forward(self, x)`
- `compute_router_logits(self, x)`
- `compute_aux_loss(self, router_logits, expert_indices)`
- `compute_z_loss(self, router_logits)`
- `update_stats(self, expert_indices)`
- `get_stats(self)`

### `TopKRouter`

**Inherits from**: RouterBase

Standard top-k router.

vLLM Pattern: Default routing in FusedMoE

**Methods** (2):
- `forward(self, x)`
- `_topk_numpy(self, router_logits)`

### `GroupedTopKRouter`

**Inherits from**: RouterBase

Grouped top-k router for expert groups.

vLLM Pattern: grouped_topk from fused_moe.py

**Methods** (1):
- `forward(self, x)`

### `ExpertChoiceRouter`

**Inherits from**: RouterBase

Expert-choice router where experts select tokens.

Beyond vLLM: Inverse routing for better load balance.

**Methods** (2):
- `__init__(self, config, tokens_per_expert)`
- `forward(self, x)`

### `SoftMoERouter`

**Inherits from**: RouterBase

Soft MoE router with differentiable soft assignments.

Beyond vLLM: Fully differentiable routing without discrete selection.

**Methods** (2):
- `__init__(self, config, temperature)`
- `forward(self, x)`

### `AdaptiveRouter`

**Inherits from**: RouterBase

Adaptive router with learned routing thresholds.

Beyond vLLM: Dynamic k selection based on input.

**Methods** (3):
- `__init__(self, config, min_k, max_k)`
- `predict_k(self, x)`
- `forward(self, x)`

### `RoutingSimulator`

Simulate routing behavior for analysis.

vLLM Pattern: RoutingSimulator from routing_simulator.py

**Methods** (5):
- `__init__(self, num_experts, num_tokens, top_k)`
- `simulate_uniform(self)`
- `simulate_skewed(self, skew_factor)`
- `analyze_load_balance(self, routing)`
- `estimate_communication_cost(self, routing, num_devices)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `numpy`
- `rust_core`
- `threading`
- `torch`
- `torch.nn.functional`
- `typing.Any`
- `typing.Callable`
- ... and 2 more

---
*Auto-generated documentation*
