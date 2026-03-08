# FleetLoadBalancer

**File**: `src\classes\api\FleetLoadBalancer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 52  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for FleetLoadBalancer.

## Classes (1)

### `FleetLoadBalancer`

GUI Improvements: Load Balancer for multi-interface traffic.
Integrated with LoadBalancerCore for cognitive pressure distribution.

**Methods** (3):
- `__init__(self, fleet)`
- `balance_request(self, interface, command)`
- `get_stats(self)`

## Dependencies

**Imports** (9):
- `logging`
- `random`
- `src.infrastructure.api.core.GatewayCore.GatewayCore`
- `src.infrastructure.fleet.core.LoadBalancerCore.AgentMetrics`
- `src.infrastructure.fleet.core.LoadBalancerCore.LoadBalancerCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
