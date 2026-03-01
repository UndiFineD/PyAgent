# Class Breakdown: task_prioritization

**File**: `src\core\base\logic\task_prioritization.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PriorityLevel`

**Line**: 45  
**Inherits**: Enum  
**Methods**: 0

Task priority levels.

[TIP] **Suggested split**: Move to `prioritylevel.py`

---

### 2. `TaskStatus`

**Line**: 54  
**Inherits**: Enum  
**Methods**: 0

Task execution status.

[TIP] **Suggested split**: Move to `taskstatus.py`

---

### 3. `TaskType`

**Line**: 65  
**Inherits**: Enum  
**Methods**: 0

Types of tasks that can be managed.

[TIP] **Suggested split**: Move to `tasktype.py`

---

### 4. `Task`

**Line**: 78  
**Inherits**: BaseModel  
**Methods**: 4

Represents a task in the system.

[TIP] **Suggested split**: Move to `task.py`

---

### 5. `PrioritizedTask`

**Line**: 141  
**Methods**: 1

Wrapper for tasks in priority queues.

[TIP] **Suggested split**: Move to `prioritizedtask.py`

---

### 6. `AgentCapability`

**Line**: 151  
**Inherits**: BaseModel  
**Methods**: 3

Represents an agent's capabilities.

[TIP] **Suggested split**: Move to `agentcapability.py`

---

### 7. `TaskManager`

**Line**: 185  
**Methods**: 14

Central task management system.

[TIP] **Suggested split**: Move to `taskmanager.py`

---

### 8. `TaskScheduler`

**Line**: 382  
**Methods**: 1

Background task scheduler for automated task management.

[TIP] **Suggested split**: Move to `taskscheduler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
