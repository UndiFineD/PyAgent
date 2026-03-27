# prj0000085-shadow-mode-replay - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-27_

## Root Cause Analysis
1. Debugging agent tasks is currently coupled to live execution side effects, so failures are hard to reproduce safely.
2. Existing structured logging is request-centric and does not yet define a replay contract for task-level determinism.
3. The platform already has transaction and context-lineage primitives, but replay/shadow design must decide where those are enforced.

## Step 1 Research Evidence
| Task Type | Findings | Evidence |
|---|---|---|
| Literature review | Project scope requires side-effect-free shadow execution and deterministic replay from structured logs. | `docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.project.md` |
| Prior-art search | Structured logging already established correlation fields and middleware patterns. | `docs/project/prj0000063/structured-logging.project.md`, `docs/project/prj0000063/structured-logging.think.md` |
| Constraint mapping | One-project-one-branch and branch scope boundaries are enforced for lifecycle artifacts. | `docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.project.md`, `/memories/repo/branch-governance.md` |
| Stakeholder impact | Sandbox path controls and transaction wrappers already influence agent runtime safety boundaries. | `docs/project/prj0000082-agent-execution-sandbox/prj0000082-agent-execution-sandbox.design.md`, `src/core/sandbox/SandboxedStorageTransaction.py` |
| Alternative seeds | Existing transaction managers offer reusable seams for side-effect capture and rollback-safe dry execution. | `src/transactions/MemoryTransactionManager.py`, `src/transactions/StorageTransactionManager.py`, `src/transactions/ProcessTransactionManager.py`, `src/transactions/ContextTransactionManager.py` |
| Determinism baseline | Core platform already positions deterministic runtime behavior as a design goal. | `docs/project/prj0000002/plan.md` |

## Constraints (Explicit)
- Must keep scope in shadow-mode-replay project artifacts and avoid broad runtime rewrites in this phase.
- Must prefer stdlib and existing transaction/context infrastructure over new frameworks.
- Must keep shadow execution side-effect-free for storage, process, and external I/O boundaries.
- Must support deterministic replay contracts from structured logs without requiring immediate full engine implementation.

## Options
### Option A - Inline Shadow Wrappers In Existing Runtime Path
**Approach**
- Add a "shadow" execution switch in existing task orchestration path.
- Wrap side-effect boundaries with existing transactions in dry behavior:
	- `StorageTransaction` queues but does not `acommit()`.
	- `ProcessTransaction` captures command intent/output but blocks process launch in shadow mode.
	- `MemoryTransaction` stages state in pending map and forces rollback.
- Emit canonical shadow log events directly from live path.

**Research coverage used**
- Literature review: replay and side-effect-free goals from project scope.
- Constraint mapping: reuse existing transaction managers and deterministic baseline.
- Stakeholder impact: touches live runtime path used by all agents.
- Risk enumeration: high blast radius due to hot path edits.
- Prior-art search: sandbox policy gates as precedent for side-effect blocking.

**Pros**
- Lowest additional abstraction count.
- Fastest path to first shadow run if runtime seams already exist.
- Maximum reuse of currently imported runtime modules.

**Cons**
- High regression risk in production execution path.
- Harder to guarantee shadow/live behavior separation long-term.
- Mixed concerns (execution and replay instrumentation in same flow).

**Stakeholder impact**
- High impact: @6code runtime modules, @5test regression matrix, @7exec operational validation.
- Medium impact: observability schema consumers.

**Failure modes (likelihood/impact)**
1. Shadow flag leak into live path causing skipped commits (M/H).
2. Incomplete side-effect interception (e.g., direct file or network calls) (H/H).
3. Log schema drift between live and replay events (M/M).

**Workspace evidence**
- `docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.project.md`
- `src/transactions/StorageTransactionManager.py`
- `src/transactions/ProcessTransactionManager.py`
- `src/transactions/MemoryTransactionManager.py`
- `src/core/sandbox/SandboxedStorageTransaction.py`

### Option B - ReplayEnvelope Event Model + Thin Orchestrator
**Approach**
- Introduce a dedicated replay contract (`ReplayEnvelope`) for deterministic task playback.
- Add a thin `ShadowReplayOrchestrator` that runs task steps from envelopes, not from direct live runtime hooks.
- Keep live execution path minimally touched: only emit `ReplayEnvelope`-compatible structured events.
- Determinism is enforced by replaying normalized inputs: task id, context lineage ids, timestamps (logical clock), tool call args, and side-effect intents.

**Research coverage used**
- Literature review: structured logging and project replay scope.
- Alternative enumeration: contract-first separation vs inline wrappers.
- Prior-art search: correlation ID middleware and transaction abstraction history.
- Constraint mapping: stdlib-first and existing transaction/context infra.
- Stakeholder impact: medium blast radius with explicit integration seams.
- Risk enumeration: schema/version and determinism drift risks.

