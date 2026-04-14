# idea000019-crdt-python-ffi-bindings - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-31_

## Overview
Deliver Option B from design: move CRDT merge from subprocess execution into the existing `rust_core` PyO3 module while preserving a stable Python facade in `src/core/crdt_bridge.py`, feature-flagged migration control, deterministic parity checks, and rollback safety.

This plan is decomposed into two executable chunks sized for downstream flow:
1. Chunk A (interface + FFI core): ~10 code files and ~10 test files.
2. Chunk B (parity/perf cutover + fallback retirement): ~10 code files and ~10 test files.

## Scope Guardrails
- Expected branch: `prj0000108-idea000019-crdt-python-ffi-bindings`
- Allowed implementation scope for this roadmap:
	- Python bridge: `src/core/crdt_bridge.py`
	- Rust extension root: `rust_core/Cargo.toml`, `rust_core/src/lib.rs`
	- CRDT crate: `rust_core/crdt/Cargo.toml`, `rust_core/crdt/src/main.rs`, new `rust_core/crdt/src/lib.rs`
	- New rust_core CRDT module family (planned): `rust_core/src/crdt.rs`, `rust_core/src/crdt/*`
	- CRDT tests and parity gates under `tests/`
	- CI/build touchpoints if needed: `.github/workflows/ci.yml`
- Out of scope for this project phase:
	- Multi-package split (Option C)
	- Long-lived subprocess hardening as primary path (Option A)

## Chunk Plan

### Chunk A - FFI Contract and Core Integration (Target: @5test -> @6code)

#### Target Code Files (~10)
- `src/core/crdt_bridge.py`
- `rust_core/src/lib.rs`
- `rust_core/src/crdt.rs` (new)
- `rust_core/src/crdt/payload_codec.rs` (new)
- `rust_core/src/crdt/error_mapper.rs` (new)
- `rust_core/src/crdt/merge_engine.rs` (new)
- `rust_core/src/crdt/telemetry.rs` (new)
- `rust_core/crdt/src/lib.rs` (new)
- `rust_core/crdt/src/main.rs`
- `rust_core/crdt/Cargo.toml`

#### Target Test Files (~10)
- `tests/test_crdt_bridge.py`
- `tests/test_rust_crdt_merge.py`
- `tests/test_rust_core.py`
- `tests/test_crdt_ffi_contract.py` (new)
- `tests/test_crdt_ffi_validation.py` (new)
- `tests/test_crdt_payload_codec.py` (new)
- `tests/test_crdt_merge_determinism.py` (new)
- `tests/test_crdt_error_mapping.py` (new)
- `tests/test_crdt_ffi_feature_flag.py` (new)
- `tests/test_crdt_ffi_observability.py` (new)

