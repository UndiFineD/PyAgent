# unified-transaction-manager - Design

_Status: IN_PROGRESS_
_Designer: @3design | Updated: 2026-03-20_

## Selected Option
Option A - Unified orchestration layer over existing transaction managers.

## Architecture
- UnifiedTransactionManager receives a transaction envelope and operation list.
- Domain adapters delegate to file, memory, process, and context transaction components.
- The orchestrator controls lifecycle: begin, stage, commit, rollback, finalize.
- Observability hooks emit transaction metadata and failure context.

## Interfaces and Contracts
- TransactionEnvelope
  - transaction_id
  - initiator
  - operation_batch
  - timeout_policy
- OperationResult
  - operation_id
  - status
  - payload
  - error_metadata
- AdapterContract
  - prepare(op)
  - commit(op)
  - rollback(op)

## Non-Functional Requirements
- Performance: Keep orchestration overhead minimal; avoid expensive serialization in hot paths.
- Security: Require transaction IDs, preserve audit trail, and avoid leaking sensitive payload data in logs.

## Open Questions
- Should process operations support compensating rollback actions by default?
- Do we require per-operation retry policy overrides in v1?
- Which error taxonomy should be standardized first: domain-specific or unified codes?
