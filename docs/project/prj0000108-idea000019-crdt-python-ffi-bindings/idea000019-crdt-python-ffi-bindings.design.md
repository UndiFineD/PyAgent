# idea000019-crdt-python-ffi-bindings - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-31_

## Selected Option
Option B - integrate CRDT bindings into the existing `rust_core` PyO3 extension module.

Rationale:
1. Directly satisfies idea000019 by replacing subprocess CRDT calls with in-process Python FFI.
2. Reuses established repository build/release flow (`PyO3` + `maturin`) and avoids dual-wheel complexity.
3. Keeps architecture aligned with project policy: thin Python orchestration, Rust in performance-critical path.

Design lock:
- This design locks Option B for v1 implementation.
- Option A (subprocess hardening) is rejected for v1 because it misses the FFI objective.
- Option C (separate CRDT extension package) is deferred until contract stability warrants split packaging.

## Architecture
### High-level flow
1. Python caller invokes `src/core/crdt_bridge.py` through a stable merge facade.
2. Facade routes to `rust_core` FFI merge API by default (feature-gated fallback allowed during migration).
3. PyO3 boundary validates payload shape and converts Python objects into canonical Rust merge inputs.
4. `rust_core` delegates merge execution to CRDT library functions (no CLI subprocess hop).
5. Rust returns deterministic merge result plus metadata or typed error mapped to Python exception.
6. Python receives normalized result envelope and emits observability hooks for latency/outcome.

### Components and responsibilities
| Component | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `PythonCRDTMergeFacade` | Single Python entrypoint and migration switch control | Python merge request | Merge response/error |
| `RustCoreCRDTModule` | PyO3-exposed merge functions and conversion boundary | Canonical merge payload | `PyResult` response |
| `CRDTMergeEngine` | Pure Rust merge semantics and conflict resolution | CRDT document states/ops | Deterministic merged state |
| `CRDTPayloadCodec` | Canonical encoding/decoding and schema invariants | Python dict/json-like values | Rust typed merge structs |
| `CRDTErrorMapper` | Typed Rust-to-Python exception mapping | Rust error enum | Python exception class + message |
| `CRDTObservabilityHooks` | Structured latency/outcome counters and parity markers | Merge execution context | Telemetry events |

### Architecture constraints
1. Python-facing merge API must remain stable across migration wave (no breaking rename in v1).
2. No subprocess invocation is allowed in the primary path once FFI gate is enabled.
3. FFI boundary must reject invalid payload shapes before entering merge engine logic.
4. Rust panics may not cross FFI boundary; all failures must be converted to typed Python exceptions.
5. Merge behavior must remain parity-consistent with baseline corpus before subprocess retirement.

## Interfaces & Contracts
### Interface contracts
| Interface ID | Interface | Contract summary | Test hook |
|---|---|---|---|
| IFACE-CRDT-001 | `PythonCRDTMergeFacade.merge(payload: dict) -> dict` | Stable Python entrypoint; routes to FFI merge path with deterministic response envelope | AC-CRDT-001, AC-CRDT-007 |
| IFACE-CRDT-002 | `rust_core.merge_crdt(payload) -> PyResult[MergeEnvelope]` | PyO3 boundary validates input and returns typed result or typed error | AC-CRDT-002, AC-CRDT-005 |
| IFACE-CRDT-003 | `CRDTPayloadCodec.decode/encode(...)` | Canonical bidirectional conversion preserving semantic equivalence | AC-CRDT-003 |
| IFACE-CRDT-004 | `CRDTMergeEngine.merge(lhs, rhs, strategy) -> MergeOutput` | Deterministic merge semantics for equivalent input tuples | AC-CRDT-004, AC-CRDT-008 |
| IFACE-CRDT-005 | `CRDTErrorMapper.to_python(error) -> Exception` | Rust failures map to documented Python exception taxonomy | AC-CRDT-005 |
| IFACE-CRDT-006 | `CRDTObservabilityHooks.emit(context) -> None` | Emits required latency/outcome/parity fields without sensitive payload leakage | AC-CRDT-006 |

### Data contracts
| Data shape | Required fields | Notes |
|---|---|---|
| `CRDTMergeRequest` | `request_id`, `lhs_state`, `rhs_state`, `merge_strategy`, `schema_version` | `schema_version` gated at boundary |
| `CRDTMergeEnvelope` | `request_id`, `merged_state`, `conflict_summary`, `engine_version`, `path` | `path` includes `ffi` or `fallback` during migration |
| `CRDTMergeError` | `error_code`, `category`, `message`, `request_id` | `category` uses stable taxonomy (`validation`, `merge`, `internal`) |
| `CRDTMergeTelemetryEvent` | `request_id`, `path`, `duration_ms`, `outcome`, `parity_tag` | Must not include full CRDT payload bodies |

