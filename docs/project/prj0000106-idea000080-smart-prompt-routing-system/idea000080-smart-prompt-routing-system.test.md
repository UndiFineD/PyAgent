# idea000080-smart-prompt-routing-system - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-30_

## Test Plan
Scope: project-scoped @5test red-phase specification after @4plan completion for prj0000106.

Approach:
1. Define deterministic red selectors per AC and planned task IDs.
2. Define expected failure contracts that must fail on missing/incorrect behavior, not import/symbol absence.
3. Enforce weak-test detection gate before any @6code handoff.
4. Keep artifacts and commands within prj0000106 boundary.

Deterministic red selector policy:
- Test selectors are fixed and map 1:1 to AC IDs.
- Red failures must be assertion-level behavior mismatches (for example: route mismatch, precedence violation, missing fallback reason), never placeholder/import-only checks.
- If a selector fails by ImportError/AttributeError, the selector is considered invalid for handoff and must be corrected by @5test first.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-SPR-001 | Facade returns decision or explicit fail-closed fallback envelope | tests/core/routing/test_prompt_routing_facade.py | PLANNED_RED |
| TC-SPR-002 | Fail-closed fallback contract on injected fault modes | tests/core/routing/test_fail_closed_fallback_contract.py | PLANNED_RED |
| TC-SPR-003 | Guardrail precedence over classifier and tie-break outputs | tests/core/routing/test_guardrail_precedence_contract.py | PLANNED_RED |
| TC-SPR-004 | Guardrail engine policy decision determinism and deny reasons | tests/core/routing/test_guardrail_policy_engine.py | PLANNED_RED |
| TC-SPR-005 | Classifier schema validity and confidence range bounds | tests/core/routing/test_classifier_schema.py | PLANNED_RED |
| TC-SPR-006 | Confidence calibration boundary behavior | tests/core/routing/test_confidence_calibration.py | PLANNED_RED |
| TC-SPR-007 | Tie-break deterministic replay contract | tests/core/routing/test_tie_break_resolver.py | PLANNED_RED |
| TC-SPR-008 | Tie-break timeout bound and timeout reason emission | tests/core/routing/test_tie_break_timeout.py | PLANNED_RED |
| TC-SPR-009 | Fallback reason taxonomy is explicit and stable | tests/core/routing/test_fallback_reason_taxonomy.py | PLANNED_RED |
| TC-SPR-010 | Shadow vs active parity for same input and policy version | tests/core/routing/test_shadow_active_parity.py | PLANNED_RED |
| TC-SPR-011 | Telemetry payload schema and required provenance fields | tests/core/routing/test_routing_telemetry_emitter.py | PLANNED_RED |
| TC-SPR-012 | Telemetry redaction blocks prompt/secret leakage | tests/core/routing/test_telemetry_redaction.py | PLANNED_RED |

## AC-to-Test Matrix
| AC ID | Contract | Test Case IDs |
|---|---|---|
| AC-SPR-001 | Route decision or explicit safe fallback always returned | TC-SPR-001, TC-SPR-002 |
| AC-SPR-002 | Guardrail precedence cannot be overridden | TC-SPR-003, TC-SPR-004 |
| AC-SPR-003 | Classifier schema and confidence bounds hold | TC-SPR-005, TC-SPR-006 |
| AC-SPR-004 | Tie-break result deterministic across replay | TC-SPR-007 |
| AC-SPR-005 | Fail-closed fallback on timeout/schema/provider faults | TC-SPR-002, TC-SPR-009 |
| AC-SPR-006 | Shadow and active parity for same inputs | TC-SPR-010 |
| AC-SPR-007 | Tie-break timeout bounded and reason recorded | TC-SPR-008 |
| AC-SPR-008 | Provenance telemetry schema and redaction validity | TC-SPR-011, TC-SPR-012 |

## Deterministic Red Selectors
1. python -m pytest -q tests/core/routing/test_prompt_routing_facade.py tests/core/routing/test_fail_closed_fallback_contract.py
2. python -m pytest -q tests/core/routing/test_guardrail_policy_engine.py tests/core/routing/test_guardrail_precedence_contract.py -k precedence
3. python -m pytest -q tests/core/routing/test_classifier_schema.py tests/core/routing/test_confidence_calibration.py
4. python -m pytest -q tests/core/routing/test_tie_break_resolver.py -k deterministic
5. python -m pytest -q tests/core/routing/test_tie_break_timeout.py
6. python -m pytest -q tests/core/routing/test_routing_fallback_policy.py tests/core/routing/test_fallback_reason_taxonomy.py
7. python -m pytest -q tests/core/routing/test_shadow_active_parity.py -k parity
8. python -m pytest -q tests/core/routing/test_routing_telemetry_emitter.py tests/core/routing/test_telemetry_redaction.py

Expected red failure contracts for @6code implementation:
1. Decision contract failures: assertion mismatch on final route envelope/fallback reason fields.
2. Precedence failures: assertion mismatch where guardrail winner is not final route.
3. Schema failures: assertion mismatch on invalid classifier payload acceptance/rejection.
4. Determinism failures: repeated run result mismatch under fixed config.
5. Timeout failures: elapsed time or reason code assertion mismatch.
6. Redaction failures: assertion mismatch when sensitive substrings are present in telemetry payload.

Invalid red signatures (must be fixed before handoff):
- ImportError
- ModuleNotFoundError
- AttributeError caused by missing test subject symbol names
- tests that only assert existence/import without behavior verification

## Validation Results
| ID | Result | Output |
|---|---|---|
| VG-SPR-001 | PASS | Branch gate validated: expected prj0000106-idea000080-smart-prompt-routing-system, observed prj0000106-idea000080-smart-prompt-routing-system |
| VG-SPR-002 | PASS | Deterministic red selectors and expected failure contracts defined for AC-SPR-001..AC-SPR-008 |
| VG-SPR-003 | PENDING | Red-phase selector execution evidence to be captured in subsequent @5test execution cycle |
| VG-SPR-004 | PENDING | Weak-test detection gate execution evidence to be captured alongside red selector run |
| VG-SPR-005 | PASS | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 12 passed in 2.04s |

## Unresolved Failures
No runtime red execution performed in this artifact-completion step; unresolved runtime evidence remains for VG-SPR-003 and VG-SPR-004.

## Weak-Test Detection Gate
Blocking command set (required before @6code handoff sign-off):
1. rg -n "assert\s+True|TODO: implement|is\s+not\s+None|isinstance\(" tests/core/routing
2. rg -n "pass\s*$|return\s+None\s*$" src/core/routing

Gate rule:
- Any unresolved weak-test hit blocks handoff.
- Missing AC-to-test mapping blocks handoff.

## Handoff Target
- Next agent: @6code
- Handoff state: READY_FOR_IMPLEMENTATION_CONTRACTS
- Note: @5test runtime red execution evidence remains a required follow-up gate before green validation sign-off.
