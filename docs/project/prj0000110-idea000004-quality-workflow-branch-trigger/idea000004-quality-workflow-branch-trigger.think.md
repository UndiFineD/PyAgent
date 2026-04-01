# idea000004-quality-workflow-branch-trigger - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-01_

## Root Cause Analysis
1. Legacy idea drift: the idea text references `.github/workflows/quality.yml` with a stale trigger (`prj0000026-*`), but repository prior-art documents show that workflow was removed in `prj0000075`.
2. Current gap persists in a different form: active quality-enforcing workflows (`.github/workflows/ci.yml`, `.github/workflows/security.yml`) only run on `main` for push and pull_request, so project branches are not validated until PR targets main.
3. Governance intent mismatch: branch-scoped project workflow expects strong per-project quality visibility, while current CI trigger model optimizes for merge-target validation only.
4. Acceptance criteria implication: the solution must satisfy "quality workflow branch trigger" intent against current workflow topology, not resurrect deleted legacy files.

Evidence:
- `.github/workflows/ci.yml`
- `.github/workflows/security.yml`
- `docs/project/ideas/idea000004-quality-workflow-branch-trigger.md`
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/project/prj0000026/prj0000026.git.md`
- `docs/architecture/archive/8testing-quality.md`

## Discovery Coverage
### Literature review
- Local architecture/policy: `docs/architecture/archive/8testing-quality.md`, `docs/project/code_of_conduct.md`, `docs/project/naming_standards.md`.
- Workflow syntax/event behavior: GitHub docs on workflow syntax and trigger events.

### Alternative enumeration
- Considered three distinct strategies:
	1. Widen top-level branch filters.
	2. Keep `main` trigger narrow and add explicit guardrail job for project-branch PRs.
	3. Two-tier model with `workflow_run` chaining (fast trigger + privileged quality workflow).

### Prior-art search
- Historical deletion/simplification rationale: `docs/project/prj0000075/prj0000075.think.md`.
- Original quality workflow introduction: `docs/project/prj0000026/prj0000026.git.md`.
- Coverage/quality governance evolution: `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`.
- Idea source sweep: `docs/project/prj0000076/prj0000076.think.md`.

### Constraint mapping
- Must stay on branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
- Must align with one-project-one-branch governance and avoid legacy workflow sprawl.
- Must preserve deterministic quality outcomes and avoid silent skip states.
- Must remain compatible with existing `ci.yml` quality contract and docs policy tests.

### Stakeholder impact
- Contributors on project branches (earlier quality signal).
- Maintainers/reviewers (required-check behavior and merge reliability).
- @4plan/@5test downstream agents (testability contracts for branch-trigger behavior).
- Security/quality operators (false negatives from skipped workflows).

### Risk enumeration
- Enumerated per option with H/M/L ratings plus testability signals.

## Constraints and Assumptions
1. Branch and scope governance remain mandatory and blocking.
2. Avoid reintroducing historical multi-workflow redundancy rejected in `prj0000075`.
3. Branch filters and path filters must avoid producing permanently pending required checks.
4. Recommendation must map directly to idea acceptance intent and provide measurable testability.

## Options
### Option A - Expand active workflow branch filters for project branches
Approach:
1. Update `ci.yml` and `security.yml` triggers to include project branches (`prj*`) on push and/or pull_request.
2. Keep jobs unchanged; only trigger surface expands.
3. Document trigger contract and non-goals in project artifacts.

Research task types covered: literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

Workspace evidence:
- `.github/workflows/ci.yml`
- `.github/workflows/security.yml`
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`

SWOT:
- Strengths: fastest implementation; immediate visibility on project branches.
- Weaknesses: may significantly increase CI volume on non-merge-ready branches.
- Opportunities: earlier defect detection and faster contributor feedback.
- Threats: noisy failures can incentivize branch churn or trigger fatigue.

Security risk analysis:
| Threat vector | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Excessive CI churn masks real security regressions in noise | M | M | Add branch pattern constraints and run-budget guardrails | Validate run volume delta and failure-to-signal ratio over baseline |
| Broad trigger expansion on sensitive workflows increases attack surface | M | H | Keep strict `permissions` and avoid `pull_request_target` | Static workflow scan for event and permissions contract |
| Misconfigured branch globs skip intended branches | M | H | Add structure tests for trigger patterns | Unit test parses workflow YAML and asserts required patterns |

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| CI load spike slows feedback loop | M | M | Track median queue/runtime before vs after trigger change |
| Trigger misses certain project branch names | M | H | Add regex/path assertions in workflow structure tests |
| Contributors see duplicate/irrelevant runs | M | M | Add event/path scoping tests and validate expected run matrix |

### Option B - Add branch-governance gate job while keeping workflow triggers narrow (recommended)
Approach:
1. Keep existing `main`-focused workflow triggers for full suites.
2. Add a lightweight branch-governance quality gate job for project-branch PR events that validates branch policy, scope boundaries, and required docs artifacts.
3. Reuse existing governance scripts (`scripts/enforce_branch.py`, docs policy tests) to avoid duplicate quality workflows.

Research task types covered: literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

