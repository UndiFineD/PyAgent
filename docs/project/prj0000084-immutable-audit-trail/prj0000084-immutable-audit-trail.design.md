# prj0000084-immutable-audit-trail - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-27_

## Selected Option
Option A - Minimal Hash-Chain File Audit (stdlib-only), constrained to a new
`src/core/audit/` package and zero required modifications to existing files for v1
module delivery.

Rationale:
- Smallest blast radius and fastest path to a usable immutable audit primitive.
- Produces a deterministic, testable append-and-verify API before integration work.
- Aligns with project constraint: keep changes isolated and avoid broad refactors.

## Architecture
High-level architecture (v1 package-only):

1. Event construction:
- Caller constructs an immutable `AuditEvent` with normalized fields and payload.

2. Chain hashing:
- `AuditHasher` canonicalizes event fields, combines with `previous_hash`, and computes
	SHA-256 `event_hash`.

3. Persistence boundary:
- `AuditTrailCore` appends a single JSONL line per event to an append-only audit file,
	ensuring each line embeds `previous_hash` and `event_hash`.

4. Verification:
- `AuditTrailCore.verify_file()` streams records in order, recomputes hashes, validates
	`previous_hash` linkage, and returns `AuditVerificationResult`.

5. Optional host integration:
- `AuditTrailMixin` provides a thin adapter API (`audit_emit_*`) that transaction/
	process/context managers can adopt later without changing this module's core logic.

Data flow:

`AuditEvent` -> `AuditHasher.canonical_event_bytes()` ->
`AuditHasher.compute_event_hash(previous_hash, event_bytes)` ->
`AuditTrailCore.append_event()` writes JSONL record ->
`AuditTrailCore.verify_file()` replays chain -> `AuditVerificationResult`.

Package/file map:
- `src/core/audit/__init__.py`: package exports.
- `src/core/audit/AuditEvent.py`: immutable event model + serialization helpers.
- `src/core/audit/AuditHasher.py`: canonicalization + SHA-256 functions.
- `src/core/audit/AuditTrailCore.py`: append/read/verify orchestration.
- `src/core/audit/AuditTrailMixin.py`: host integration convenience methods.
- `src/core/audit/AuditVerificationResult.py`: verifier result model.
- `src/core/audit/exceptions.py`: audit-specific exception hierarchy.

## Interfaces and Contracts
Module constants:
- `AUDIT_SCHEMA_VERSION = 1`
- `GENESIS_PREVIOUS_HASH = "0" * 64`

Core data types:

1) `AuditEvent` (`dataclass(frozen=True, slots=True)`)
- Fields:
	- `event_id: str` (UUID-like string; unique per event)
	- `event_type: str` (e.g., `transaction.commit`)
	- `occurred_at_utc: str` (ISO-8601 UTC string)
	- `actor_id: str | None`
	- `action: str`
	- `target: str | None`
	- `tx_id: str | None`
	- `context_id: str | None`
	- `correlation_id: str | None`
	- `payload: dict[str, object]`
	- `schema_version: int = AUDIT_SCHEMA_VERSION`
- Methods:
	- `to_canonical_dict(self) -> dict[str, object]`
	- `to_json_dict(self, previous_hash: str, event_hash: str, sequence: int) -> dict[str, object]`
	- `@classmethod from_json_dict(cls, data: dict[str, object]) -> "AuditEvent"`

2) `AuditHasher`
- Methods:
	- `canonical_event_bytes(event: AuditEvent) -> bytes`
	- `compute_event_hash(previous_hash: str, canonical_event_bytes: bytes) -> str`
	- `validate_hash_format(hash_value: str) -> bool`

3) `AuditVerificationResult` (`dataclass(frozen=True, slots=True)`)
- Fields:
	- `is_valid: bool`
	- `total_events: int`
	- `validated_events: int`
	- `first_invalid_sequence: int | None`
	- `error_code: str | None`
	- `error_message: str | None`
	- `last_valid_hash: str | None`

4) `AuditTrailCore`
- Constructor:
	- `__init__(self, audit_file_path: str, *, fail_closed: bool = True) -> None`
