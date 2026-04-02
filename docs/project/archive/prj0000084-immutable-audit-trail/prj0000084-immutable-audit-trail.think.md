# prj0000084-immutable-audit-trail - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-27_

## Root Cause Analysis
Current transaction and logging capabilities provide consistency and observability, but not
tamper evidence.

Root causes:
- Transaction managers focus on atomicity and rollback semantics, not immutable audit history.
- Logging paths are mutable streams without cryptographic linkage between events.
- There is no canonical audit module in `src/core/` to standardize event shape, hashing,
	append behavior, and verification.
- Audit intent exists in project and architecture artifacts, but implementation points are not
	yet concretely defined.

Evidence reviewed:
- `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.project.md`
- `docs/project/kanban.md`
- `docs/transaction-manager-architecture.md`
- `src/transactions/MemoryTransactionManager.py`
- `src/transactions/StorageTransactionManager.py`
- `src/transactions/ProcessTransactionManager.py`
- `src/transactions/ContextTransactionManager.py`
- `src/core/UnifiedTransactionManager.py`
- `backend/logging_config.py`
- `src/core/observability.py`
- `rust_core/src/utils/hash.rs` (prior-art for hashing intent, but not required in v1)

## Option Space

### Option A - Minimal Hash-Chain File Audit (Recommended)
Problem addressed:
- Deliver a testable immutable audit trail without broad refactors.

Approach:
- Add `src/core/audit/` with stdlib-only components:
	- `AuditRecord.py` dataclass for stable event schema.
	- `AuditHasher.py` (`hashlib.sha256`) for canonical hash-chain links.
	- `AuditWriter.py` append-only JSON Lines sink using atomic append discipline.
	- `AuditVerifier.py` linear chain validator for tests and operational checks.
- Integrate via lightweight call-sites in selected transaction boundaries (`begin`, `commit`,
	`rollback`, process start/fail/success, context enter/exit).

Research coverage and evidence:
- Literature review:
	- `docs/transaction-manager-architecture.md` (auditability principle)
	- `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.project.md`
- Prior-art search:
	- `docs/architecture/archive/agent_task_security_architecture.md` (immutable audit objective)
	- `rust_core/src/utils/hash.rs` (existing hash capability pattern)
- Constraint mapping:
	- Scope preference: small implementation in `src/core/audit/`
	- Dependency constraint: stdlib only for v1
	- Branch and scope boundary from project branch plan
- Stakeholder impact:
	- Core/runtime maintainers (transaction managers)
	- Security/compliance consumers (verification)
	- Test maintainers (new deterministic fixtures)
- Risk enumeration:
	- R1: Partial event coverage if only some transaction paths are instrumented (M/H)
	- R2: Concurrent append races corrupt ordering under high write contention (M/M)
	- R3: Canonicalization drift breaks verification across versions (L/H)

Pros:
- Smallest blast radius and fastest validation path.
- Fully testable with unit tests and fixture replay.
- No new external runtime dependencies.

Cons:
- Single-file append sink can become a throughput bottleneck.
- Requires strict schema versioning discipline to avoid verifier drift.

### Option B - Deep Transaction-Embedded Audit Mixin
Problem addressed:
- Enforce immutable logging uniformly across all transaction manager operations.

Approach:
- Introduce an audit mixin/base contract and wire every transaction manager to emit audit
	records in context manager entry/exit and commit/rollback paths.
- Potentially update sandboxes/wrappers so all side-effects are automatically audited.

Research coverage and evidence:
- Literature review:
	- `src/transactions/BaseTransaction.py`
	- `src/transactions/*TransactionManager.py`
- Prior-art search:
	- `src/core/sandbox/SandboxedStorageTransaction.py` (cross-cutting enforcement pattern)
- Constraint mapping:
	- Existing mixed sync/async transaction APIs make a universal hook non-trivial.
	- Need to preserve public behavior and avoid regressions in existing tests.
- Stakeholder impact:
	- Broad impact on core abstractions and downstream callers.
