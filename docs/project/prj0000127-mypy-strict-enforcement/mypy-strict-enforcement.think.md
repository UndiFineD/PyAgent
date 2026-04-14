# mypy-strict-enforcement - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-04_

## Root Cause Analysis
- The idea requires progressive strictness for Python agents beginning in `src/core`, but the root `mypy.ini` currently sets `strict = False` and `ignore_errors = True` with `files = src`; this makes the default gate effectively non-enforcing for repository-wide checks.
- The repository also defines a stricter `[tool.mypy]` in `pyproject.toml` (`strict = true`) with selective relaxations and explicit notes about gradual adoption. This creates governance ambiguity because two active config surfaces express opposite baseline strictness.
- Prior-art in the repository shows successful targeted mypy gating on bounded slices (for example, focused commands in prior project artifacts) instead of immediate full-repo strict mode, indicating phased enforcement is the stable local pattern.
- Current project boundary is docs-focused at this stage. Enforcement must be designed for downstream agents without forcing large code refactors in this option phase.

## Research Coverage
- Literature review:
	- `docs/project/ideas/idea000003-mypy-strict-enforcement.md`
	- `mypy.ini`
	- `pyproject.toml`
	- `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.project.md`
- Alternative enumeration:
	- soft config-only rollout
	- progressive blocking allowlist rollout
	- immediate all-core blocking rollout
- Prior-art search:
	- `docs/project/archive/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`
	- `docs/project/prj0000124-llm-gateway/llm-gateway.plan.md`
	- `docs/project/kanban.json`
- Constraint mapping:
	- Branch must remain `prj0000127-mypy-strict-enforcement`.
	- Scope for this step: project docs artifacts + @2think memory/log only.
	- No production code changes in @2think mode.
	- Naming and conduct policies must remain aligned with `docs/project/naming_standards.md` and `docs/project/code_of_conduct.md`.
- Stakeholder impact:
	- @3design defines strict-lane architecture and phase boundaries.
	- @4plan maps rollout into executable, deterministic gates.
	- @5test/@7exec own pass-fail enforcement signal integrity.
	- @6code owns remediation only within approved rollout slices.
- Risk enumeration: included per option below with risk-to-testability mapping.

## Constraints and Scope Boundaries
- In scope for this @2think delivery:
	- Option analysis for progressive mypy strictness.
	- Recommendation and phased rollout order for downstream design/planning.
	- Documentation milestone update (M1).
- Out of scope for this @2think delivery:
	- Editing `mypy.ini`, `pyproject.toml`, source code, CI workflows, or tests.
	- Running broad mypy remediation.
- Acceptance signals for this stage:
	- Think artifact contains at least 3 concrete options.
	- Decision matrix includes risk/effort/value.
	- Recommendation includes phased rollout order and explicit boundaries.
	- Docs policy selector passes.

## Options
### Option A - Observation-first strictness (non-blocking pilot)
Approach:
- Keep current enforcement permissive at repo baseline while introducing one or more informational mypy checks for a narrow `src/core` slice.
- Focus on signal collection (error profile, churn hotspots, dependency noise) before enabling blocking gates.

SWOT:
- Strengths: minimal disruption; low immediate CI instability risk.
- Weaknesses: does not prevent regressions during pilot.
- Opportunities: produces empirical baseline for safer phase planning.
- Threats: teams may normalize warnings and delay true enforcement.

Stakeholder impact:
- Low disruption for @6code and @7exec.
- Moderate analysis load for @3design/@4plan to convert signal into enforceable gates.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Warning-only lane is ignored | H | M | CI log contract check: informational lane must publish explicit warning counts and trend deltas |
| Config divergence persists (`mypy.ini` vs `pyproject.toml`) | H | H | Structure test asserting canonical config source declaration and explicit precedence note |
| Pilot slice not representative | M | M | Add acceptance rule for diverse module sampling in pilot target list |

