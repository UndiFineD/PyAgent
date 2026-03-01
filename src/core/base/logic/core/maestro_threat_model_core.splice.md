# Class Breakdown: maestro_threat_model_core

**File**: `src\core\base\logic\core\maestro_threat_model_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MaestroLayer`

**Line**: 19  
**Inherits**: str, Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `maestrolayer.py`

---

### 2. `ThreatSeverity`

**Line**: 28  
**Inherits**: str, Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `threatseverity.py`

---

### 3. `AgentThreat`

**Line**: 34  
**Inherits**: BaseModel  
**Methods**: 0

[TIP] **Suggested split**: Move to `agentthreat.py`

---

### 4. `MaestroThreatModelCore`

**Line**: 41  
**Methods**: 3

Evaluates agentic systems against the MAESTRO security framework.
(Multi-Agent Environment, Security, Threat Risk, and Outcome).
Pattern harvested from Agent-Wiz.

[TIP] **Suggested split**: Move to `maestrothreatmodelcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
