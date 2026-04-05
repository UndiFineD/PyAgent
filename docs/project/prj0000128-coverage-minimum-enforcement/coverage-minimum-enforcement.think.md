# coverage-minimum-enforcement - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-05_

## Root Cause Analysis
- The original idea is partially stale. It claims the active coverage gate is effectively `--cov-fail-under=1`, but the current repository already sets `[tool.coverage.report].fail_under = 40` in `pyproject.toml`, and `tests/test_coverage_config.py` enforces that floor.
- The live enforcement gap is elsewhere: `.github/workflows/ci.yml` does not run coverage at all in the blocking `quick` job, and `tests/structure/test_ci_yaml.py` currently asserts that no coverage gate path exists in lightweight CI.
- The repository therefore has split governance: config tests say a minimum exists, while CI structure tests and workflow behavior ensure that minimum is never exercised on the blocking path.
- Prior art in archived `prj0000096` already identified this same gap, but current repo state shows only part of that earlier intent survived: the configured threshold and its tests remain, while the CI runtime gate is absent.
- The smallest valuable next slice is not another threshold increase. It is reconnecting CI to the existing `40` floor so the configured minimum becomes an actual blocking signal.

## Research Coverage
- Literature review:
	- `docs/project/ideas/idea000008-coverage-minimum-enforcement.md`
	- `pyproject.toml`
	- `.github/workflows/ci.yml`
	- `tests/test_coverage_config.py`
	- `tests/structure/test_ci_yaml.py`
- Alternative enumeration:
	- single-step coverage gate inside the current `quick` job
	- dedicated blocking coverage job inside the existing `ci.yml`
	- contract-only/docs-only refresh with runtime enforcement deferred
- Prior-art search:
	- `docs/project/archive/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`
	- `docs/project/archive/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md`
	- `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.think.md`
	- `docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.think.md`
- Constraint mapping:
	- Branch must remain `prj0000128-coverage-minimum-enforcement`.
	- This @2think step is docs-only; no production workflow or test changes are allowed yet.
	- Current CI contract is intentionally lightweight and constrained by `tests/structure/test_ci_yaml.py`.
	- Current threshold source of truth already exists in `pyproject.toml`; duplicating the value elsewhere would reintroduce drift risk.
- Stakeholder impact:
	- @3design must choose how to reconnect blocking CI without breaking lightweight CI intent.
	- @4plan must map the exact workflow/test/doc changes and keep them in one bounded slice.
	- @5test must flip current structure assertions from “no coverage gate” to “one blocking coverage gate.”
	- @6code will own the actual workflow/test/config edits, but should avoid raising the threshold in the same slice.
	- @7exec must produce deterministic evidence that the new gate consumes the configured floor.
- Risk enumeration:
	- Included per option below with explicit risk-to-testability mapping.
- Approved external evidence:
	- `pytest-cov` documentation on PyPI and GitHub states that coverage behavior can be driven through pytest-cov CLI options or coverage config, and that the plugin handles default reporting/coverage data combination. That supports keeping `pyproject.toml` as the threshold authority while adding one blocking CI execution path.

## Constraints and Scope Boundaries
- In scope for this @2think delivery:
	- Replace the placeholder options artifact with grounded analysis.
	- Identify the current mismatch between configured threshold and CI invocation reality.
	- Recommend the smallest valuable implementation slice for downstream agents.
	- Update milestone M1 when discovery is complete.
- Out of scope for this @2think delivery:
	- Editing `.github/workflows/ci.yml`, `pyproject.toml`, or tests.
	- Raising the coverage floor above `40`.
	- Adding per-package thresholds or additional workflow files.

## Options
### Option A - Add One Blocking Coverage Step to `jobs.quick`
Approach:
- Keep the existing single-job lightweight workflow shape.
- Add one blocking coverage command to the current `quick` job and point it at the existing `pyproject.toml` floor.
- Update structure tests so `quick` requires exactly one blocking coverage gate path instead of asserting absence.

Research task coverage:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

Workspace evidence:
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/test_coverage_config.py`
- `tests/structure/test_ci_yaml.py`
- `docs/project/archive/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md`

SWOT:
- Strengths: smallest YAML delta; one workflow job remains easy to reason about.
- Weaknesses: makes the current `quick` job less lightweight and more internally overloaded.
- Opportunities: fast reconnection of CI to the already-configured `40` floor.
- Threats: duplicated pytest work can slow routine PR feedback and encourage future bypass pressure.

Stakeholder impact:
- @3design/@4plan: low-to-medium complexity.
- @5test/@7exec: straightforward verification surface.
- Developers: slower `quick` feedback loop.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| `quick` job runtime grows enough to reduce feedback quality | M | M | Compare pre/post job duration in exec evidence and set an explicit runtime budget in downstream artifacts |
| Coverage command drifts from `pyproject.toml` threshold authority | M | H | Add deterministic structure/config tests that require one canonical threshold source and one blocking coverage path |
| Duplicate pytest execution produces confusing failures | M | M | Require a single documented coverage command and a structure test that forbids multiple coverage gate steps |

### Option B - Add One Dedicated Blocking Coverage Job in Existing `ci.yml`
Approach:
- Keep `jobs.quick` lightweight for fast hygiene checks.
- Add a separate blocking `coverage` job in the same workflow that runs once, honors the existing `fail_under = 40`, and becomes the canonical enforcement path.
- Update structure tests to require exactly one blocking coverage job/step while preserving the existing single-workflow footprint.

Research task coverage:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

Workspace evidence:
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/test_coverage_config.py`
- `tests/structure/test_ci_yaml.py`
- `docs/project/archive/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`
- `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.think.md`

