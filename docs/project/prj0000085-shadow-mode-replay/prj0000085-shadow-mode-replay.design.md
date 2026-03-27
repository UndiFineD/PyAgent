# prj0000085-shadow-mode-replay - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-27_

## Selected Option
Option B - ReplayEnvelope event model + thin orchestrator.

Rationale:
1. Keeps live execution stable by limiting live-path changes to deterministic event emission.
2. Provides explicit versioned contracts for replay compatibility and future migration.
3. Reuses existing transaction/context infrastructure for side-effect policy and lineage.

## Architecture
### Overview
This design introduces a new replay package at `src/core/replay/` that executes historical task traces in two controlled modes:
1. `shadow`: side-effect-free execution against transaction-backed stubs.
2. `replay`: deterministic reconstruction from previously emitted envelopes.

Live runtime responsibilities remain in existing orchestration paths. Live code emits normalized envelopes and appends them to a replay store. Replay code consumes only envelopes and deterministic fixtures.

### Implementable Module Layout
1. `src/core/replay/ReplayEnvelope.py`
	- Defines immutable event contract and schema validation.
	- Owns normalization and serialization helpers.
2. `src/core/replay/ShadowExecutionCore.py`
	- Executes one envelope under strict no-side-effect policy.
	- Integrates with existing transaction managers using dry behavior.
3. `src/core/replay/ReplayStore.py`
	- Persists and retrieves envelope streams by `session_id` and sequence.
	- Supports append, range read, and idempotent upsert semantics.
4. `src/core/replay/ReplayOrchestrator.py`
	- Coordinates envelope loading, ordering, deterministic clocking, and dispatch.
	- Produces replay summary and divergence results.
5. `src/core/replay/ReplayMixin.py`
	- Exposes agent-facing methods to emit envelopes and run shadow/replay workflows.
	- Keeps mixin-only orchestration logic out of core agent classes.
6. `src/core/replay/exceptions.py`
	- Defines replay-specific error taxonomy.
7. `src/core/replay/__init__.py`
	- Exports public symbols for stable imports.

### Component Responsibilities
1. Envelope contract layer:
	- Validate required fields.
	- Enforce deterministic field defaults.
	- Manage `schema_version` compatibility policy.
2. Store layer:
	- Durable append/read abstraction.
	- Ordering and dedup guarantees.
3. Execution layer:
	- Apply shadow policy.
	- Run deterministic replay step handlers.
4. Orchestration layer:
	- Build replay context, run sequence, collect metrics.
5. Integration layer (mixin):
	- Hook into existing agent lifecycle and logging emission points.

## Data Flow
### Flow A - Live Emission
1. Agent executes task step in normal runtime.
2. `ReplayMixin.emit_replay_envelope(...)` builds normalized `ReplayEnvelope`.
3. Envelope includes deterministic lineage fields from `ContextTransaction` and side-effect intent metadata.
4. `ReplayStore.append_envelope(...)` stores envelope in monotonic sequence.

### Flow B - Shadow Execution
1. Caller triggers `ReplayMixin.run_shadow_session(session_id=...)`.
2. `ReplayOrchestrator.load_session(...)` fetches ordered envelopes from store.
3. `ShadowExecutionCore.execute_envelope(...)` dispatches deterministic handler with dry/no-side-effect adapters.
4. Orchestrator records results, divergence, and policy violations.
5. Summary is returned without persistent side effects.

### Flow C - Deterministic Replay
1. Caller triggers `ReplayMixin.replay_session(session_id=...)`.
2. Orchestrator loads envelopes + optional fixture overrides.
3. Logical clock and deterministic random seed are bound from envelope metadata.
4. Replay runs sequentially by `sequence_no` and validates expected outputs.
5. Result object reports pass/fail, first divergence index, and diagnostics.

## Interfaces and Contracts
### `ReplayEnvelope.py`
Primary data contract (dataclass or pydantic model, frozen/immutable):

```python
class ReplayEnvelope:
		schema_version: str
		envelope_id: str
		session_id: str
		sequence_no: int
		event_type: str
		occurred_at: str
		logical_clock: int
		context_id: str
		transaction_id: str
		parent_transaction_id: str | None
		agent_name: str
		tool_name: str | None
		input_payload: dict
		output_payload: dict | None
		side_effect_intents: list[dict]
		checksum: str

		@classmethod
		def from_dict(cls, payload: dict) -> "ReplayEnvelope": ...
		def to_dict(self) -> dict: ...
		def validate(self) -> None: ...
```

Contract notes:
1. `schema_version` starts at `1.0`.
2. `sequence_no` is unique within `session_id`.
3. `checksum` is deterministic hash over canonicalized payload excluding checksum field.

### `ShadowExecutionCore.py`

```python
class ShadowExecutionCore:
		def __init__(
				self,
				*,
				memory_tx_factory,
				storage_tx_factory,
				process_tx_factory,
				context_tx_factory,
				block_network: bool = True,
		) -> None: ...

		async def execute_envelope(
				self,
				envelope: ReplayEnvelope,
				*,
				deterministic_seed: int | None = None,
		) -> "ReplayStepResult": ...

		async def _execute_tool_intent(
				self,
				envelope: ReplayEnvelope,
		) -> "ReplayStepResult": ...
```

Contract notes:
1. Never commits storage or process side effects in shadow mode.
2. Must rollback open transactions on exception paths.
3. Returns structured `ReplayStepResult` instead of raising for expected divergence.

### `ReplayStore.py`

