# mypy-strict-enforcement - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-28_

## Selected Option
Option B - Progressive strict lane in stable `src/core` slices (blocking, scoped).

Rationale:
- Provides immediate enforcement (blocking) without full-repo blast radius.
- Aligns with deterministic-guard philosophy already used in repository structure tests.
- Keeps sprint scope realistic by constraining phase-1 to low-churn, contract-oriented modules.

## Problem Statement And Goals
Current repository mypy settings are permissive (`strict = False`, `ignore_errors = True`) and CI has no dedicated blocking mypy gate.
The goal of phase-1 is to introduce a strict, deterministic, low-risk enforcement lane that proves policy and pipeline behavior before broader rollout.

Phase-1 goals:
- Enforce strict mypy checks on a locked allowlist of stable `src/core` modules.
- Add a blocking CI check dedicated to strict lane validation.
- Add deterministic structure tests that prevent silent drift in lane scope and CI wiring.
- Preserve existing non-lane behavior (no repo-wide strict flip in this phase).

## Architecture
### Enforcement Topology
1. Legacy mypy behavior remains unchanged for broad repository checks.
2. A dedicated strict-lane mypy config governs phase-1 allowlisted modules only.
3. CI adds one blocking strict-lane check job/step that runs once per pipeline.
4. Structure/meta tests enforce lane integrity:
	 - strict-lane allowlist exactness,
	 - CI step existence and blocking semantics,
	 - deterministic strict-failure smoke behavior.

### Data Flow
1. Developer/CI invokes strict lane command.
2. mypy reads strict-lane config and checks only allowlisted modules.
3. CI fails on any lane violation.
4. Structure tests fail if lane is widened/narrowed or CI guard is removed/softened without explicit artifact updates.

## Phase-1 Locked Scope (Strict Lane Allowlist)
The following modules are the only phase-1 strict lane targets:

1. `src/core/audit/AuditEvent.py`
2. `src/core/audit/exceptions.py`
3. `src/core/resilience/CircuitBreakerConfig.py`
4. `src/core/resilience/CircuitBreakerState.py`
5. `src/core/resilience/exceptions.py`
6. `src/core/universal/exceptions.py`

Why this lane is low risk:
- Contract-heavy modules (exceptions, dataclasses/enums, serialization contracts).
- Minimal external I/O and orchestration dependencies.
- Lower churn relative to workflow/runtime orchestration paths.

## Interfaces & Contracts
### IFC-01 Strict Lane Config Contract
- File: `mypy-strict-lane.ini` (new file at repository root).
- Contract:
	- `strict = True` for lane execution.
	- `ignore_errors = False` for lane execution.
	- `files` contains exactly the 6 allowlisted modules above.
	- `show_error_codes = True` and `warn_unused_ignores = True` for actionable output.

### IFC-02 CI Blocking Contract
- File: `.github/workflows/ci.yml`.
- Contract:
	- Pipeline must execute a blocking strict-lane command:
		`python -m mypy --config-file mypy-strict-lane.ini`
	- Strict-lane check must not be marked `continue-on-error`.
	- Strict-lane check must run independently of test sharding (single execution per workflow run).

### IFC-03 Structure Guard Contract
- Files (planned):
	- `tests/structure/test_mypy_strict_lane_config.py` (new)
	- `tests/structure/test_ci_yaml.py` (extend) or sibling lane-specific CI structure test
- Contract:
	- Assert lane config file exists.
	- Assert exact allowlist content (no silent additions/removals).
	- Assert CI contains blocking strict-lane command.
	- Assert command does not contain non-blocking softeners.

### IFC-04 Strict Failure Smoke Contract
- Files (planned):
	- `tests/fixtures/mypy_strict_lane/bad_case.py` (new)
	- `tests/test_zzc_mypy_strict_lane_smoke.py` (new)
- Contract:
	- Running mypy strict against the known-bad fixture must return non-zero.
	- Test behavior must be deterministic and not depend on full-repo type state.

