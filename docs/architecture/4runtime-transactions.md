# 4 - Runtime and Transaction Architecture

This document explains how PyAgent executes work safely across Python and Rust while preserving rollback guarantees.

## Runtime model

- Rust (Tokio) is the scheduling backbone for high-throughput task dispatch.
- Python async coroutines orchestrate agent behavior, prompting, and tool invocations.
- Blocking operations are disallowed in hot paths; structure tests enforce this.

## Transaction boundary model

All side-effecting operations must be wrapped in a transaction manager:

- Storage: StorageTransaction (filesystem writes/moves/deletes)
- Memory: MemoryTransaction (agent and runtime memory updates)
- Process: ProcessTransaction (subprocess execution and side effects)
- Context: ContextTransaction (task lineage and recursion control)

## Required transaction behavior

- Begin -> mutate -> validate -> commit for success path.
- Any exception must trigger rollback.
- Rollback must be idempotent and safe to rerun.
- Every transaction should emit structured trace events.

## Failure handling

- Prefer fail-fast at transaction boundaries.
- Surface user-actionable error messages to orchestration layers.
- Keep original error context for postmortem analysis.

## Implementation anchors

- src/core/base/base_agent.py
- src/core/base/agent_state_manager.py
- src/core/base/models/communication_models.py
- rust_core/src

## Operational expectations

- New side-effecting features must declare transaction ownership.
- Tests must include rollback-path verification.
- Performance-sensitive transaction operations should be considered for rust_core acceleration.
