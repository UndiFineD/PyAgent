# routing

**File**: `src\infrastructure\cloud\routing.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 15 imports  
**Lines**: 389  
**Complexity**: 12 (moderate)

## Overview

Intelligent routing for multi-cloud AI providers.

Routes requests to the optimal provider based on model availability,
latency requirements, budget constraints, and provider health.

## Classes (4)

### `RoutingStrategy`

**Inherits from**: Enum

Strategy for selecting providers.

### `ProviderMetrics`

Metrics for a registered provider.

### `RoutingConstraints`

Constraints for routing decisions.

### `IntelligentRouter`

Intelligent request router for multi-cloud AI providers.

Manages provider registration, health monitoring, and intelligent
routing based on various optimization strategies.

Example:
    router = IntelligentRouter()
    router.register_provider(gemini_connector, priority=1)
    router.register_provider(groq_connector, priority=2)
    
    # Get best provider for a request
    provider = await router.get_provider_for_request(
        request,
        strategy=RoutingStrategy.LATENCY_OPTIMIZED
    )
    
    response = await provider.complete(request)

**Methods** (12):
- `__init__(self, default_strategy, health_check_interval, failover_cooldown)`
- `register_provider(self, provider, priority, cost_per_1k_tokens)`
- `unregister_provider(self, name)`
- `_get_candidates(self, model, constraints)`
- `_is_provider_healthy(self, name)`
- `_route_by_cost(self, candidates, request)`
- `_route_by_latency(self, candidates)`
- `_route_by_priority(self, candidates)`
- `_route_round_robin(self, candidates)`
- `_route_failover(self, candidates)`
- ... and 2 more methods

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `base.CloudProviderBase`
- `base.InferenceRequest`
- `base.InferenceResponse`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