### Option B - Progressive blocking allowlist (recommended)
Approach:
- Establish a blocking strict lane for an explicit phase-1 allowlist in `src/core` while keeping non-core and legacy paths on gradual mode.
- Expand strict lane by phase only after deterministic acceptance signals pass.
- Pair every expansion with updated guardrails and explicit rollback criteria.

SWOT:
- Strengths: real enforcement with controlled blast radius.
- Weaknesses: requires ongoing allowlist governance.
- Opportunities: creates repeatable rollout template for additional packages.
- Threats: if allowlist maintenance drifts, teams can route around strict lanes.

Stakeholder impact:
- @3design/@4plan: moderate design and sequencing effort.
- @5test: moderate work to harden structure and CI invariants.
- @6code: targeted typing remediation on strict-lane modules only.
- @7exec/@8ql: clear binary signal for scoped enforcement.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Allowlist shrinks silently to bypass strictness | M | H | Structure test pins allowlist entries and fails on unreviewed removals |
| Blocking lane flaps due to unstable module choice | M | M | Start with low-churn modules; enforce phase gate requiring N consecutive green runs |
| Config precedence confusion breaks intended behavior | M | H | Deterministic selector validates effective mypy config used by strict lane command |

### Option C - Full `src/core` strict blocking immediately
Approach:
- Switch to strict blocking for all `src/core` in one move and remediate until green.

SWOT:
- Strengths: fastest path to maximum enforcement coverage.
- Weaknesses: highest short-term disruption and refactor demand.
- Opportunities: immediate consistency in core typing quality.
- Threats: broad red-wall can force emergency bypasses and weaken policy trust.

Stakeholder impact:
- High load across @4plan, @5test, @6code, @7exec.
- Elevated schedule risk for concurrent projects.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Immediate CI red-wall blocks unrelated delivery | H | H | Preflight dry-run report artifact + severity-based triage threshold before cutover |
| Scope creep beyond planned rollout | H | H | Strict changed-file scope checks tied to project artifact updates |
| Emergency global ignores reintroduced | M | H | Policy test forbidding new blanket `ignore_errors = True` for core paths |

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Delivery risk (lower is better) | Low | Medium-Low | High |
| Effort (lower is better) | Low | Medium | High |
| Enforcement value | Low-Medium | High (scoped) | Very High |
| Stability during rollout | High | Medium-High | Low-Medium |
| Fit with progressive requirement | Medium | High | Low |
| Overall recommendation score | 3/5 | 5/5 | 2/5 |

## Recommendation
**Option B - Progressive blocking allowlist**

Rationale:
- Best balance of value vs. risk for this repository's current dual-config state.
- Aligns with prior-art from previous strictness project (`prj0000092`) and recent bounded mypy gating pattern (`prj0000124`) where focused checks were kept deterministic.
- Satisfies the idea requirement for progressive rollout starting in `src/core` without requiring immediate broad refactoring.

Phased rollout order for @3design/@4plan:
1. Phase 1: declare canonical strict-lane config behavior and introduce blocking lane for a small low-churn `src/core` allowlist.
2. Phase 2: remediate phase-1 typed defects and add guard tests for config precedence + allowlist drift.
3. Phase 3: expand allowlist to adjacent `src/core` modules with explicit entry criteria and rollback threshold.
4. Phase 4: evaluate migration path from split strictness toward wider repository policy convergence.

Acceptance signals for downstream execution phases:
- Strict-lane command exists and is blocking for phase allowlist.
- Deterministic tests verify allowlist integrity and config precedence behavior.
- No new blanket ignores for strict-lane modules.
- Consecutive green-run threshold met before each expansion.

## Open Questions
1. Which exact `src/core` subpackages should be phase-1 allowlist candidates based on churn and dependency surface?
2. Should repository policy converge on one mypy config authority (`mypy.ini` or `pyproject.toml`) before phase-2 expansion?
3. What green-run threshold (for example, consecutive runs) should be required before expanding strict coverage?
4. Do we want strict-lane enforcement to run on PR only, push + PR, or both in phase 1?