#### Tasks
| Task ID | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|
| T-CRDT-001 | @5test | Add red-phase schema contract tests for stable Python facade request/response envelope and path markers. | `tests/test_crdt_ffi_contract.py`, `tests/test_crdt_bridge.py` | AC-CRDT-001 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_contract.py -k schema` |
| T-CRDT-002 | @6code | Refactor Python facade to route through FFI path with stable envelope while preserving fallback switch contract. | `src/core/crdt_bridge.py` | AC-CRDT-001, AC-CRDT-007 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_bridge.py tests/test_crdt_ffi_contract.py` |
| T-CRDT-003 | @5test | Add boundary negative tests for invalid payload shape/version and deterministic validation error categories. | `tests/test_crdt_ffi_validation.py` | AC-CRDT-002 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_validation.py` |
| T-CRDT-004 | @6code | Implement PyO3 CRDT entrypoint registration with strict input validation before merge execution. | `rust_core/src/lib.rs`, `rust_core/src/crdt.rs`, `rust_core/src/crdt/payload_codec.rs` | AC-CRDT-002 | `cargo test --manifest-path rust_core/Cargo.toml crdt` |
| T-CRDT-005 | @5test | Add codec round-trip tests for semantic equivalence across dict/json-like payload shapes. | `tests/test_crdt_payload_codec.py` | AC-CRDT-003 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_payload_codec.py` |
| T-CRDT-006 | @6code | Implement canonical payload codec and schema-version gates for Python->Rust->Python conversion path. | `rust_core/src/crdt/payload_codec.rs`, `rust_core/src/crdt.rs` | AC-CRDT-003 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_payload_codec.py` |
| T-CRDT-007 | @5test | Add determinism replay tests for identical input tuples and conflict-summary stability. | `tests/test_crdt_merge_determinism.py`, `tests/test_rust_crdt_merge.py` | AC-CRDT-004 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_merge_determinism.py` |
| T-CRDT-008 | @6code | Refactor CRDT merge engine to library-callable deterministic API and wire CLI to library function. | `rust_core/crdt/src/lib.rs`, `rust_core/crdt/src/main.rs`, `rust_core/src/crdt/merge_engine.rs` | AC-CRDT-004 | `cargo test --manifest-path rust_core/crdt/Cargo.toml` |
| T-CRDT-009 | @5test | Add Rust-error to Python-exception mapping contract tests across validation/merge/internal categories. | `tests/test_crdt_error_mapping.py` | AC-CRDT-005 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_error_mapping.py` |
| T-CRDT-010 | @6code | Implement typed error mapper with stable taxonomy and safe message redaction at FFI boundary. | `rust_core/src/crdt/error_mapper.rs`, `rust_core/src/crdt.rs` | AC-CRDT-005 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_error_mapping.py` |

### Chunk B - Observability, Parity Gates, and Cutover (Target: @5test -> @6code -> @7exec -> @8ql)

#### Target Code Files (~10)
- `src/core/crdt_bridge.py`
- `rust_core/src/crdt.rs`
- `rust_core/src/crdt/telemetry.rs`
- `rust_core/src/crdt/error_mapper.rs`
- `rust_core/src/crdt/merge_engine.rs`
- `rust_core/src/lib.rs`
- `rust_core/Cargo.toml`
- `rust_core/crdt/Cargo.toml`
- `.github/workflows/ci.yml` (if parity/perf gate integration required)
- `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md` (status/consequence closure in later stages)

#### Target Test Files (~10)
- `tests/test_crdt_ffi_observability.py`
- `tests/test_crdt_ffi_feature_flag.py`
- `tests/test_crdt_ffi_parity.py` (new)
- `tests/test_crdt_ffi_performance.py` (new)
- `tests/test_crdt_bridge.py`
- `tests/test_rust_crdt_merge.py`
- `tests/test_rust_core.py`
- `tests/test_crdt_ffi_validation.py`
- `tests/test_crdt_error_mapping.py`
- `tests/test_crdt_merge_determinism.py`

