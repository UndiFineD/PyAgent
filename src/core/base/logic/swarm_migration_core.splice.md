# Class Breakdown: swarm_migration_core

**File**: `src\core\base\logic\swarm_migration_core.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MigrationTask`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Types of migration tasks supported

[TIP] **Suggested split**: Move to `migrationtask.py`

---

### 2. `MigrationTarget`

**Line**: 44  
**Methods**: 0

Represents a single migration target (file, component, etc.)

[TIP] **Suggested split**: Move to `migrationtarget.py`

---

### 3. `MigrationBatch`

**Line**: 52  
**Methods**: 0

A batch of migration targets for a single sub-agent

[TIP] **Suggested split**: Move to `migrationbatch.py`

---

### 4. `MigrationResult`

**Line**: 61  
**Methods**: 0

Result of a migration batch execution

[TIP] **Suggested split**: Move to `migrationresult.py`

---

### 5. `MigrationStrategy`

**Line**: 71  
**Inherits**: ABC  
**Methods**: 1

Abstract base class for migration strategies

[TIP] **Suggested split**: Move to `migrationstrategy.py`

---

### 6. `SwarmMigrationCore`

**Line**: 85  
**Methods**: 4

Core implementation of the Swarm Migration Pattern
Enables parallel execution of large-scale code migrations using multiple sub-agents

[TIP] **Suggested split**: Move to `swarmmigrationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
