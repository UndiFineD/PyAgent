# idea000015-specialized-agent-library - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-31_

## Test Plan
Red-phase contracts are defined for Chunk A and Chunk B interfaces from the plan, with deterministic selector order and failure signatures that must represent missing behavior rather than import-only or existence-only checks.

Scope for this @5test package:
1. Define executable red selectors for T-SAL-001..T-SAL-008 and T-SAL-011..T-SAL-016.
2. Specify expected failing contracts that @6code must satisfy in green phase.
3. Enforce weak-test gate and AC-to-test traceability as blocking criteria before handoff.

Out of scope for this artifact step:
1. Production implementation changes.
2. Full green execution sign-off.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-SAL-001 | Descriptor schema valid/invalid resolution with typed reasons | tests/agents/specialization/test_specialization_registry.py | PLANNED_RED |
| TC-SAL-002 | Contract major-version gate rejects unsupported versions | tests/agents/specialization/test_contract_versioning.py | PLANNED_RED |
| TC-SAL-003 | Adapter mapping determinism under identical descriptor/context input | tests/agents/specialization/test_specialized_agent_adapter.py | PLANNED_RED |
| TC-SAL-004 | Manifest-to-request parity consistency across fixture corpus | tests/agents/specialization/test_manifest_request_parity.py | PLANNED_RED |
| TC-SAL-005 | Capability policy deny-by-default and immutable evidence fields | tests/agents/specialization/test_capability_policy_enforcer.py | PLANNED_RED |
| TC-SAL-006 | Core binding accepts valid targets and fail-closes unresolved targets | tests/agents/specialization/test_specialized_core_binding.py | PLANNED_RED |
| TC-SAL-007 | Fallback policy determinism for schema/policy/timeout faults | tests/agents/specialization/test_fault_injection_fallback.py | PLANNED_RED |
| TC-SAL-008 | Telemetry bridge emits required redacted provenance fields | tests/agents/specialization/test_telemetry_redaction.py | PLANNED_RED |
| TC-SAL-009 | Telemetry schema continuity and correlation enforcement | tests/agents/specialization/test_specialization_telemetry_bridge.py | PLANNED_RED |
| TC-SAL-010 | Universal shell feature-flag path preserves baseline behavior | tests/core/universal/test_universal_agent_shell_specialization_flag.py | PLANNED_RED |

## AC-to-Test Matrix (Blocking)
| AC ID | Contract Requirement | Test Case IDs |
|---|---|---|
| AC-SAL-001 | Registry resolves valid descriptors and rejects invalid schema with typed reason | TC-SAL-001 |
| AC-SAL-002 | Adapter mapping is deterministic for identical inputs | TC-SAL-003 |
| AC-SAL-003 | Unauthorized capabilities are denied by default with policy evidence | TC-SAL-005 |
| AC-SAL-004 | Core binding rejects unresolved targets and accepts valid bindings | TC-SAL-006 |
| AC-SAL-005 | Fallback triggers on schema/timeouts/policy faults with fail-closed result | TC-SAL-007 |
| AC-SAL-006 | Telemetry payload includes required redacted provenance fields | TC-SAL-008, TC-SAL-009 |
| AC-SAL-007 | Major-version incompatibility blocked pre-execution | TC-SAL-002 |
| AC-SAL-008 | Manifest intent parity with shell request across releases | TC-SAL-004 |

## Deterministic Red-Phase Selectors
Execution order is fixed to minimize cascading noise and isolate contract layers.

1. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_registry.py -k "resolve or schema"
2. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_contract_versioning.py
3. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialized_agent_adapter.py -k "deterministic or replay"
4. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_manifest_request_parity.py
5. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_capability_policy_enforcer.py -k "allow or deny"
6. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialized_core_binding.py
7. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_fault_injection_fallback.py -k "timeout or policy or schema"
8. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_telemetry_redaction.py
9. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_telemetry_bridge.py
10. c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/core/universal/test_universal_agent_shell_specialization_flag.py

## Expected Failing Contracts (Red Phase)
Allowed red failures must be behavior-contract failures only.

| Selector ID | Expected red signature | Forbidden red signature | @6code green expectation |
|---|---|---|---|
| S1 | AssertionError for schema validation mismatch or incorrect typed reason code | ImportError, ModuleNotFoundError, AttributeError-only | Implement schema + typed reason taxonomy so assertion path passes |
| S2 | AssertionError for unsupported major version not rejected deterministically | ImportError, AttributeError-only | Enforce major-version gate before adapter/runtime execution |
| S3 | AssertionError for non-deterministic request payload fields | ImportError, AttributeError-only | Ensure pure deterministic mapping for identical inputs |
| S4 | AssertionError for manifest/request parity drift | ImportError, AttributeError-only | Align adapter serialization with manifest intent contract |
| S5 | AssertionError for missing deny-by-default behavior or absent policy evidence fields | ImportError, AttributeError-only | Enforce deny-by-default + immutable evidence |
| S6 | AssertionError for unresolved core target not fail-closing | ImportError, AttributeError-only | Bind valid core targets and fail-close unresolved paths |
| S7 | AssertionError for non-deterministic or non-fail-closed fallback | ImportError, AttributeError-only | Implement deterministic fallback taxonomy with no unauthorized side effects |
| S8 | AssertionError for missing redaction or missing required provenance fields | ImportError, AttributeError-only | Emit telemetry with required fields and secret redaction |
| S9 | AssertionError for correlation continuity/schema invariants | ImportError, AttributeError-only | Preserve correlation and schema invariants across emissions |
| S10 | AssertionError for incorrect feature-flag gating or baseline regression | ImportError, AttributeError-only | Gate specialization path strictly behind validated flag + policy preconditions |

## Weak-Test Detection Gate (Blocking)
Any of the findings below blocks handoff to @6code until tests are strengthened:
1. Test passes with stub or placeholder implementation (for example pass, return None, unconditional default object).
2. Test only verifies import/existence/isinstance without behavioral assertions.
3. Test only asserts no exception is raised.
4. Test uses unconditional assert True or TODO placeholders.

Weak-test gate procedure:
1. Run selectors in deterministic order.
2. Inspect failure signatures and confirm behavior-contract assertion failures.
3. Reject and revise tests if failures are import/existence-only or if stubs satisfy assertions.
4. Record accepted red evidence in Validation Results before handoff.

## Validation Results
| ID | Result | Output |
|---|---|---|
| S1-S10 | PENDING_RED_EXECUTION | Deterministic selector list defined; execution evidence pending in current cycle |
| AC Matrix | PASS | AC-SAL-001..AC-SAL-008 each map to at least one concrete test case |
| Weak-test gate | PASS (policy defined) | Blocking criteria documented; enforcement required during selector run |
| Docs policy gate | PASS | c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 12 passed in 2.57s |

## Unresolved Failures
1. Red selector execution evidence is not yet recorded in this artifact revision.
2. Green validation is blocked until @6code implementation exists and weak-test gate remains satisfied.