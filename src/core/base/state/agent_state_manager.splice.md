# Class Breakdown: agent_state_manager

**File**: `src\core\base\state\agent_state_manager.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EmergencyEventLog`

**Line**: 37  
**Methods**: 3

Phase 278: Ring buffer recording the last 10 filesystem actions for recovery.

[TIP] **Suggested split**: Move to `emergencyeventlog.py`

---

### 2. `AgentCircuitBreaker`

**Line**: 72  
**Methods**: 7

Phase 336: Circuit breaker for autonomous agents to prevent cascading failures.
Tracks failure rates and halts operations if threshold is exceeded.

[TIP] **Suggested split**: Move to `agentcircuitbreaker.py`

---

### 3. `AgentCheckpointManager`

**Line**: 131  
**Methods**: 3

Phase 336: Manages agent state snapshots and restoration.
Provides logic to rollback agent memory layer and file system changes atomically.

[TIP] **Suggested split**: Move to `agentcheckpointmanager.py`

---

### 4. `StateDriftDetector`

**Line**: 194  
**Methods**: 3

Phase 336: Validates pre/post execution state to detect corruption.

[TIP] **Suggested split**: Move to `statedriftdetector.py`

---

### 5. `StructuredErrorValidator`

**Line**: 220  
**Methods**: 3

Phase 336: Validates and classifies errors to prevent 'Unknown failure' states.
Captures diagnostic metadata for swarm intelligence.

[TIP] **Suggested split**: Move to `structurederrorvalidator.py`

---

### 6. `StateTransaction`

**Line**: 283  
**Methods**: 9

Phase 267: Transactional context manager for agent file operations.

[TIP] **Suggested split**: Move to `statetransaction.py`

---

### 7. `AgentStateManager`

**Line**: 452  
**Methods**: 2

Manages saving and loading agent state to/from disk.

[TIP] **Suggested split**: Move to `agentstatemanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
