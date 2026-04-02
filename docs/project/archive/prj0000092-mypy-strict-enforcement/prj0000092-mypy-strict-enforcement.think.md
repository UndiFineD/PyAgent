# mypy-strict-enforcement - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
- Global type checking is effectively disabled by configuration (`mypy.ini`: `strict = False`,
	`ignore_errors = True`).
- Current CI focuses on test sharding and does not run a dedicated blocking mypy gate
	(`.github/workflows/ci.yml`).
- The repository already uses deterministic structure/meta-tests for quality tooling contracts
	(examples: `tests/test_zzb_mypy_config.py`, `tests/structure/test_ci_yaml.py`).
- Strictness must start in `src/core/**` without large refactors in this sprint.

## Constraint Map
- Branch must remain `prj0000092-mypy-strict-enforcement`.
- Scope boundary from project overview: progressive rollout design for `src/core/**`, config/guardrail
	changes, and project artifacts only.
- No large refactors this sprint.
- Deterministic regression guard is required (CI and/or structure tests).
- Naming and conduct policies must remain aligned with:
	`docs/project/naming_standards.md` and `docs/project/code_of_conduct.md`.

## Prior Art References
- `docs/project/prj0000076/prj0000076.think.md` (idea and prioritization lineage for mypy strictness).
- `docs/project/prj0000075/prj0000075.think.md` (CI simplification decisions and deterministic gate
	mindset).
- `tests/test_zzb_mypy_config.py` (tooling meta-test pattern for type checker behavior).
- `tests/structure/test_ci_yaml.py` (structure-test pattern enforcing CI workflow invariants).
- `docs/architecture/archive/8testing-quality.md` (quality gate ordering and deterministic outcomes).

## Options
### Option A - Config-first soft launch for `src/core/**` (non-blocking)
Approach:
- Add targeted `mypy` section overrides for `src.core.*` in `mypy.ini`.
- Keep mypy execution non-blocking in CI for one sprint (collect trend data only).
- Add structure test that asserts presence of required `src.core.*` override keys.

Research coverage used:
- Literature review: `mypy.ini`, project overview, idea file.
- Alternative enumeration: compared soft vs balanced vs hard rollouts.
- Prior-art search: config/CI meta-tests and previous CI simplification project.
- Constraint mapping: no large refactor, branch/scope policy.
- Stakeholder impact: @5test low disruption; @6code low immediate pressure.
- Risk enumeration: listed below.

Tradeoffs:
- Delivery risk: Low.
- CI stability: High.
- Enforcement strength: Low to Medium (visibility without hard prevention).

Failure modes and risk-to-testability mapping:
| Failure Mode | Likelihood | Impact | Testability Strategy |
|---|---|---|---|
| Overrides added but ineffective due to mypy precedence | M | M | Structure test parses `mypy.ini` and validates section keys + target patterns |
| CI logs warnings but team ignores drift | H | M | Trend check in CI summary + threshold alert in follow-up task |
| False confidence from non-blocking mode | M | H | Add explicit "non-blocking" marker assertion in CI structure test |

### Option B - Progressive strict lane in stable `src/core` slices (blocking, scoped)
Approach:
- Keep global defaults permissive for non-core modules during rollout.
- Introduce blocking mypy checks for an explicit initial allowlist inside `src/core/**`
	(e.g., `src/core/workflow/**`, `src/core/resilience/**`, selected `src/core/universal/**` contracts).
- Add deterministic structure tests that enforce:
	1) targeted allowlist is present,
	2) mypy command for strict lane remains in CI,
	3) lane cannot silently broaden or disappear.

Research coverage used:
- Literature review: idea requirements and current CI/mypy state.
- Alternative enumeration: balanced rollout between signal and stability.
- Prior-art search: deterministic tests in `tests/test_zzb_mypy_config.py` and
	`tests/structure/test_ci_yaml.py`; CI philosophy in `docs/architecture/archive/8testing-quality.md`.
- Constraint mapping: sprint-ready without broad refactors.
- Stakeholder impact: moderate for @5test/@6code, clear gates for @7exec.
- Risk enumeration: listed below.