```python
class ReplayStore:
		def __init__(self, *, root_path: Path, max_session_bytes: int = 50_000_000) -> None: ...

		async def append_envelope(self, envelope: ReplayEnvelope) -> None: ...
		async def append_many(self, envelopes: list[ReplayEnvelope]) -> None: ...
		async def load_session(self, session_id: str) -> list[ReplayEnvelope]: ...
		async def load_range(self, session_id: str, start: int, end: int) -> list[ReplayEnvelope]: ...
		async def delete_session(self, session_id: str) -> None: ...
		async def session_exists(self, session_id: str) -> bool: ...
```

Contract notes:
1. Storage format: JSONL per session for append efficiency.
2. Enforce monotonic `sequence_no`; reject duplicates.
3. Raise typed store exceptions on corruption/limit violations.

### `ReplayOrchestrator.py`

```python
class ReplayOrchestrator:
		def __init__(
				self,
				*,
				store: ReplayStore,
				shadow_core: ShadowExecutionCore,
		) -> None: ...

		async def replay_session(
				self,
				session_id: str,
				*,
				mode: str = "replay",
				stop_on_divergence: bool = True,
		) -> "ReplaySessionResult": ...

		async def run_shadow_session(self, session_id: str) -> "ReplaySessionResult": ...
		async def validate_session(self, session_id: str) -> "ReplayValidationResult": ...
```

Contract notes:
1. Orders envelopes by `sequence_no` before execution.
2. Fails fast on schema incompatibility or sequence gaps.
3. Supports full-run diagnostics when `stop_on_divergence=False`.

### `ReplayMixin.py`

```python
class ReplayMixin:
		async def emit_replay_envelope(
				self,
				*,
				event_type: str,
				input_payload: dict,
				output_payload: dict | None,
				side_effect_intents: list[dict] | None = None,
		) -> ReplayEnvelope: ...

		async def replay_session(self, session_id: str, *, stop_on_divergence: bool = True) -> "ReplaySessionResult": ...
		async def run_shadow_session(self, session_id: str) -> "ReplaySessionResult": ...
```

Contract notes:
1. Mixin depends on host agent attributes `self._replay_store` and `self._replay_orchestrator`.
2. Envelope emission must be side-effect-safe and non-blocking for live path.
3. Host agent initializes replay dependencies during boot.

### `exceptions.py`

```python
class ReplayError(Exception): ...
class ReplaySchemaError(ReplayError): ...
class ReplayStoreError(ReplayError): ...
class ReplayCorruptionError(ReplayStoreError): ...
class ReplaySequenceError(ReplayError): ...
class ReplayDivergenceError(ReplayError): ...
class ShadowPolicyViolation(ReplayError): ...
```

### `__init__.py`

```python
from .ReplayEnvelope import ReplayEnvelope
from .ReplayStore import ReplayStore
from .ShadowExecutionCore import ShadowExecutionCore
from .ReplayOrchestrator import ReplayOrchestrator
from .ReplayMixin import ReplayMixin
from .exceptions import (
		ReplayError,
		ReplaySchemaError,
		ReplayStoreError,
		ReplayCorruptionError,
		ReplaySequenceError,
		ReplayDivergenceError,
		ShadowPolicyViolation,
)
```

## Non-Functional Requirements
- Performance:
	- Envelope serialization overhead target: <= 3 ms p95 per emission on local dev baseline.
	- Replay throughput target: >= 100 envelopes/sec for JSONL-backed sessions of 1k envelopes.
- Security:
	- Shadow mode blocks external process/network side effects by default.
	- Replay data is treated as untrusted input; schema and checksum validation required.
	- Sensitive payload fields can be redacted before persistence via mixin hook.
- Determinism:
	- Replay uses logical clock and deterministic seed from envelope stream.
	- Sequence gaps or duplicate sequence numbers are hard failures.
- Testability:
	- All public interfaces are async and injectable for fixture-driven tests.
	- Store and core classes expose narrow seams for unit and integration tests.

## Test Scope (18 tests)
Target: 18 tests total across unit + integration, implemented by @5test/@6code.

1. Envelope round-trip `to_dict/from_dict` preserves canonical payload.
2. Envelope validation rejects missing required fields.
3. Envelope validation rejects non-monotonic logical clock values.
4. Envelope checksum mismatch raises `ReplaySchemaError`.
5. Store append + load returns ordered envelopes.
6. Store rejects duplicate `(session_id, sequence_no)`.
7. Store `load_range` enforces bounds and returns deterministic subset.
8. Store handles corrupted JSONL line with `ReplayCorruptionError`.
9. Store `delete_session` removes all persisted events.
10. Shadow core executes read-only envelope without side effects.
11. Shadow core blocks process side effect intents.
12. Shadow core rolls back transactions on execution exception.
13. Orchestrator fails on sequence gap with `ReplaySequenceError`.
14. Orchestrator `stop_on_divergence=True` halts at first divergence.
15. Orchestrator `stop_on_divergence=False` collects all divergences.
16. Mixin emission includes context lineage fields from active context transaction.
17. Mixin replay API delegates to orchestrator and returns session result.
18. End-to-end fixture replay reproduces deterministic output hash.

## Open Questions
1. v1 decision: functional-equivalence divergence checks are required; byte-identical stream checks are optional debug mode.
2. v1 decision: unknown envelope fields are ignored only when `schema_version` major matches; otherwise hard fail.
3. Follow-up for @4plan: confirm retention and pruning policy for session logs based on operational constraints.

## Handoff Readiness
This design is actionable for @4plan and provides concrete contracts for approximately 10 code files and 10 test files in downstream planning.