- Methods:
	- `append_event(self, event: AuditEvent) -> str`
	- `append_event_dict(self, *, event_type: str, action: str, payload: dict[str, object], actor_id: str | None = None, target: str | None = None, tx_id: str | None = None, context_id: str | None = None, correlation_id: str | None = None, occurred_at_utc: str | None = None, event_id: str | None = None) -> str`
	- `iter_records(self) -> list[dict[str, object]]`
	- `verify_file(self) -> AuditVerificationResult`
	- `get_last_hash(self) -> str`
	- `get_last_sequence(self) -> int`

5) `AuditTrailMixin`
- Required host hook:
	- `_get_audit_trail_core(self) -> AuditTrailCore | None`
- Convenience methods:
	- `audit_emit_event(self, *, event_type: str, action: str, payload: dict[str, object], target: str | None = None, tx_id: str | None = None, context_id: str | None = None, correlation_id: str | None = None) -> str | None`
	- `audit_emit_success(self, action: str, payload: dict[str, object]) -> str | None`
	- `audit_emit_failure(self, action: str, payload: dict[str, object]) -> str | None`

6) `exceptions.py`
- `class AuditTrailError(Exception)`
- `class AuditSerializationError(AuditTrailError)`
- `class AuditChainLinkError(AuditTrailError)`
- `class AuditIntegrityError(AuditTrailError)`
- `class AuditPersistenceError(AuditTrailError)`

Behavior contracts:
- Append-only contract: existing lines are never rewritten by module APIs.
- Determinism contract: canonical bytes for equivalent events are identical.
- Linkage contract: for sequence `n > 1`, `previous_hash[n] == event_hash[n-1]`.
- Verification contract: first detected defect halts validation and returns structured
	failure in `AuditVerificationResult`.
- Failure policy contract: `fail_closed=True` raises on write/serialization errors;
	`fail_closed=False` returns without raising only for mixin convenience paths.

## Test Scope for @4plan
Target test count: 18

1. `AuditEvent` canonical dict contains required keys and schema version.
2. Canonical dict ordering remains stable across equivalent payload insertion orders.
3. `AuditHasher.canonical_event_bytes` is deterministic for same input.
4. `compute_event_hash` returns 64-char lowercase hex string.
5. Genesis append uses `GENESIS_PREVIOUS_HASH`.
6. Second append links `previous_hash` to first `event_hash`.
7. `append_event_dict` produces same hash as explicit `AuditEvent` equivalent.
8. `iter_records` preserves append order.
9. `verify_file` passes on valid 3-event chain.
10. `verify_file` fails when middle record payload is tampered.
11. `verify_file` fails when `previous_hash` link is broken.
12. `verify_file` fails on malformed hash format.
13. `verify_file` fails on malformed JSON line.
14. Empty file verification behavior is explicit and deterministic (valid empty chain).
15. `get_last_hash` returns genesis hash for empty file and latest for populated file.
16. `fail_closed=True` raises `AuditPersistenceError` on unwritable file.
17. `AuditTrailMixin.audit_emit_event` returns `None` when no core is configured.
18. Exception hierarchy catches (`AuditTrailError`) and preserves specific subclass types.

## Non-Functional Requirements
- Performance:
	- Append path should remain O(1) per event excluding file system latency.
	- Verification path is O(n) with single-pass stream semantics.
	- Canonicalization/hashing must use Python stdlib only (`json`, `hashlib`).
- Security:
	- Hashchain tamper-evidence is mandatory; each record binds to its predecessor.
	- Canonical serialization must not include nondeterministic fields.
	- Verification errors must include precise sequence index for forensic triage.
- Testability:
	- All core APIs deterministic and unit-testable without external services.
	- Test fixtures use temporary files only; no global state required.
	- Public contracts include explicit exception classes for assertion clarity.
- Compatibility:
	- Python stdlib-only implementation, no third-party dependencies in v1.
	- Keep existing runtime modules unchanged in this design phase.

## Open Questions
1. Default write policy in production integration: fail-closed vs fail-open per subsystem.
2. Rotation strategy that preserves continuity (`next_file_genesis_hash` convention).
3. Minimum mandatory audited operations for first integration wave.
4. Whether verifier should support partial-window verification in addition to full replay.