### Compatibility and rollout
- Keep `src/core/crdt_bridge.py` as canonical caller during migration; internals move from subprocess to FFI.
- Feature flag: `CRDT_FFI_ENABLED` controls progressive enablement and rollback.
- Subprocess fallback remains temporary and must be removed after parity and stability gates pass.

## Non-Functional Requirements
- Performance:
	- FFI merge path p95 latency improves by >= 40% over subprocess baseline on representative corpus.
	- FFI overhead (boundary conversion + call) p95 <= 15 ms excluding merge compute time.
	- Zero temporary-file I/O in default merge path.
- Security:
	- Input schema validation enforced at Python and Rust boundary.
	- Exception mapping must not leak internals (paths, secrets, raw panic payloads).
	- Telemetry emitted as redacted metadata only.
- Reliability:
	- Failure path is deterministic with typed error categories.
	- Fallback switch can be activated without code redeploy.
	- Panic-crossing boundary is prohibited by contract.
- Testability:
	- Contract tests for each interface ID.
	- Baseline parity corpus compares subprocess legacy vs FFI outputs.
	- Cross-platform matrix validation on Windows and Linux.

## Acceptance Criteria
| AC ID | Requirement | Verification hook |
|---|---|---|
| AC-CRDT-001 | Python merge facade exposes stable request/response schema for FFI path | Python contract tests on facade schema |
| AC-CRDT-002 | FFI boundary rejects invalid payloads with typed validation errors | Boundary negative tests |
| AC-CRDT-003 | Payload codec round-trip preserves semantic equivalence | Encode/decode parity tests |
| AC-CRDT-004 | Merge engine produces deterministic output for identical inputs | Determinism replay tests |
| AC-CRDT-005 | Rust errors map to documented Python exception taxonomy | Error mapping tests |
| AC-CRDT-006 | Observability event emits required fields and excludes sensitive payload body | Telemetry schema/redaction tests |
| AC-CRDT-007 | Feature flag controls FFI enablement and deterministic fallback selection | Feature-flag behavior tests |
| AC-CRDT-008 | FFI output parity against legacy subprocess corpus meets threshold before default cutover | Legacy-vs-FFI parity gate tests |

## Interface-to-Task Traceability
| Planned Task ID (@4plan) | Interface/Contract | Delivery expectation |
|---|---|---|
| T-CRDT-01 | IFACE-CRDT-001 | Implement stable Python merge facade and migration switch behavior |
| T-CRDT-02 | IFACE-CRDT-002 | Implement PyO3 merge entrypoint with typed boundary validation |
| T-CRDT-03 | IFACE-CRDT-003 | Implement canonical payload codec and schema version gate |
| T-CRDT-04 | IFACE-CRDT-004 | Refactor CRDT merge engine into library-callable deterministic API |
| T-CRDT-05 | IFACE-CRDT-005 | Implement Rust-to-Python exception mapper and taxonomy docs |
| T-CRDT-06 | IFACE-CRDT-006 | Implement observability hooks for latency/outcome/parity metrics |
| T-CRDT-07 | AC-CRDT-002, AC-CRDT-005 | Add negative-boundary and error-mapping contract tests |
| T-CRDT-08 | AC-CRDT-003, AC-CRDT-004 | Add codec round-trip and merge determinism tests |
| T-CRDT-09 | AC-CRDT-007 | Add feature-flag fallback and cutover behavior tests |
| T-CRDT-10 | AC-CRDT-008 + NFR performance hooks | Add legacy-vs-FFI parity and p95 performance gate checks |

## ADR Impact
- ADR update required: architecture shifts CRDT integration from subprocess boundary to in-process FFI boundary in existing `rust_core` module.
- ADR target: `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md`.
- ADR scope: module topology choice, rejected alternatives, migration constraints, validation/rollback triggers.

## Open Questions
Resolved for @4plan handoff readiness:
1. Namespace choice: expose CRDT API under existing `rust_core` module namespace with explicit CRDT function prefixing.
2. v1 contract: single stable merge entrypoint plus typed response envelope and error taxonomy.
3. rollout gate: default switch to FFI only after AC-CRDT-008 parity + NFR performance thresholds pass.
4. fallback window: subprocess path remains temporary migration fallback and is removed in follow-up hardening task.

No blocking open design questions remain for decomposition.
