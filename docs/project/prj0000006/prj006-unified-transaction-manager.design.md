# prj006-unified-transaction-manager - Design

## Problem
PyAgent currently has transaction behavior spread across multiple managers. This can lead to inconsistent commit/rollback semantics and duplicated orchestration logic.

## Design Summary
Use a thin unified transaction orchestration layer that delegates domain operations to existing specialized transaction managers.

## Components
- UnifiedTransactionManager
  - Coordinates transaction lifecycle (`begin`, `commit`, `rollback`)
  - Tracks operation results and failures
- Domain adapters
  - File adapter
  - Memory adapter
  - Process adapter
  - Context adapter
- Audit/telemetry hooks
  - Emit transaction IDs and phase transitions

## Lifecycle
1. Begin transaction and assign transaction ID
2. Execute domain operations in declared order
3. On success, commit all staged changes
4. On failure, rollback completed stages in reverse order
5. Emit final status and error details

## Consistency Rules
- All operations in one transaction share one transaction ID
- Domain adapters must be idempotent for retry-safe stages
- Rollback handlers are mandatory for mutating operations
- Errors propagate with domain + operation metadata

## Mapping to Existing Code
- Memory: `src/MemoryTransactionManager.py`
- Context/state: `src/core/agent_state_manager.py`
- Process execution: `src/core/base/models/communication_models.py` and related process modules
- File-system operations: current storage/file transaction modules in `src/`

## Notes
This design intentionally avoids replacing existing managers. It standardizes orchestration and transaction semantics above them.
