# task_prioritization

**File**: `src\core\base\logic\task_prioritization.py`  
**Type**: Python Module  
**Summary**: 8 classes, 2 functions, 23 imports  
**Lines**: 538  
**Complexity**: 25 (complex)

## Overview

Task Prioritization and Management System

This module implements intelligent task prioritization, assignment, and management
for multi-agent systems. Features include:
- Dynamic priority assignment based on urgency and importance
- Intelligent task routing to appropriate agents
- Workload balancing and resource optimization
- Deadline tracking and escalation mechanisms

Based on patterns from agentic_design_patterns repository.

## Classes (8)

### `PriorityLevel`

**Inherits from**: Enum

Task priority levels.

### `TaskStatus`

**Inherits from**: Enum

Task execution status.

### `TaskType`

**Inherits from**: Enum

Types of tasks that can be managed.

### `Task`

**Inherits from**: BaseModel

Represents a task in the system.

**Methods** (4):
- `validate_deadline(cls, v, values)`
- `is_overdue(self)`
- `time_remaining(self)`
- `priority_score(self)`

### `PrioritizedTask`

Wrapper for tasks in priority queues.

**Methods** (1):
- `__post_init__(self)`

### `AgentCapability`

**Inherits from**: BaseModel

Represents an agent's capabilities.

**Methods** (3):
- `can_handle_task(self, task)`
- `workload_capacity(self)`
- `suitability_score(self, task)`

### `TaskManager`

Central task management system.

**Methods** (14):
- `__init__(self)`
- `add_task(self, task)`
- `update_task(self, task_id)`
- `remove_task(self, task_id)`
- `assign_task(self, task_id, agent_id)`
- `auto_assign_tasks(self)`
- `_find_best_agent(self, task)`
- `complete_task(self, task_id, success)`
- `get_task_queue(self)`
- `get_agent_workload(self)`
- ... and 4 more methods

### `TaskScheduler`

Background task scheduler for automated task management.

**Methods** (1):
- `__init__(self, task_manager, check_interval)`

## Functions (2)

### `create_task(title, description, task_type, priority, deadline, tags, dependencies)`

Create a new task with sensible defaults.

### `create_agent_capability(agent_id, name, skills, max_concurrent_tasks, specialization_scores)`

Create an agent capability profile.

## Dependencies

**Imports** (23):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `heapq`
- `logging`
- `pydantic.BaseModel`
- `pydantic.Field`
- `pydantic.validator`
- `threading`
- `time`
- ... and 8 more

---
*Auto-generated documentation*
