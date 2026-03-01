# Class Breakdown: self_evolution_mixin

**File**: `src\logic\agents\swarm\self_evolution_mixin.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EvolutionMetrics`

**Line**: 28  
**Methods**: 0

Metrics for tracking workflow performance.

[TIP] **Suggested split**: Move to `evolutionmetrics.py`

---

### 2. `EvolutionHistory`

**Line**: 40  
**Methods**: 0

History of workflow evolution attempts.

[TIP] **Suggested split**: Move to `evolutionhistory.py`

---

### 3. `SelfEvolutionMixin`

**Line**: 49  
**Methods**: 13

Mixin that enables self-evolving capabilities for PyAgent orchestrators.

This mixin implements automatic workflow optimization based on execution
feedback, inspired by EvoAgentX's self-evolution algo...

[TIP] **Suggested split**: Move to `selfevolutionmixin.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