#### Tasks
| Task ID | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|
| T-CRDT-011 | @5test | Add telemetry schema and redaction tests for latency/outcome/parity events with no payload leakage. | `tests/test_crdt_ffi_observability.py` | AC-CRDT-006 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_observability.py` |
| T-CRDT-012 | @6code | Implement observability hooks for FFI path and ensure required fields emit on success/failure/fallback. | `rust_core/src/crdt/telemetry.rs`, `rust_core/src/crdt.rs`, `src/core/crdt_bridge.py` | AC-CRDT-006 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_observability.py` |
| T-CRDT-013 | @5test | Add deterministic feature-flag behavior tests for FFI enable/disable and fallback selection. | `tests/test_crdt_ffi_feature_flag.py` | AC-CRDT-007 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_feature_flag.py` |
| T-CRDT-014 | @6code | Implement feature-flag gate and deterministic fallback routing with explicit path markers in response envelope. | `src/core/crdt_bridge.py`, `rust_core/src/crdt.rs` | AC-CRDT-007 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_feature_flag.py tests/test_crdt_bridge.py` |
| T-CRDT-015 | @5test | Add legacy-subprocess vs FFI parity gate tests over representative corpus with threshold assertions. | `tests/test_crdt_ffi_parity.py`, `tests/test_crdt_bridge.py` | AC-CRDT-008 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_parity.py` |
| T-CRDT-016 | @6code | Implement parity harness integration and resolve divergences until threshold passes. | `src/core/crdt_bridge.py`, `rust_core/src/crdt/merge_engine.rs`, `rust_core/crdt/src/lib.rs` | AC-CRDT-008 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_parity.py tests/test_crdt_merge_determinism.py` |
| T-CRDT-017 | @5test | Add p95 performance gate tests for FFI path and no-temp-file assertions in default path. | `tests/test_crdt_ffi_performance.py`, `tests/test_crdt_bridge.py` | NFR-Performance | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_performance.py` |
| T-CRDT-018 | @6code | Tune conversion and merge path to meet p95 targets and remove temp-file dependency in default flow. | `src/core/crdt_bridge.py`, `rust_core/src/crdt/payload_codec.rs`, `rust_core/src/crdt/merge_engine.rs` | NFR-Performance | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_performance.py tests/test_crdt_bridge.py` |
| T-CRDT-019 | @7exec | Run cross-platform runtime validation and import/build smoke for rust_core + CRDT FFI flow. | `rust_core/Cargo.toml`, `.github/workflows/ci.yml`, runtime artifacts | AC-CRDT-008, NFR-Reliability | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_rust_core.py tests/test_crdt_bridge.py` |
| T-CRDT-020 | @8ql | Perform security/quality closure on boundary validation, error redaction, and fallback governance before cutover. | `src/core/crdt_bridge.py`, `rust_core/src/crdt/*`, `tests/test_crdt_ffi_validation.py`, `tests/test_crdt_error_mapping.py` | AC-CRDT-002, AC-CRDT-005, AC-CRDT-006 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_validation.py tests/test_crdt_error_mapping.py tests/test_crdt_ffi_observability.py` |

## AC to Task and Command Mapping
| AC ID | Requirement | Primary Tasks | Owner Sequence | Command Gate |
|---|---|---|---|---|
| AC-CRDT-001 | Stable Python merge facade schema | T-CRDT-001, T-CRDT-002 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_contract.py tests/test_crdt_bridge.py` |
| AC-CRDT-002 | Boundary validation with typed errors | T-CRDT-003, T-CRDT-004 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_validation.py` |
| AC-CRDT-003 | Codec semantic round-trip | T-CRDT-005, T-CRDT-006 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_payload_codec.py` |
| AC-CRDT-004 | Deterministic merge outputs | T-CRDT-007, T-CRDT-008 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_merge_determinism.py` |
| AC-CRDT-005 | Rust-to-Python error taxonomy mapping | T-CRDT-009, T-CRDT-010 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_error_mapping.py` |
| AC-CRDT-006 | Observability schema + redaction | T-CRDT-011, T-CRDT-012 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_observability.py` |
| AC-CRDT-007 | Feature-flag cutover and fallback control | T-CRDT-013, T-CRDT-014 | @5test -> @6code | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_feature_flag.py` |
| AC-CRDT-008 | Legacy-vs-FFI parity gate before default cutover | T-CRDT-015, T-CRDT-016, T-CRDT-019 | @5test -> @6code -> @7exec | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_parity.py tests/test_crdt_bridge.py` |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Chunk A red tests authored | T-CRDT-001,003,005,007,009 | PLANNED |
| M2 | Chunk A green implementation | T-CRDT-002,004,006,008,010 | PLANNED |
| M3 | Chunk B red tests authored | T-CRDT-011,013,015,017 | PLANNED |
| M4 | Chunk B green implementation | T-CRDT-012,014,016,018 | PLANNED |
| M5 | Runtime cross-platform validation | T-CRDT-019 | PLANNED |
| M6 | Security/quality closure and cutover readiness | T-CRDT-020 | PLANNED |

## Dependency Order
1. @5test creates red-phase selectors per task.
2. @6code implements minimal green changes to satisfy selectors.
3. @7exec validates runtime and cross-platform behavior.
4. @8ql closes security/quality gates.
5. @9git performs narrow staging and release handoff.

## Validation Commands
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_contract.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_validation.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_payload_codec.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_merge_determinism.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_error_mapping.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_feature_flag.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_observability.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_parity.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_performance.py
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```