Tradeoffs:
- Delivery risk: Medium-Low.
- CI stability: Medium-High.
- Enforcement strength: Medium-High where enabled.

Failure modes and risk-to-testability mapping:
| Failure Mode | Likelihood | Impact | Testability Strategy |
|---|---|---|---|
| Selected strict slice includes high-churn modules causing unstable CI | M | H | Keep allowlist explicit and small; CI structure test validates allowlist exactness |
| Developers bypass strict lane by moving files outside allowlist | M | M | Structure test enforces protected path set and disallows removals without artifact update |
| mypy command changed to non-blocking or removed | L | H | CI YAML structure test asserts required blocking command exists |

### Option C - Hard strict gate for all `src/core/**` now (big-bang)
Approach:
- Turn on strict enforcement for entire `src/core/**` in one sprint and block CI on any type error.
- Remove permissive assumptions early and force immediate cleanup.

Research coverage used:
- Literature review: scope and current permissive config.
- Alternative enumeration: hard-enforcement endpoint.
- Prior-art search: historical CI simplification shows preference for stable focused gates.
- Constraint mapping: conflicts with "no large refactor" sprint constraint.
- Stakeholder impact: high across @5test, @6code, @7exec due to broad blast radius.
- Risk enumeration: listed below.

Tradeoffs:
- Delivery risk: High.
- CI stability: Low to Medium during migration.
- Enforcement strength: Very High.

Failure modes and risk-to-testability mapping:
| Failure Mode | Likelihood | Impact | Testability Strategy |
|---|---|---|---|
| Immediate CI red wall from legacy `Any`/Protocol gaps | H | H | Dry-run report first; baseline snapshot test before switching to blocking |
| Large refactor pressure spills beyond sprint scope | H | H | Scope test guarding touched paths + mandatory change-budget review |
| Emergency bypass weakens long-term policy trust | M | H | Policy test requiring explicit exception annotation and expiry |

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Delivery risk this sprint | 5/5 (lowest risk) | 4/5 | 1/5 (highest risk) |
| CI stability | 5/5 | 4/5 | 2/5 |
| Enforcement strength | 2/5 | 4/5 | 5/5 |
| Implementable without large refactor | 5/5 | 4/5 | 1/5 |
| Testability determinism | 3/5 | 5/5 | 3/5 |
| Overall sprint fitness | 3/5 | 5/5 | 1/5 |

## Recommendation
**Option B - Progressive strict lane in stable `src/core` slices (blocking, scoped).**

Rationale:
- It provides real enforcement now (not only observability) while keeping risk bounded.
- It aligns with prior-art quality strategy: deterministic gates and explicit CI invariants.
- It is practical for this sprint because it avoids full `src/core` refactoring and focuses on a curated,
	lower-churn allowlist.

## Deterministic Regression Guard Strategy (for chosen option)
1. Configuration guard:
	 Add a structure test that parses `mypy.ini` and asserts strict-lane sections exist for the initial
	 `src/core` allowlist and are configured as enforcing.
2. CI command guard:
	 Add a CI structure test that asserts a blocking mypy step exists for the strict lane and cannot be
	 downgraded to non-blocking behavior.
3. Scope guard:
	 Add a structure test that pins the first strict-lane target set. Any target removal/addition must update
	 project artifacts (explicit conscious change, not silent drift).
4. Signal guard:
	 Keep a deterministic smoke fixture with known type mismatch in an isolated temporary package to ensure the
	 strict lane fails as expected when broken.

## Stakeholder Impact
- @3design: define exact strict-lane module allowlist and mypy flags for phase 1.
- @4plan: break rollout into phase increments with change budget and rollback criteria.
- @5test: implement structure and CI guard tests first.
- @6code: remediate targeted lane typing issues only.
- @7exec: validate CI pass/fail behavior and rollback trigger.

## Open Questions
1. Which exact `src/core/**` subpaths are phase-1 strict-lane candidates with lowest churn?
2. Should phase-1 strictness use full `strict = True` semantics or an explicit strict flag subset?
3. Where should the strict-lane path allowlist live for best auditability: `mypy.ini` only, or duplicated in
	 structure test constants with cross-check?
4. What is the agreed error budget for expanding from phase-1 to phase-2 strict lanes?
