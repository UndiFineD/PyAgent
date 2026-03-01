# Class Breakdown: ExpertRouter

**File**: `src\infrastructure\moe\ExpertRouter.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RoutingMethod`

**Line**: 46  
**Inherits**: str, Enum  
**Methods**: 0

Routing method for token-to-expert assignment.

[TIP] **Suggested split**: Move to `routingmethod.py`

---

### 2. `RouterConfig`

**Line**: 60  
**Methods**: 0

Configuration for expert router.

[TIP] **Suggested split**: Move to `routerconfig.py`

---

### 3. `RouterOutput`

**Line**: 91  
**Methods**: 0

Output from router forward pass.

[TIP] **Suggested split**: Move to `routeroutput.py`

---

### 4. `RouterBase`

**Line**: 110  
**Inherits**: ABC  
**Methods**: 7

Base class for expert routers.

[TIP] **Suggested split**: Move to `routerbase.py`

---

### 5. `TopKRouter`

**Line**: 225  
**Inherits**: RouterBase  
**Methods**: 2

Standard top-k router.

vLLM Pattern: Default routing in FusedMoE

[TIP] **Suggested split**: Move to `topkrouter.py`

---

### 6. `GroupedTopKRouter`

**Line**: 289  
**Inherits**: RouterBase  
**Methods**: 1

Grouped top-k router for expert groups.

vLLM Pattern: grouped_topk from fused_moe.py

[TIP] **Suggested split**: Move to `groupedtopkrouter.py`

---

### 7. `ExpertChoiceRouter`

**Line**: 356  
**Inherits**: RouterBase  
**Methods**: 2

Expert-choice router where experts select tokens.

Beyond vLLM: Inverse routing for better load balance.

[TIP] **Suggested split**: Move to `expertchoicerouter.py`

---

### 8. `SoftMoERouter`

**Line**: 452  
**Inherits**: RouterBase  
**Methods**: 2

Soft MoE router with differentiable soft assignments.

Beyond vLLM: Fully differentiable routing without discrete selection.

[TIP] **Suggested split**: Move to `softmoerouter.py`

---

### 9. `AdaptiveRouter`

**Line**: 498  
**Inherits**: RouterBase  
**Methods**: 3

Adaptive router with learned routing thresholds.

Beyond vLLM: Dynamic k selection based on input.

[TIP] **Suggested split**: Move to `adaptiverouter.py`

---

### 10. `RoutingSimulator`

**Line**: 575  
**Methods**: 5

Simulate routing behavior for analysis.

vLLM Pattern: RoutingSimulator from routing_simulator.py

[TIP] **Suggested split**: Move to `routingsimulator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
