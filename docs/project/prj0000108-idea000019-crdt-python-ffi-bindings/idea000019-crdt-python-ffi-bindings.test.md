# idea000019-crdt-python-ffi-bindings - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-31_

## Test Plan
- Objective: define deterministic red-phase selectors and expected failing contracts that force real CRDT FFI behavior implementation in @6code.
- Scope source: `idea000019-crdt-python-ffi-bindings.design.md` and `idea000019-crdt-python-ffi-bindings.plan.md`.
- Red-phase rule: failing evidence is valid only when failure is assertion/behavioral mismatch. `ImportError`, `AttributeError`, or existence-only passes are rejected as weak evidence.
- Weak-test gate: unresolved weak-test findings block handoff.

## Branch Validation
- Expected branch: `prj0000108-idea000019-crdt-python-ffi-bindings`
- Observed branch: `prj0000108-idea000019-crdt-python-ffi-bindings`
- Result: PASS

## AC-to-Test Matrix
| AC ID | Contract Requirement | Test Case IDs |
|---|---|---|
| AC-CRDT-001 | Stable Python facade schema and envelope/path markers | TC-CRDT-001, TC-CRDT-002 |
| AC-CRDT-002 | Invalid payloads rejected with typed validation errors | TC-CRDT-003, TC-CRDT-004 |
| AC-CRDT-003 | Payload codec preserves semantic equivalence on round-trip | TC-CRDT-005 |
| AC-CRDT-004 | Deterministic merge output for identical inputs | TC-CRDT-006, TC-CRDT-007 |
| AC-CRDT-005 | Rust errors map to documented Python taxonomy | TC-CRDT-008, TC-CRDT-009 |
| AC-CRDT-006 | Observability includes required fields and redacts payload body | TC-CRDT-010, TC-CRDT-011 |
| AC-CRDT-007 | Feature flag controls FFI/fallback deterministically | TC-CRDT-012, TC-CRDT-013 |
| AC-CRDT-008 | Legacy-vs-FFI parity gate enforced before default cutover | TC-CRDT-014, TC-CRDT-015 |

## Deterministic Red-Phase Selector Order
Execute selectors in strict order. Stop on first non-behavioral failure signature and mark BLOCKED.

| Selector ID | Command | Contract Focus | Expected Red Failure Contract |
|---|---|---|---|
| S1 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_contract.py -k schema` | AC-CRDT-001 | Fails on missing/incorrect envelope fields (`request_id`, `merged_state`, `path`) or path value mismatch (`ffi`/`fallback`). |
| S2 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_bridge.py -k "ffi and envelope"` | AC-CRDT-001, AC-CRDT-007 | Fails on routing mismatch between bridge and FFI flag state; failure must assert wrong behavior, not missing symbol. |
| S3 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_validation.py -k shape` | AC-CRDT-002 | Fails because invalid payload shape/version is accepted or mis-categorized; must assert validation category contract. |
| S4 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_payload_codec.py -k round_trip` | AC-CRDT-003 | Fails on semantic drift after encode/decode (state/equivalence mismatch). |
| S5 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_merge_determinism.py` | AC-CRDT-004 | Fails when repeated merge over identical tuples yields non-identical merged output/conflict summary. |
| S6 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_error_mapping.py` | AC-CRDT-005 | Fails when Rust-side failures do not map to `validation`, `merge`, `internal` taxonomy. |
| S7 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_observability.py` | AC-CRDT-006 | Fails when required telemetry keys are absent or payload bodies leak in event data. |
| S8 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_feature_flag.py` | AC-CRDT-007 | Fails when `CRDT_FFI_ENABLED` does not deterministically select expected path. |
| S9 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_parity.py` | AC-CRDT-008 | Fails when corpus parity threshold is unmet or mismatch count exceeds gate allowance. |
| S10 | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_crdt_ffi_performance.py` | NFR-Performance | Fails when p95 bound or no-temp-file assertions are violated for FFI path. |

## Weak-Test Detection Gate (Blocking)
Reject handoff and keep `_Status: IN_PROGRESS_` if any of the following are observed:
- Tests pass against placeholder/stub logic (`pass`, constant return, or no merge behavior check).
- Assertions only verify existence/import/type checks without output semantics.
- Red evidence is `ImportError`, `AttributeError`, or collection error unrelated to behavior contracts.
- AC-to-test mapping has any AC without at least one concrete test case ID.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-CRDT-001 | Facade response includes stable envelope fields | `tests/test_crdt_ffi_contract.py` | RED_DEFINED |
| TC-CRDT-002 | Facade marks `path` correctly for FFI vs fallback | `tests/test_crdt_bridge.py` | RED_DEFINED |
| TC-CRDT-003 | Invalid payload shape rejected with validation category | `tests/test_crdt_ffi_validation.py` | RED_DEFINED |
| TC-CRDT-004 | Unsupported schema version rejected deterministically | `tests/test_crdt_ffi_validation.py` | RED_DEFINED |
| TC-CRDT-005 | Payload codec round-trip preserves semantic equivalence | `tests/test_crdt_payload_codec.py` | RED_DEFINED |
| TC-CRDT-006 | Identical tuple replay yields identical merge output | `tests/test_crdt_merge_determinism.py` | RED_DEFINED |
| TC-CRDT-007 | Conflict summary remains stable across reruns | `tests/test_crdt_merge_determinism.py` | RED_DEFINED |
| TC-CRDT-008 | Rust validation errors map to Python validation category | `tests/test_crdt_error_mapping.py` | RED_DEFINED |
| TC-CRDT-009 | Rust internal failures map without leaking internals | `tests/test_crdt_error_mapping.py` | RED_DEFINED |
| TC-CRDT-010 | Telemetry contains required keys (`duration_ms`, `outcome`, `path`) | `tests/test_crdt_ffi_observability.py` | RED_DEFINED |
| TC-CRDT-011 | Telemetry does not include raw payload body | `tests/test_crdt_ffi_observability.py` | RED_DEFINED |
| TC-CRDT-012 | Feature flag on uses FFI path deterministically | `tests/test_crdt_ffi_feature_flag.py` | RED_DEFINED |
| TC-CRDT-013 | Feature flag off routes to fallback deterministically | `tests/test_crdt_ffi_feature_flag.py` | RED_DEFINED |
| TC-CRDT-014 | Legacy-vs-FFI parity corpus mismatch stays under threshold | `tests/test_crdt_ffi_parity.py` | RED_DEFINED |
| TC-CRDT-015 | Parity gate blocks default cutover on threshold breach | `tests/test_crdt_ffi_parity.py` | RED_DEFINED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| BRANCH-GATE | PASS | expected=observed (`prj0000108-idea000019-crdt-python-ffi-bindings`) |
| RED-SELECTOR-DEFINITION | PASS | S1..S10 deterministic order and failure contracts recorded |
| WEAK-TEST-GATE | PASS | Blocking criteria defined and tied to handoff status |
| DOCS-POLICY | PASS | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed` |

## Unresolved Failures
- None at artifact-definition stage.

## Handoff Summary for @6code
- Status: READY_FOR_IMPLEMENTATION_CONTRACTS.
- Required first action in @6code: implement behavior required by S1 -> S10 contracts; do not bypass weak-test gate with existence-only changes.
