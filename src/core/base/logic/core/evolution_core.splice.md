# Class Breakdown: evolution_core

**File**: `src\core\base\logic\core\evolution_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentMetadata`

**Line**: 20  
**Methods**: 0

[TIP] **Suggested split**: Move to `agentmetadata.py`

---

### 2. `EvolutionCore`

**Line**: 29  
**Methods**: 4

Manages the lifecycle and evolution of agents based on task performance.
Harvested from self-evolving-subagent patterns.

[TIP] **Suggested split**: Move to `evolutioncore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
