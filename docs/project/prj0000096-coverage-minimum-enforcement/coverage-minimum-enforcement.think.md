# coverage-minimum-enforcement - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
1. Enforcement drift: historical coverage workflow used effectively non-enforcing semantics (`--cov-fail-under=1` with soft-fail behavior), documented in prior-art analysis.
2. Current CI gap: active workflow runs sharded pytest without coverage flags, so `pyproject.toml` coverage thresholds are configured but not exercised in the blocking CI path.
3. Signal mismatch: configuration presence tests validate that coverage settings exist, but they do not assert that CI enforces a minimum threshold on merged results.
4. Governance coupling: workflow-count and CI-structure tests tightly constrain workflow layout; adding coverage enforcement must fit existing `ci.yml` contract rather than reintroducing retired workflow sprawl.
5. Delivery risk: hard jump to a high threshold can create broad red-wall failures if current measured baseline is below target, so rollout method is the key architecture decision.

Evidence (literature + constraints + prior-art):
- `pyproject.toml` (`[tool.coverage.report] fail_under = 30` exists)
- `.github/workflows/ci.yml` (no `--cov` invocation in active jobs)
- `tests/test_coverage_config.py` (presence/config tests only)
- `tests/structure/test_ci_yaml.py` and `tests/ci/test_workflow_count.py` (CI contract and workflow-count constraints)
- `docs/project/prj0000075/prj0000075.think.md` (historical `quality.yml` non-enforcing threshold context)
- `docs/project/prj0000026/prj0000026.git.md` (original introduction of coverage config + legacy quality workflow)
- `docs/architecture/archive/8testing-quality.md` (deterministic quality-gate expectations)

## Options
### Option A - Fixed Baseline Gate Now (single global threshold)
Approach:
1. Add one blocking coverage execution path in `ci.yml` that produces a merged coverage result and fails under a fixed threshold (for this project, baseline target 70).
2. Keep threshold source-of-truth in `pyproject.toml` (`[tool.coverage.report] fail_under`) and make CI explicitly honor it.
3. Add/adjust structure tests to assert that CI contains a blocking coverage gate.

Research coverage used (5/6):
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Risk enumeration

Workspace evidence:
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/structure/test_ci_yaml.py`
- `tests/test_coverage_config.py`

Likely files/workflows to touch:
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/structure/test_ci_yaml.py`
- `tests/test_coverage_config.py`
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.design.md`

Pros:
- Strongest immediate non-regression signal.
- Simple policy and low ongoing governance overhead.
- Fastest path to a clear blocking quality gate.

Cons:
- Highest short-term CI failure risk if real baseline < threshold.
- Can force rushed test additions or scope creep under delivery pressure.
- Less flexible for teams/components with uneven test maturity.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Baseline set above actual current coverage causes persistent red CI | H | H | Add pre-enforcement baseline capture test artifact and dry-run command evidence before switching gate to blocking |
| Developers bypass gate pressure with ad hoc test inflation | M | M | Add focused acceptance tests in `tests/` for critical paths; review changed-test-to-changed-code ratio in PR checks |
| CI duration regression from coverage instrumentation | M | M | Track CI wall-clock before/after in execution artifact and add budget alert threshold in design/test docs |

### Option B - Staged Ratchet to Target Baseline (recommended)
Approach:
1. Introduce a blocking global minimum in phases (example: 40 -> 55 -> 70), with each step promoted only after stability criteria are met.
2. Keep threshold value versioned in one explicit config location (`pyproject.toml`) and define ratchet cadence in project artifacts.
3. Add structure/documentation checks that require explicit ratchet updates rather than silent drift.

Research coverage used (6/6):
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

Workspace evidence:
- `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.think.md`
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/structure/test_ci_yaml.py`
- `docs/architecture/archive/8testing-quality.md`