Workspace evidence:
- `scripts/enforce_branch.py`
- `tests/docs/test_agent_workflow_policy_docs.py`
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`
- `docs/architecture/archive/8testing-quality.md`

SWOT:
- Strengths: keeps CI topology simple; adds targeted branch-trigger assurance tied to governance.
- Weaknesses: does not run full build/test suite on every project branch push.
- Opportunities: high signal-to-noise and reuse of established governance assets.
- Threats: if governance gate is mis-scoped, teams may overestimate coverage depth.

Security risk analysis:
| Threat vector | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Governance gate passes while code-level defects remain undetected pre-main | M | M | Explicitly classify gate as governance precheck, not full verification | Contract test ensures gate messaging and required-check naming are explicit |
| Script reuse drift causes false pass/fail | M | M | Pin gate to stable script entrypoints and test selectors | CI test executes exact selector `tests/docs/test_agent_workflow_policy_docs.py` |
| Unauthorized trigger context escalation | L | H | Use `pull_request` event and least-privilege permissions | Static workflow policy check for event type and permissions |

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Gate status unclear to reviewers | M | M | Add test asserting required-check name and description contract |
| Branch/scope validation drift | M | H | Run `scripts/enforce_branch.py` in gate and test expected fail cases |
| False confidence about full quality execution | M | M | Add docs test validating gate scope language in project artifacts |

### Option C - Two-tier branch trigger via `workflow_run` chaining
Approach:
1. Add a lightweight branch-trigger workflow for project branches.
2. Chain privileged or heavier checks via `workflow_run` on completion.
3. Separate fast policy checks from expensive full validation.

Research task types covered: literature review, alternative enumeration, prior-art search, constraint mapping, risk enumeration.

Workspace evidence:
- `.github/workflows/ci.yml`
- `.github/workflows/security.yml`
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/architecture/archive/8testing-quality.md`

SWOT:
- Strengths: flexible pipeline orchestration and phased verification.
- Weaknesses: highest complexity and workflow coupling.
- Opportunities: future extensibility for merge-queue and staged gates.
- Threats: recursive trigger pitfalls and hard-to-debug execution ordering.

Security risk analysis:
| Threat vector | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Trigger-chain privilege misuse (`workflow_run` can escalate) | M | H | Strict permissions and artifact trust boundaries | Security test checks permission minimization and event source constraints |
| Chain depth/ordering failures cause skipped required checks | M | H | Keep chain shallow with explicit completion checks | Integration test verifies downstream workflow runs on expected conclusions |
| Increased operational complexity introduces misconfiguration debt | H | M | Standardize templates and add structure tests | Workflow lint/structure tests assert allowed events and chain topology |

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Downstream workflow never fires | M | H | Add CI fixture event simulation and required-check presence assertions |
| Token/secret context over-privilege | M | H | Add static policy test over workflow permissions blocks |
| Debugging overhead slows incident response | H | M | Add runbook validation section and incident drill checklist |

## Stakeholder Impact Summary
| Stakeholder | Option A | Option B | Option C |
|---|---|---|---|
| Contributors on project branches | Earlier full checks, heavier run volume | Earlier governance feedback, low noise | Mixed; fast then chained checks, more complexity |
| Reviewers/maintainers | More check traffic | Clear policy gate + existing main checks | Harder to reason about required checks |
| Security/quality owners | More data, more triage | High-signal governance controls | Rich but complex control surface |
| Downstream agents (@3design/@4plan/@5test) | Straightforward trigger change | Clear reusable gate design path | More orchestration design burden |

## Decision Matrix
| Criterion | Option A: Expand branch filters | Option B: Governance gate + narrow triggers | Option C: Two-tier workflow_run chain |
|---|---|---|---|
| Delivery speed | High | Medium-High | Medium-Low |
| Complexity | Low | Medium | High |
| Reuse of existing assets | Medium | High | Medium |
| CI cost/noise control | Low | High | Medium |
| Security posture clarity | Medium | High | Medium-Low |
| Testability and determinism | Medium | High | Medium |
| Fit to acceptance intent | High | High | Medium |

## Recommendation
**Option B - Add a targeted branch-governance quality gate while keeping full-suite triggers narrow to main.**

Rationale:
1. Best alignment with repository prior-art that intentionally removed redundant workflow sprawl (`docs/project/prj0000075/prj0000075.think.md`).
2. Reuses proven governance controls already in code and tests (`scripts/enforce_branch.py`, `tests/docs/test_agent_workflow_policy_docs.py`) instead of rebuilding overlapping quality jobs.
3. Preserves deterministic quality model from architecture guidance (`docs/architecture/archive/8testing-quality.md`) while directly addressing idea intent: branch-trigger quality signal on active project work.

Historical prior-art references (required):
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`
- `docs/project/prj0000026/prj0000026.git.md`

Acceptance-criteria mapping:
1. Branch-trigger quality behavior exists for project branches (governance gate).
2. Required checks remain deterministic and avoid stale/pending skip traps.
3. No regression to legacy redundant workflow topology.
4. Validation path remains script/test backed and reproducible.

## Open Questions for @3design
1. Should the governance gate run on push to `prj*` branches, PR events to `main`, or both?
2. Must the gate be strictly blocking for merge, or informational on push + blocking on PR?
3. Should security workflow branch behavior mirror CI gate behavior, or remain main-only with explicit rationale?
4. Is merge-queue support (`merge_group`) in scope now or explicitly deferred?