## Exact Implementation Changes (For Sprint)
1. Add `mypy-strict-lane.ini` with strict lane configuration and locked allowlist.
2. Leave existing permissive `mypy.ini` defaults intact in phase-1 (no global strict flip).
3. Add blocking strict-lane mypy execution in CI workflow.
4. Add/extend structure tests to enforce lane configuration and CI command invariants.
5. Add strict-failure smoke fixture and test.
6. Document lane expansion protocol (phase-2+ requires explicit artifact updates).

## Acceptance Criteria
| AC ID | Requirement | Verification | Owner Phase |
|---|---|---|---|
| AC-01 | Phase-1 strict lane allowlist is exactly the 6 locked modules | Structure test asserts exact list and order-insensitive equality | @5test |
| AC-02 | Dedicated strict-lane mypy config exists with strict enforcement enabled | Structure test parses `mypy-strict-lane.ini` keys/values | @5test |
| AC-03 | CI runs blocking strict-lane command once per workflow run | CI structure test parses `.github/workflows/ci.yml` | @5test |
| AC-04 | Strict lane fails on deterministic type violation | Smoke test executes strict mypy on bad fixture and expects non-zero | @5test/@7exec |
| AC-05 | Existing non-lane repository behavior is preserved in phase-1 | No global strict flip in `mypy.ini`; targeted regression check | @6code/@7exec |
| AC-06 | Design-to-plan traceability is complete for all lane contracts | `IFC-*` rows mapped to task seeds in traceability table | @3design/@4plan |

## Interface-To-Task Traceability (For @4plan Seeding)
| Interface/Contract | Task Seed ID | Planned Task Description |
|---|---|---|
| IFC-01 Strict Lane Config Contract | TSK-01 | Create `mypy-strict-lane.ini` with strict settings + locked `files` allowlist |
| IFC-02 CI Blocking Contract | TSK-02 | Add blocking CI strict-lane mypy step/job with no soft-fail flags |
| IFC-03 Structure Guard Contract | TSK-03 | Implement strict-lane config and CI structure tests |
| IFC-04 Strict Failure Smoke Contract | TSK-04 | Add smoke fixture + deterministic strict-failure test |
| AC-05 preservation requirement | TSK-05 | Validate no global mypy strict behavior change and update docs comments |
| Expansion governance | TSK-06 | Add lane-expansion protocol note to project docs for explicit change control |

## Rollback Plan
Rollback trigger conditions:
1. Strict-lane CI instability blocks merges for >2 consecutive runs due to non-deterministic issues.
2. Phase-1 lane surfaces unexpected high-churn dependency failures that exceed sprint budget.

Rollback actions:
1. Disable strict-lane CI step/job in one isolated change.
2. Retain structure tests but mark strict-lane command assertion as expected-missing only behind explicit temporary rollback marker.
3. Keep `mypy-strict-lane.ini` and fixture tests in place for re-enable readiness.
4. Create follow-up issue with root cause and re-enable criteria.

Rollback guardrail:
- Rollback must be explicit, reviewable, and time-bounded; no silent removal of strict-lane artifacts.

## Non-Goals
1. Enabling strict mypy for all `src/core/**` in this sprint.
2. Enabling strict mypy for full repository.
3. Refactoring high-churn orchestration/runtime modules to satisfy strictness now.
4. Replacing existing CI shard model.
5. Introducing new runtime features unrelated to type-safety guardrails.

## Policy Compliance
- Code of conduct policy respected: no harmful, exclusionary, or unsafe process requirements introduced.
- Naming standards alignment:
	- New module/file suggestions remain `snake_case`.
	- Test file naming follows existing `test_*.py` conventions.

## Open Questions For @4plan
1. Should strict-lane CI be a dedicated standalone job or an early step in existing `test` job (prefer standalone for isolation and visibility)?
2. Do we require a temporary `make`/task alias for local strict-lane invocation in this sprint, or defer to documentation-only command guidance?
3. For phase-2, should expansion prioritize `src/core/universal` contracts first or `src/core/audit` supporting modules first?