Likely files/workflows to touch:
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/structure/test_ci_yaml.py`
- `tests/test_coverage_config.py`
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.plan.md`
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md`

Pros:
- Best balance between enforcement and delivery stability.
- Aligns with proven ratchet governance pattern already used for strict-quality initiatives.
- Provides measurable progress without requiring big-bang cleanup.

Cons:
- Requires governance discipline (promotion rules, cadence tracking).
- Slightly more process/documentation overhead than fixed gate.
- Risk of stalling at intermediate threshold without explicit accountability.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Ratchet stalls at an intermediate threshold | M | H | Add governance check in project test artifact requiring threshold movement evidence per defined cadence |
| Threshold increases too quickly and destabilizes CI | M | H | Require promotion gate: N consecutive green runs plus baseline snapshot before each increase |
| Different local/CI commands compute coverage differently | M | M | Document single canonical command in test artifact and add structure assertion for CI command parity |

### Option C - Per-Package Floor (global + critical-package minimums)
Approach:
1. Enforce a global minimum plus stricter floors for selected critical packages (for example `src/core/**`, `src/security/**`).
2. Generate per-package coverage report and fail CI if any critical package floor is missed.
3. Keep package list explicit and versioned to avoid hidden scope drift.

Research coverage used (4/6):
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact

Workspace evidence:
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `tests/ci/test_ci_parallelization.py`
- `docs/architecture/archive/8testing-quality.md`

Likely files/workflows to touch:
- `.github/workflows/ci.yml`
- `pyproject.toml` (or dedicated coverage policy config)
- `tests/structure/test_ci_yaml.py`
- New structure/meta tests for per-package policy contract
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.design.md`

Pros:
- Strong risk-based enforcement for high-value modules.
- Better behavioral signal than pure global percentage.
- Future-ready governance model for critical-path quality.

Cons:
- Highest implementation complexity of the three options.
- More maintenance overhead (package policy list and exemptions).
- Greater chance of confusion during early rollout.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Policy list drifts from real critical modules | M | H | Add contract test that validates policy list against documented critical-path mapping |
| CI complexity and runtime increase from multi-report processing | M | M | Add execution-budget assertion in exec artifact and compare against baseline runtime budget |
| Teams optimize for package floors while neglecting integration coverage | M | M | Add integration-suite coverage signal in acceptance criteria and validate with targeted integration tests |

## Decision Matrix
| Criterion | Opt A: Fixed Baseline | Opt B: Staged Ratchet | Opt C: Per-Package Floor |
|---|---|---|---|
| Enforcement strength | High | High (progressive) | Very High |
| Delivery risk (near-term) | High | Medium | Medium-High |
| Implementation complexity | Low-Medium | Medium | High |
| CI stability during rollout | Medium-Low | High | Medium |
| Governance clarity | High | High (if cadence enforced) | Medium |
| Long-term extensibility | Medium | High | High |
| Fit for idea-008 tight scope | Medium | High | Medium-Low |

## Recommendation
**Option B - Staged Ratchet to Target Baseline**

Rationale:
1. It directly addresses the root cause (non-enforcing or missing gate behavior) while avoiding big-bang instability.
2. It reuses proven governance mechanics from strict-lane quality projects (ratchet with explicit promotion gates) rather than inventing a new process.
3. It stays within idea-008 scope: enforce a meaningful minimum quickly, then raise deterministically to target.

Required prior-art anchors for @3design:
- `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.think.md`
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/architecture/archive/8testing-quality.md`

## Initial Acceptance Criteria (for @3design -> @4plan -> @5test)
1. CI includes exactly one blocking coverage-gate path that fails when coverage is below the current ratchet threshold.
2. Threshold source-of-truth is singular and explicit (documented config location), and CI command consumes that source directly.
3. Ratchet policy is documented with promotion rules (minimum green-run window and rollback/pause rule).
4. Structure/meta tests fail if CI coverage gate is removed, softened (`|| true` / continue-on-error), or decoupled from configured threshold.
5. Project test artifact records baseline measurement method and current ratchet step with reproducible command.
6. Workflow-count/CI-structure constraints remain green (no reintroduction of retired workflow sprawl).
7. Handoff package includes clear next threshold target and explicit owner checkpoint for promotion.

## Open Questions
1. Should the first blocking threshold start at current configured `fail_under = 30` or at a newly measured baseline snapshot value?
2. Do we enforce coverage in a dedicated CI step after shard execution, or by adding a single non-sharded coverage run to avoid merge-artifact complexity?
3. What promotion cadence is acceptable for this repository (per sprint vs per release train)?
4. Should critical-path modules receive an explicit future ratchet track (deferred extension), or remain out of scope for prj0000096?
