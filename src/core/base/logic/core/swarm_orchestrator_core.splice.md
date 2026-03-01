# Class Breakdown: swarm_orchestrator_core

**File**: `src\core\base\logic\core\swarm_orchestrator_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DelegationMode`

**Line**: 20  
**Inherits**: str, Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `delegationmode.py`

---

### 2. `SwarmMember`

**Line**: 26  
**Methods**: 0

[TIP] **Suggested split**: Move to `swarmmember.py`

---

### 3. `SwarmOrchestratorCore`

**Line**: 33  
**Methods**: 4

Handles higher-level multi-agent orchestration logic.
Patterns harvested from Agno (Team) and AgentUniverse (WorkPatterns).

[TIP] **Suggested split**: Move to `swarmorchestratorcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