**Pros**
- Clear separation between live execution and replay logic.
- Easier versioning and backward compatibility via envelope schema.
- Strongest long-term determinism posture without immediate large refactor.

**Cons**
- Requires upfront schema design and migration policy.
- Slightly higher initial design effort than Option A.
- Needs explicit adapter code at key integration points.

**Stakeholder impact**
- Medium impact: @3design contracts, @4plan sequencing, @5test replay fixtures.
- Low-medium impact: live runtime (emission adapters only).

**Failure modes (likelihood/impact)**
1. Envelope under-specification causes nondeterministic replay gaps (M/H).
2. Envelope schema version churn causes compatibility friction (M/M).
3. Emission overhead increases log volume unexpectedly (M/M).

**Workspace evidence**
- `docs/project/prj0000063/structured-logging.project.md`
- `docs/project/prj0000063/structured-logging.think.md`
- `backend/logging_config.py`
- `src/transactions/ContextTransactionManager.py`
- `docs/project/prj0000002/plan.md`

### Option C - Hybrid Snapshot + Event Replay Pipeline
**Approach**
- Record periodic in-memory state snapshots plus incremental event logs.
- Replay starts from nearest snapshot and replays forward through events.
- Shadow mode runs against snapshot clones and side-effect stubs.

**Research coverage used**
- Alternative enumeration: snapshot+event model for long sessions.
- Prior-art search: transaction manager and memory sync groundwork.
- Constraint mapping: deterministic replay requirement and medium budget.
- Stakeholder impact: larger impact on memory/state and storage handling.
- Risk enumeration: complexity and storage growth.

**Pros**
- Faster replay for long traces.
- Potentially better incident forensics with checkpointed state.
- Supports future time-travel debugging use cases.

**Cons**
- Highest complexity of the three options.
- Needs snapshot consistency guarantees across transaction boundaries.
- Larger storage footprint and retention policy burden.

**Stakeholder impact**
- High impact: core runtime state model, storage lifecycle, observability retention.
- Medium impact: operations and infra due to data growth.

**Failure modes (likelihood/impact)**
1. Snapshot/event mismatch yields invalid replay state (M/H).
2. Snapshot frequency tradeoff causes high storage cost or poor replay speed (H/M).
3. Snapshot capture introduces latent side effects or locking contention (M/M).

**Workspace evidence**
- `src/transactions/MemoryTransactionManager.py`
- `src/transactions/StorageTransactionManager.py`
- `docs/project/kanban.md`
- `docs/project/prj0000082-agent-execution-sandbox/prj0000082-agent-execution-sandbox.design.md`

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Delivery scope fit (S/M) | S | M | L |
| Reuse of existing infra | High | High | Medium |
| Deterministic replay fidelity | Medium | High | High |
| Operational risk | High | Medium | High |
| Blast radius | High | Medium | High |
| Evolvability | Medium | High | Medium |

## Recommendation
**Option B - ReplayEnvelope Event Model + Thin Orchestrator**

Rationale:
1. Best fit for requested small/medium scope: medium effort with strong replay guarantees.
2. Preserves live runtime stability by minimizing intrusive hot-path edits.
3. Reuses existing transaction/context primitives while introducing explicit deterministic contracts.
4. Provides a clean handoff to @3design for interface-first architecture decisions.

## Integration Points
1. `src/core/base/base_agent.py` and orchestration mixins: emit `ReplayEnvelope` events at task boundaries.
2. `src/transactions/ContextTransactionManager.py`: include `context_id`, `transaction_id`, `parent_id` lineage in event contract.
3. `src/transactions/StorageTransactionManager.py` + `src/core/sandbox/SandboxedStorageTransaction.py`: represent side-effect intents (`write/delete/mkdir`) as replayable records; no commit in shadow mode.
4. `src/transactions/ProcessTransactionManager.py`: capture subprocess intent and deterministic stdout/stderr replay fixtures.
5. `backend/logging_config.py` and structured logging conventions from prj0000063: map envelope fields to stable JSON keys with schema version.
6. Project lifecycle artifacts: `docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.design.md` should define schema/versioning and kill-switch behavior.

## Open Questions
1. What is the minimum required `ReplayEnvelope` field set to guarantee deterministic replay across all task types?
2. Should shadow mode block all external network calls by default, or allow an explicit per-agent allowlist similar to sandbox paths/hosts?
3. Where should logical clock generation live: runtime orchestrator, context transaction layer, or replay adapter?
4. What schema-version policy should govern backward compatibility for replay logs (`major/minor`, migration adapters, retention window)?
5. How should kill-switch behavior be defined when replay parser encounters unknown fields or malformed events?
6. Should replay fidelity target "functional equivalence" or "byte-identical event sequence" for v1 acceptance?

## Handoff
- Recommended option for @3design: **Option B - ReplayEnvelope Event Model + Thin Orchestrator**.
- This recommendation is intended as a medium-scope path that preserves runtime stability while enabling deterministic replay contracts.
