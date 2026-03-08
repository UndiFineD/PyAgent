# swarm_migration_core

**File**: `src\core\base\logic\swarm_migration_core.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 15 imports  
**Lines**: 247  
**Complexity**: 5 (moderate)

## Overview

Swarm Migration Core - Parallel sub-agent execution for large-scale code migrations
Based on the Swarm Migration Pattern from agentic-patterns repository

## Classes (6)

### `MigrationTask`

**Inherits from**: Enum

Types of migration tasks supported

### `MigrationTarget`

Represents a single migration target (file, component, etc.)

### `MigrationBatch`

A batch of migration targets for a single sub-agent

### `MigrationResult`

Result of a migration batch execution

### `MigrationStrategy`

**Inherits from**: ABC

Abstract base class for migration strategies

**Methods** (1):
- `get_migration_instructions(self)`

### `SwarmMigrationCore`

Core implementation of the Swarm Migration Pattern
Enables parallel execution of large-scale code migrations using multiple sub-agents

**Methods** (4):
- `__init__(self, max_parallel_agents, batch_size, timeout_seconds)`
- `register_strategy(self, task_type, strategy)`
- `_create_migration_batches(self, targets, strategy)`
- `get_migration_stats(self, trial)`

## Dependencies

**Imports** (15):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `logging`
- `src.core.base.logic.strategy_optimizer.OptimizationTrial`
- `src.core.base.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