SWOT:
- Strengths: cleanest fit with current repo reality; preserves lightweight quick checks while adding true blocking enforcement.
- Weaknesses: slightly more YAML/test complexity than Option A.
- Opportunities: creates a stable place for later ratchet work without changing the meaning of `quick`.
- Threats: if job boundaries are underspecified, config and CI can drift again.

Stakeholder impact:
- @3design: define job boundaries and fail-closed semantics.
- @4plan/@5test: specify and enforce the one-job/one-threshold contract.
- @6code: bounded workflow/test edits with no threshold raise.
- @7exec: clearer validation surface than Option A.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Coverage job is added but not truly blocking | M | H | Structure tests must fail on `continue-on-error`, soft-fail shell patterns, or non-required job placement |
| Threshold is duplicated in YAML instead of sourced from config policy | M | H | Config tests plus workflow contract checks must assert one threshold authority and parity with the runtime command |
| New job scope expands into broader CI redesign | L | M | Plan/test artifacts must cap scope to one new blocking coverage path in the existing workflow file only |

### Option C - Keep Runtime Enforcement Deferred and Refresh Docs/Contracts Only
Approach:
- Accept current `fail_under = 40` as a config-only policy signal.
- Update docs and tests to describe the current state accurately, but defer blocking runtime enforcement to a later project.
- Treat this project as a governance cleanup rather than a CI behavior change.

Research task coverage:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Risk enumeration

Workspace evidence:
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `tests/test_coverage_config.py`
- `tests/structure/test_ci_yaml.py`
- `docs/project/archive/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`

SWOT:
- Strengths: lowest implementation risk.
- Weaknesses: leaves the actual enforcement gap unresolved.
- Opportunities: minimal churn if the repository is not ready for coverage runtime cost.
- Threats: creates false confidence because coverage policy remains documented but unenforced.

Stakeholder impact:
- Low near-term load on @4plan/@6code.
- High residual risk for @7exec/@8ql because the claimed policy still lacks runtime backing.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Teams assume coverage is already enforced because tests assert a threshold exists | H | H | Add explicit docs assertions that distinguish config-only state from runtime enforcement state |
| Later projects must rediscover the same gap | H | M | Record explicit deferred-work acceptance criteria and failure disposition in downstream artifacts |
| Coverage floor drifts upward or downward without any runtime signal | M | M | Keep config tests, but note this remains a non-blocking governance-only signal |

## Decision Matrix
| Criterion | Option A: step in `quick` | Option B: dedicated coverage job | Option C: docs/contracts only |
|---|---|---|---|
| Solves current root cause | High | High | Low |
| Smallest valuable next slice | Medium-High | High | Low |
| Preserves current lightweight CI semantics | Low | High | High |
| Governance clarity | Medium | High | Low |
| Implementation complexity | Low | Medium | Low |
| Long-term ratchet readiness | Medium | High | Low |
| Overall fit with current repo truth | Medium | High | Low |

## Recommendation
**Option B - Add one dedicated blocking coverage job in the existing `ci.yml` at the current `40` floor.**

Rationale:
- The original idea's `1`-threshold premise is stale, so the best next move is not a new floor increase. The best next move is making CI honor the floor the repository already claims to enforce.
- Option B gives the smallest valuable behavior change without redefining the meaning of the current lightweight `quick` job.
- It reuses proven local governance patterns: one workflow file, one explicit blocking path, one threshold authority, and one bounded slice before any later ratchet increase.

### Smallest Valuable Next Slice
1. Keep `[tool.coverage.report].fail_under = 40` unchanged.
2. Add exactly one blocking coverage path in `.github/workflows/ci.yml`.
3. Flip `tests/structure/test_ci_yaml.py` from asserting absence of coverage gating to asserting presence of one fail-closed gate.
4. Keep `tests/test_coverage_config.py` as the threshold-authority guard.
5. Defer any raise above `40` to a follow-up ratchet project after measured green evidence exists.

### Acceptance Signals for Downstream Design/Plan
1. The active CI workflow contains exactly one blocking coverage gate path in `.github/workflows/ci.yml`.
2. The runtime coverage command honors the threshold defined in `pyproject.toml` rather than introducing a conflicting second source of truth.
3. `tests/structure/test_ci_yaml.py` fails if the coverage gate path is removed, softened, or duplicated.
4. `tests/test_coverage_config.py` still enforces `fail_under >= 40` and remains aligned with the runtime gate.
5. Execution evidence shows the coverage path runs on the project branch without changing the threshold above `40`.

## Open Questions
1. Should the coverage gate be a dedicated job dependency after `quick`, or an independent blocking job in the same workflow graph?
2. Should downstream implementation use `pytest --cov=src ...` directly, or run `coverage report` after a separate coverage-producing pytest invocation?
3. What runtime budget is acceptable before the repository should revisit sharding or narrower coverage scope?
4. After CI is reconnected to `40`, what evidence threshold should justify the next ratchet increase?

