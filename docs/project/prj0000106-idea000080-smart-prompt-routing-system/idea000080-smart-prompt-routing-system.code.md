# idea000080-smart-prompt-routing-system - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-30_

## Implementation Summary
Implemented a minimal smart prompt routing slice under `src/core/routing` with deterministic guardrail-first routing,
bounded confidence threshold handling, deterministic tie-break behavior, fail-closed fallback taxonomy, and redacted
provenance telemetry.

Scope stayed narrow to new routing package files, AC-focused routing tests, and this project code artifact.

## Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-SPR-001 | src/core/routing/prompt_routing_facade.py | tests/core/routing/test_prompt_routing_facade.py::test_confidence_threshold_uses_classifier_when_above_threshold | PASS |
| AC-SPR-002 | src/core/routing/guardrail_policy_engine.py, src/core/routing/prompt_routing_facade.py | tests/core/routing/test_guardrail_precedence_contract.py::test_guardrail_precedence_overrides_classifier_candidates | PASS |
| AC-SPR-003 | src/core/routing/classifier_schema.py, src/core/routing/confidence_calibration.py, src/core/routing/prompt_semantic_classifier.py | tests/core/routing/test_prompt_routing_facade.py::test_confidence_threshold_uses_classifier_when_above_threshold, tests/core/routing/test_prompt_routing_facade.py::test_confidence_threshold_invokes_tie_break_when_below_threshold | PASS |
| AC-SPR-004 | src/core/routing/tie_break_resolver.py | tests/core/routing/test_tie_break_resolver.py::test_tie_break_is_deterministic_for_same_seed | PASS |
| AC-SPR-005 | src/core/routing/routing_fallback_policy.py, src/core/routing/fallback_reason_taxonomy.py, src/core/routing/prompt_routing_facade.py | tests/core/routing/test_prompt_routing_facade.py::test_fail_closed_on_schema_violation, tests/core/routing/test_prompt_routing_facade.py::test_fail_closed_on_classifier_provider_error, tests/core/routing/test_fail_closed_fallback_contract.py::test_fail_closed_on_tie_break_timeout | PASS |
| AC-SPR-006 | src/core/routing/shadow_mode_router.py, src/core/routing/prompt_routing_facade.py | tests/core/routing/test_shadow_active_parity.py::test_shadow_active_parity_for_same_policy_version | PASS |
| AC-SPR-007 | src/core/routing/tie_break_resolver.py, src/core/routing/prompt_routing_facade.py | tests/core/routing/test_tie_break_resolver.py::test_tie_break_timeout_raises_typed_error, tests/core/routing/test_fail_closed_fallback_contract.py::test_fail_closed_on_tie_break_timeout | PASS |
| AC-SPR-008 | src/core/routing/routing_telemetry_emitter.py | tests/core/routing/test_routing_telemetry_emitter.py::test_telemetry_includes_required_provenance_fields_and_redacts | PASS |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| src/core/routing/__init__.py | add | +23/-0 |
| src/core/routing/routing_models.py | add | +134/-0 |
| src/core/routing/request_normalizer.py | add | +47/-0 |
| src/core/routing/routing_policy_loader.py | add | +34/-0 |
| src/core/routing/policy_versioning.py | add | +33/-0 |
| src/core/routing/guardrail_policy_engine.py | add | +62/-0 |
| src/core/routing/prompt_semantic_classifier.py | add | +63/-0 |
| src/core/routing/classifier_schema.py | add | +53/-0 |
| src/core/routing/confidence_calibration.py | add | +34/-0 |
| src/core/routing/tie_break_resolver.py | add | +67/-0 |
| src/core/routing/fallback_reason_taxonomy.py | add | +54/-0 |
| src/core/routing/routing_fallback_policy.py | add | +64/-0 |
| src/core/routing/routing_telemetry_emitter.py | add | +52/-0 |
| src/core/routing/shadow_mode_router.py | add | +45/-0 |
| src/core/routing/prompt_routing_facade.py | add | +189/-0 |
| tests/core/routing/test_guardrail_precedence_contract.py | add | +43/-0 |
| tests/core/routing/test_prompt_routing_facade.py | add | +164/-0 |
| tests/core/routing/test_tie_break_resolver.py | add | +49/-0 |
| tests/core/routing/test_fail_closed_fallback_contract.py | add | +85/-0 |
| tests/core/routing/test_tie_break_fallback.py | add | +93/-0 |
| tests/core/routing/test_shadow_active_parity.py | add | +55/-0 |
| tests/core/routing/test_routing_telemetry_emitter.py | add | +57/-0 |
| docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.code.md | update | +57/-2 |

## Test Run Results
```
python -m pytest -q tests/core/routing/test_prompt_routing_facade.py tests/core/routing/test_fail_closed_fallback_contract.py tests/core/routing/test_guardrail_precedence_contract.py tests/core/routing/test_tie_break_resolver.py tests/core/routing/test_tie_break_fallback.py tests/core/routing/test_shadow_active_parity.py tests/core/routing/test_routing_telemetry_emitter.py
11 passed in 3.38s

.venv\Scripts\ruff.exe check --fix src/core/routing tests/core/routing
All checks passed!

.venv\Scripts\ruff.exe check src/core/routing tests/core/routing
All checks passed!

.venv\Scripts\ruff.exe check --select D src/core/routing tests/core/routing
All checks passed!

python -m mypy src/core/routing
Success: no issues found in 15 source files

python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
12 passed in 1.37s
```

## Deferred Items
none
