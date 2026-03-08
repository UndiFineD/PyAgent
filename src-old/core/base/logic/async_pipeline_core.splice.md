# Class Breakdown: async_pipeline_core

**File**: `src\core\base\logic\async_pipeline_core.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TaskStatus`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Status of a pipeline task

[TIP] **Suggested split**: Move to `taskstatus.py`

---

### 2. `TaskPriority`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

Priority levels for tasks

[TIP] **Suggested split**: Move to `taskpriority.py`

---

### 3. `PipelineTask`

**Line**: 49  
**Methods**: 1

Represents a task in the async pipeline

[TIP] **Suggested split**: Move to `pipelinetask.py`

---

### 4. `PipelineConfig`

**Line**: 75  
**Methods**: 0

Configuration for the async pipeline

[TIP] **Suggested split**: Move to `pipelineconfig.py`

---

### 5. `AsyncPipelineCore`

**Line**: 85  
**Methods**: 8

Orchestrates asynchronous coding agent pipelines
Based on the Asynchronous Coding Agent Pipeline pattern from agentic-patterns

[TIP] **Suggested split**: Move to `asyncpipelinecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
