# Class Breakdown: job_manager_core

**File**: `src\core\base\logic\core\job_manager_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `JobStatus`

**Line**: 21  
**Inherits**: Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `jobstatus.py`

---

### 2. `AgentJob`

**Line**: 29  
**Methods**: 0

[TIP] **Suggested split**: Move to `agentjob.py`

---

### 3. `JobManagerCore`

**Line**: 36  
**Methods**: 2

Manages the lifecycle of persistent agent jobs (sessions).
Harvested from LiveKit Agents patterns.

[TIP] **Suggested split**: Move to `jobmanagercore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
