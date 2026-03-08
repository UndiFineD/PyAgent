# Class Breakdown: agent_card_core

**File**: `src\core\base\logic\core\agent_card_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentCapability`

**Line**: 18  
**Inherits**: BaseModel  
**Methods**: 0

[TIP] **Suggested split**: Move to `agentcapability.py`

---

### 2. `AgentCard`

**Line**: 24  
**Inherits**: BaseModel  
**Methods**: 0

Standardized manifest for cross-agent discovery.
Pattern harvested from agentic_design_patterns.

[TIP] **Suggested split**: Move to `agentcard.py`

---

### 3. `AgentCardCore`

**Line**: 38  
**Methods**: 5

Manages a registry of AgentCards for inter-agent communication (A2A).

[TIP] **Suggested split**: Move to `agentcardcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
