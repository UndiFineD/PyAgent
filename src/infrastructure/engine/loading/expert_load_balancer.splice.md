# Class Breakdown: expert_load_balancer

**File**: `src\infrastructure\engine\loading\expert_load_balancer.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExpertType`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

Types of experts in MoE models.

[TIP] **Suggested split**: Move to `experttype.py`

---

### 2. `EplbMetrics`

**Line**: 64  
**Methods**: 3

Metrics regarding expert parallelism load balancing.

vLLM Pattern: EplbModelState from eplb_state.py

[TIP] **Suggested split**: Move to `eplbmetrics.py`

---

### 3. `ExpertMapping`

**Line**: 103  
**Methods**: 2

Complete mapping between logical and physical experts.

vLLM Pattern: Result of rebalance_experts

[TIP] **Suggested split**: Move to `expertmapping.py`

---

### 4. `AbstractEplbPolicy`

**Line**: 132  
**Inherits**: ABC  
**Methods**: 2

Abstract policy regarding expert load balancing.

vLLM Pattern: AbstractEplbPolicy from policy/abstract.py

[TIP] **Suggested split**: Move to `abstracteplbpolicy.py`

---

### 5. `DefaultEplbPolicy`

**Line**: 207  
**Inherits**: AbstractEplbPolicy  
**Methods**: 3

Default EPLB policy with balanced packing.

vLLM Pattern: DefaultEplbPolicy from policy/default.py
Adapted from DeepSeek EPLB algorithm.

[TIP] **Suggested split**: Move to `defaulteplbpolicy.py`

---

### 6. `LocalityAwarePolicy`

**Line**: 376  
**Inherits**: AbstractEplbPolicy  
**Methods**: 1

Locality-aware EPLB policy.

BEYOND vLLM: Considers network topology regarding expert placement.
Prioritizes keeping related experts on same node.

[TIP] **Suggested split**: Move to `localityawarepolicy.py`

---

### 7. `ExpertLoadBalancer`

**Line**: 419  
**Methods**: 14

Main expert load balancer class.

Manages expert replication and rearrangement regarding MoE models.

[TIP] **Suggested split**: Move to `expertloadbalancer.py`

---

### 8. `AsyncExpertRebalancer`

**Line**: 607  
**Methods**: 6

Asynchronous expert rebalancer.

BEYOND vLLM: Background rebalancing with minimal inference disruption.

[TIP] **Suggested split**: Move to `asyncexpertrebalancer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
