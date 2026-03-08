# Class Breakdown: agent_card

**File**: `src\core\base\models\agent_card.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentCard`

**Line**: 19  
**Inherits**: BaseModel  
**Methods**: 0

Standardized metadata for an agent in the fleet.
Enables cross-agent discovery and orchestration.
Harvested from .external/agentic_design_patterns pattern.

[TIP] **Suggested split**: Move to `agentcard.py`

---

### 2. `Config`

**Line**: 37  
**Methods**: 0

[TIP] **Suggested split**: Move to `config.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