- Risk enumeration:
	- R1: Behavior regressions in commit/rollback semantics (M/H)
	- R2: Deadlocks or ordering side effects from synchronous audit writes in critical paths (M/M)
	- R3: Higher review and stabilization time delays delivery (H/M)

Pros:
- Strong consistency if fully implemented.
- Centralized enforcement model.

Cons:
- Larger scope and higher regression risk.
- Harder to deliver quickly as minimal testable increment.

### Option C - SQLite-Backed Audit Ledger (stdlib)
Problem addressed:
- Add queryability and integrity metadata with stronger local transactional semantics.

Approach:
- Implement `src/core/audit/` ledger with `sqlite3` table storing event payload, previous hash,
	current hash, sequence id, and timestamps.
- Add verifier that replays rows in sequence order.

Research coverage and evidence:
- Literature review:
	- `docs/transaction-manager-architecture.md` (persistence + monitoring principles)
- Prior-art search:
	- `src/core/UnifiedTransactionManager.py` (envelope concepts)
	- `tests/unit/test_McpSandbox.py` (sha256 validation patterns)
- Constraint mapping:
	- Still stdlib-only, but introduces operational concerns (file locks, migrations).
	- Scope may exceed "minimal" due to schema lifecycle and query API decisions.
- Stakeholder impact:
	- Security/reporting benefits from richer query surface.
	- Ops/test teams must handle DB lifecycle in local/dev/CI.
- Risk enumeration:
	- R1: Migration/versioning complexity earlier than needed (M/M)
	- R2: Lock contention under concurrent writes on Windows/Linux differences (M/M)
	- R3: More code before first value signal, slowing feedback loop (H/M)

Pros:
- Better structured querying than JSONL file scans.
- Good base for future reporting features.

Cons:
- More moving parts than minimal scope.
- Heavier test setup and compatibility matrix.

## Decision Matrix
| Criterion | Option A: Hash-Chain File | Option B: Embedded Mixin | Option C: SQLite Ledger |
|---|---|---|---|
| Delivery speed | High | Low | Medium |
| Scope fit (`src/core/audit/`, small) | High | Low | Medium |
| Testability (unit + fixture replay) | High | Medium | Medium |
| Regression risk in existing transaction behavior | Low-Medium | High | Medium |
| Operational complexity | Low | Medium | Medium-High |
| Extensibility to richer queries | Medium | Medium | High |

## Recommendation
**Option A - Minimal Hash-Chain File Audit**

Rationale:
- Best fit for a minimal, testable first increment.
- Aligns with explicit scope preference for `src/core/audit/` and stdlib-only implementation.
- Preserves existing transaction manager behavior while enabling immediate tamper-evidence checks.

## Integration Points
- `src/core/audit/` (new package): record model, hasher, writer, verifier.
- `src/transactions/MemoryTransactionManager.py`: emit begin/commit/rollback events.
- `src/transactions/StorageTransactionManager.py`: emit stage/commit/rollback and write targets.
- `src/transactions/ProcessTransactionManager.py`: emit start/success/failure/rollback.
- `src/transactions/ContextTransactionManager.py`: emit context lineage enter/exit markers.
- `src/core/UnifiedTransactionManager.py`: optional envelope-level emit for high-level orchestration.
- `backend/logging_config.py`: optional adapter to mirror audit event ids into structured logs.
- Tests:
	- Add focused unit tests under `tests/` for hash chaining and verification failure cases.
	- Add integration test covering one transaction happy path and one rollback path.

## Design Questions for @3design
1. What canonical event schema and required fields (actor, action, target, tx_id, context_id,
	 correlation_id) are mandatory for v1?
2. Which operations are "security-critical" in v1 and must be audited before optional coverage?
3. Should writer failures fail-closed (block operation) or fail-open (continue with error signal)?
4. What rotation/retention strategy preserves chain integrity across file boundaries?
5. How should concurrent writers serialize appends (process lock, thread lock, queue)?
6. Which verification command/API should be exposed for CI and runtime integrity checks?
