# universal-agent-shell - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-27_

## Overview
Deliver a TDD-first implementation roadmap for the Universal Agent Shell Facade defined in design, with deterministic routing behavior, single-fallback guarantees, and explicit contract validation.

## Scope & Chunking
- Single implementation chunk is selected because the design scope is constrained to 5 production files and focused contract tests.
- Chunk 001 target footprint:
  - Code files: `src/core/universal/UniversalIntentRouter.py`, `src/core/universal/UniversalCoreRegistry.py`, `src/core/universal/UniversalAgentShell.py`, `src/core/universal/exceptions.py`, `src/core/universal/__init__.py`
  - Test files: `tests/core/universal/test_universal_intent_router.py`, `tests/core/universal/test_universal_core_registry.py`, `tests/core/universal/test_universal_agent_shell.py`

## Acceptance Criteria
- `AC-01`: Router normalizes intent deterministically (`None`/empty -> `unknown`, casing normalized).
- `AC-02`: Router selects `core` only for allowlisted intents and `legacy` otherwise.
- `AC-03`: Registry supports register/resolve/list/has/unregister with strict contract checks.
- `AC-04`: Registry rejects duplicate registrations unless overwrite is explicitly introduced later.
- `AC-05`: Shell dispatches to core exactly when decision is core-eligible and resolver succeeds.
- `AC-06`: Shell falls back exactly once to legacy on recoverable core failures.
- `AC-07`: Shell raises non-recoverable contract/validation errors (no swallow behavior).
- `AC-08`: Shell emits route telemetry fields (`route`, `intent`, `fallback_reason`) without secret leakage.
- `AC-09`: Public facade exports are stable and importable from `src/core/universal/__init__.py`.
- `AC-10`: Validation suite passes for targeted module tests and lint/type checks on universal facade files.

## Implementation Order (TDD)
1. [ ] `T1` - Define exception hierarchy and error semantics first.
	- Files: `src/core/universal/exceptions.py`
	- Acceptance: `AC-07`
2. [ ] `T2` - Implement router dataclasses, normalization, and classification policy.
	- Files: `src/core/universal/UniversalIntentRouter.py`
	- Acceptance: `AC-01`, `AC-02`
3. [ ] `T3` - Implement core registry contract and O(1) resolution behavior.
	- Files: `src/core/universal/UniversalCoreRegistry.py`
	- Acceptance: `AC-03`, `AC-04`
4. [ ] `T4` - Implement shell orchestration (core path, single fallback guard, timeout handling, telemetry result).
	- Files: `src/core/universal/UniversalAgentShell.py`
	- Acceptance: `AC-05`, `AC-06`, `AC-07`, `AC-08`
5. [ ] `T5` - Implement package export surface and import contract.
	- Files: `src/core/universal/__init__.py`
	- Acceptance: `AC-09`
6. [ ] `T6` - Add and pass focused validation commands for unit tests and static checks.
	- Files: `tests/core/universal/test_universal_intent_router.py`, `tests/core/universal/test_universal_core_registry.py`, `tests/core/universal/test_universal_agent_shell.py`
	- Acceptance: `AC-10`

## Test Mapping (18 Tests)
| Test ID | Test File | Test Name | Covers AC |
|---|---|---|---|
| `TEST-01` | `tests/core/universal/test_universal_intent_router.py` | `test_normalize_intent_lowercases_known_value` | `AC-01` |
| `TEST-02` | `tests/core/universal/test_universal_intent_router.py` | `test_normalize_intent_none_returns_unknown` | `AC-01` |
| `TEST-03` | `tests/core/universal/test_universal_intent_router.py` | `test_classify_allowlisted_intent_prefers_core` | `AC-02` |
| `TEST-04` | `tests/core/universal/test_universal_intent_router.py` | `test_classify_non_allowlisted_intent_prefers_legacy` | `AC-02` |
| `TEST-05` | `tests/core/universal/test_universal_intent_router.py` | `test_classify_is_deterministic_for_identical_envelope` | `AC-01`, `AC-02` |
| `TEST-06` | `tests/core/universal/test_universal_core_registry.py` | `test_register_valid_factory_succeeds` | `AC-03` |
| `TEST-07` | `tests/core/universal/test_universal_core_registry.py` | `test_register_duplicate_intent_raises_core_registration_error` | `AC-04` |
| `TEST-08` | `tests/core/universal/test_universal_core_registry.py` | `test_resolve_registered_intent_returns_handler_with_execute` | `AC-03` |
| `TEST-09` | `tests/core/universal/test_universal_core_registry.py` | `test_resolve_missing_intent_raises_core_not_registered_error` | `AC-03` |
| `TEST-10` | `tests/core/universal/test_universal_core_registry.py` | `test_list_intents_returns_stable_tuple` | `AC-03` |
| `TEST-11` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_routes_allowlisted_intent_to_core` | `AC-05` |
| `TEST-12` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_routes_non_allowlisted_intent_to_legacy` | `AC-05` |
| `TEST-13` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_falls_back_on_registry_miss_once` | `AC-06` |
| `TEST-14` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_falls_back_on_core_execution_error` | `AC-06` |
| `TEST-15` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_falls_back_on_core_timeout` | `AC-06` |
| `TEST-16` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_raises_envelope_validation_error_for_invalid_envelope` | `AC-07` |
| `TEST-17` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_does_not_retry_fallback_when_legacy_dispatch_fails` | `AC-06`, `AC-07` |
| `TEST-18` | `tests/core/universal/test_universal_agent_shell.py` | `test_dispatch_result_includes_route_intent_and_fallback_reason` | `AC-08`, `AC-09` |

## AC Coverage Matrix
| AC | Covered by Tests |
|---|---|
| `AC-01` | `TEST-01`, `TEST-02`, `TEST-05` |
| `AC-02` | `TEST-03`, `TEST-04`, `TEST-05` |
| `AC-03` | `TEST-06`, `TEST-08`, `TEST-09`, `TEST-10` |
| `AC-04` | `TEST-07` |
| `AC-05` | `TEST-11`, `TEST-12` |
| `AC-06` | `TEST-13`, `TEST-14`, `TEST-15`, `TEST-17` |
| `AC-07` | `TEST-16`, `TEST-17` |
| `AC-08` | `TEST-18` |
| `AC-09` | `TEST-18` |
| `AC-10` | Validation Commands block |

## Handoff Package For @5test
- First chunk for immediate test authoring: `TEST-01` through `TEST-18` in listed file order.
- Required fixtures/mocks:
  - deterministic `TaskEnvelope` factory
  - async fake core handler factory with configurable outcome (`success`, `error`, `timeout`)
  - async fake legacy dispatcher with call counter
- Definition of done for @5test handoff:
  - 18 tests authored, named exactly as mapped, and green against completed implementation tasks `T1`-`T5`.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| `M1` | Error model implemented | `T1` | NOT_STARTED |
| `M2` | Router and registry implemented | `T2`, `T3` | NOT_STARTED |
| `M3` | Shell dispatch implemented | `T4` | NOT_STARTED |
| `M4` | Public exports stabilized | `T5` | NOT_STARTED |
| `M5` | Test suite and static validation green | `T6` | NOT_STARTED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/core/universal/test_universal_intent_router.py tests/core/universal/test_universal_core_registry.py tests/core/universal/test_universal_agent_shell.py
python -m mypy src/core/universal
python -m ruff check src/core/universal tests/core/universal
```
