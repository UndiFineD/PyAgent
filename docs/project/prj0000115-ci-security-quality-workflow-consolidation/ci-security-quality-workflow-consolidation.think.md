# ci-security-quality-workflow-consolidation - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-02_

## Root Cause Analysis
1. CI/security intent and implementation drifted over time: legacy ideas described missing automation while current repository state already uses a lightweight CI model with `pre-commit run --all-files` in `.github/workflows/ci.yml`.
2. Security coverage is partially manual: `pip_audit_results.json` exists as a generated artifact but there is no dedicated scheduled security workflow and only one workflow file is present under `.github/workflows/`.
3. Repository security capabilities are available but under-integrated in CI: `codeql/` and `codeql-custom-queries-*` directories exist, but no active CodeQL workflow is wired.
4. Governance and branch protections are present (`scripts/enforce_branch.py` and docs policy checks), but heavyweight security scan cadence and ownership boundaries remain unclear.

## Current-State Assessment

### Evidence Summary
1. `.pre-commit-config.yaml` currently includes:
	 - Python quality hooks: `ruff`, `ruff-format`, `mypy`.
	 - Local governance/security hooks: `enforce-branch`, `secret-scan`.
	 - Rust hooks: `rust-fmt`, `rust-clippy`.
	 - Shared orchestrator hook: `run-precommit-checks` (`python scripts/ci/run_checks.py --profile precommit`).
2. `.github/workflows/ci.yml` currently defines one lightweight workflow/job family:
	 - Workflow: `CI / Lightweight`.
	 - Trigger: `push` to `main`, and `pull_request` to `main` or project branches matching `prj[0-9]{7}-*`.
	 - Job `quick`: checkout, Python setup, install `requirements-ci.txt`, run `pre-commit run --all-files`, then run `pytest tests/ci/test_placeholder_smoke.py -q`.
3. `.github/workflows/` currently contains only `ci.yml`.

### Gaps Relative to idea000131 Intent
1. No explicit scheduled heavyweight security scans (for example nightly dependency audit or CodeQL deep scan).
2. No active CodeQL workflow despite local query assets (`codeql/`, `codeql-custom-queries-python/`, `codeql-custom-queries-rust/`, etc.).
3. Dependency vulnerability scanning is not codified in workflow automation; repository evidence still includes committed report output (`pip_audit_results.json`) consistent with partial/manual operation.

### Constraint Map
1. Branch constraint: must remain on `prj0000115-ci-security-quality-workflow-consolidation`.
2. Scope constraint for this phase: discovery artifact updates only under `docs/project/prj0000115-ci-security-quality-workflow-consolidation/`.
3. Non-edit constraint: do not modify `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, or source files during @2think.
4. Governance constraint: follow `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
5. Architecture constraint: preserve lightweight CI behavior and avoid regressing branch/governance checks already in place.

## Options
### Option A - Incremental pre-commit hook group rollout

#### Proposed approach
Add or tune pre-commit hook groups in phases (quality -> rust/security -> dependency/security policy), while keeping CI as confirmation and avoiding immediate major workflow topology changes.

#### Research task coverage
1. Literature review: `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`, `.pre-commit-config.yaml`.
2. Alternative enumeration: staged rollout minimizes disruption while allowing policy hardening by tranche.
3. Prior-art search: `docs/project/ideas/archive/idea000004-quality-workflow-branch-trigger.md`, `docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md`.
4. Constraint mapping: branch/scope/no-edit constraints from project artifact and assignment.
5. Stakeholder impact: contributors, maintainers, @3design/@4plan/@5test, and CI reviewers.
6. Risk enumeration: detailed below with testability mapping.

#### SWOT
- Strengths:
	- Lowest migration shock; aligns with existing pre-commit-first baseline.
	- Easier rollback by disabling specific hook groups.
	- Preserves fast PR signal while improving local catch rate.
- Weaknesses:
	- Security parity may remain incomplete for multiple iterations.
	- Requires careful sequencing and ownership to avoid "half-migrated" state.
	- Can leave temporary duplication between local and CI checks.
- Opportunities:
	- Build durable ownership model per hook domain (quality/rust/security).
	- Standardize contributor workflow around one local command surface.
	- Reduce flaky CI failures by shifting deterministic checks earlier.
- Threats:
	- Extended transition window can create policy ambiguity.
	- Contributors with inconsistent local environments may encounter setup friction.
	- Security stakeholders may perceive delayed full coverage as unacceptable.

#### Security risk analysis with testability mapping
| Risk ID | Threat vector | Likelihood | Impact | Mitigation concept | Testability signal |
|---|---|---|---|---|---|
| A-R1 | Hook group staged too slowly leaves dependency vulnerabilities unguarded | M | H | Time-box phase gates and enforce milestone-based promotion | Workflow contract test proving phase deadlines + policy assertions in docs checks |
| A-R2 | Local hook bypass (`--no-verify`) reduces enforcement reliability | M | M | Keep CI confirmation job mandatory for protected branches | Branch protection required-check simulation and CI gate tests |
| A-R3 | Rust security/lint drift if hook versions diverge from CI toolchain | M | M | Version pinning policy and periodic parity checks | Deterministic parity script comparing hook tool versions in CI logs |

#### Pros
1. Best fit for teams prioritizing low-risk adoption and contributor ergonomics.
2. Strong compatibility with existing lightweight `ci.yml` and governance checks.
3. Clear rollback boundaries for each phase.

#### Cons
1. Slower time to complete security consolidation.
2. Requires explicit phase governance to avoid indefinite partial rollout.
3. Can delay activation of CodeQL/dependency automation if phases stall.

### Option B - Pre-commit baseline + minimal CI verifier from day one

#### Proposed approach
Normalize all feasible checks behind pre-commit immediately, then reduce CI validation to a single verifier path (`pre-commit run --all-files` + minimal smoke/governance checks) from day one.

#### Research task coverage
1. Literature review: current `.github/workflows/ci.yml` already includes `pre-commit run --all-files` and a smoke test.
2. Alternative enumeration: consolidate to one canonical verification path.
3. Prior-art search: `docs/architecture/archive/8testing-quality.md` (deterministic quality gates), `docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md` (lightweight governance gate pattern).
4. Constraint mapping: maintain lightweight CI and project branch trigger behavior.
5. Stakeholder impact: largest immediate impact on contributors and CI maintainers.
6. Risk enumeration: detailed below with testability mapping.

#### SWOT
- Strengths:
	- Fastest unification of local and CI signals.
	- Simplifies maintenance by reducing duplicated check logic.
	- Deterministic contributor guidance: one command surface.
- Weaknesses:
	- Big-bang shift can break contributor flow if environment assumptions are wrong.
	- CI may under-represent heavyweight security posture unless separately scheduled.
	- Requires robust pre-commit performance tuning to avoid local slowdowns.
- Opportunities:
	- Create a strict "local pass implies CI pass" development contract.
	- Lower CI runtime and queue pressure through check deduplication.
	- Clarify policy ownership between pre-commit and CI quickly.
- Threats:
	- Immediate regressions if hidden CI-only assumptions exist.
	- Potential false confidence if pre-commit excludes important file scopes.
	- Resistance from contributors on platforms lacking tooling parity.

#### Security risk analysis with testability mapping
| Risk ID | Threat vector | Likelihood | Impact | Mitigation concept | Testability signal |
|---|---|---|---|---|---|
| B-R1 | Missing heavyweight scans creates blind spots after CI simplification | M | H | Pair baseline with explicit scheduled security jobs | Scheduled workflow dry-run/assertion tests and alert ingestion checks |
| B-R2 | Pre-commit file filters miss sensitive paths | M | H | Expand and test hook coverage map against repository structure | Coverage-style "hook target map" tests over representative path fixtures |
| B-R3 | Contributor environments fail on unified hook stack | M | M | Provide bootstrap validation and platform compatibility checks | Cross-platform CI matrix for pre-commit bootstrap smoke tests |

#### Pros
1. Highest simplicity once stabilized.
2. Strong consistency between local and CI behavior.
3. Immediate reduction in duplicated workflow logic.

#### Cons
1. Highest transition risk and onboarding friction.
2. Needs immediate parallel investment in scheduled security controls.
3. Less forgiving for teams preferring gradual operational change.

### Option C - Hybrid: fast pre-commit checks + scheduled heavyweight security scans

#### Proposed approach
Keep pre-commit as fast primary gate (quality/rust/secret/governance) and keep CI lightweight for confirmation on PR/push, while adding scheduled heavyweight security workflows (for example CodeQL and dependency vulnerability scanning) on a daily cadence.

#### Research task coverage
1. Literature review: idea000131 non-goal favors not replacing all CI checks in one change; current `ci.yml` already lightweight.
2. Alternative enumeration: separates fast developer feedback from expensive periodic scanning.
3. Prior-art search: `docs/project/ideas/archive/idea000006-codeql-ci-integration.md`, `docs/project/ideas/archive/idea000007-security-scanning-ci.md`, and `docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md`.
4. Constraint mapping: preserves current CI trigger model and branch governance while addressing missing scan automation.
5. Stakeholder impact: balanced impact across contributors, security reviewers, and release owners.
6. Risk enumeration: detailed below with testability mapping.

#### SWOT
- Strengths:
	- Balances developer speed and security depth.
	- Preserves already-working lightweight CI topology.
	- Directly addresses CodeQL and dependency scan automation gaps.
- Weaknesses:
	- Two cadences (per-PR vs scheduled) increase operational complexity.
	- Requires clear ownership of scheduled scan triage.
	- Vulnerability discovery may occur post-merge rather than pre-merge.
- Opportunities:
	- Use scheduled jobs to tune false-positive handling without blocking all PRs.
	- Integrate repository CodeQL custom queries with controlled runtime cost.
	- Establish explicit security SLOs (scan freshness and triage response).
- Threats:
	- Scheduled jobs can be ignored if alert routing is weak.
	- Security debt can accumulate between schedule intervals.
	- Overly broad scheduled scans can consume CI resources unexpectedly.

#### Security risk analysis with testability mapping
| Risk ID | Threat vector | Likelihood | Impact | Mitigation concept | Testability signal |
|---|---|---|---|---|---|
| C-R1 | Daily scans detect issues after merge, extending exposure window | M | H | Define severity-based response SLAs and optional on-demand manual trigger | SLA compliance dashboard checks + incident drill test scenarios |
| C-R2 | CodeQL workflow misconfiguration yields false sense of coverage | M | H | Use minimal verified CodeQL template with explicit language matrix and permissions | Workflow schema tests + SARIF upload assertion in CI test harness |
| C-R3 | Dependency scan noise causes alert fatigue | M | M | Apply ignore policy governance and triage ownership model | Regression tests for allowlist rules and periodic alert volume reports |

#### Pros
1. Best alignment with current repository state: pre-commit and lightweight CI are already active.
2. Addresses missing heavyweight security automation without overloading per-PR cycles.
3. Provides clear separation of fast feedback vs deep analysis responsibilities.

#### Cons
1. Requires careful scheduled-job governance and triage discipline.
2. Some vulnerabilities surface later than a fully blocking pre-merge model.
3. More policy documentation required for severity thresholds and escalation.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Delivery risk | Low-Medium | High | Medium |
| Time to unified developer experience | Medium | Fast | Medium |
| Security-depth coverage potential | Medium | Medium (unless extra work added) | High |
| Fit with current repository state | High | Medium | High |
| CI runtime efficiency | Medium-High | High | High |
| Governance/operational complexity | Medium | Medium | Medium-High |
| Overall score (qualitative) | 7/10 | 7/10 | 8/10 |

## Recommendation
**Option C (with Option A-style phased execution discipline)**

Rationale:
1. Best matches observed current state: lightweight CI verifier is already in place (`.github/workflows/ci.yml`), and pre-commit already carries core quality/rust/security hooks (`.pre-commit-config.yaml`).
2. Directly closes the biggest uncovered area from discovery: absence of active automated heavyweight security scanning despite available local assets (`codeql/`, `codeql-custom-queries-*`, and manual `pip_audit_results.json` artifact).
3. Preserves prior-art direction to avoid full-suite duplication on project branches while keeping deterministic governance checks:
	 - `docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md`
	 - `docs/project/ideas/archive/idea000006-codeql-ci-integration.md`
	 - `docs/project/ideas/archive/idea000007-security-scanning-ci.md`
4. Aligns with approved external patterns:
	 - `pre-commit` as multi-language local gate framework (github.com/pre-commit/pre-commit)
	 - `pip-audit` supports both pre-commit and GitHub Actions integration (github.com/pypa/pip-audit)
	 - CodeQL action supports advanced workflow setup and explicit permissions (github.com/github/codeql-action)

## Risk-to-Testability Mapping for Recommended Direction
| Recommended-risk ID | Risk statement | Proposed testability strategy |
|---|---|---|
| R-REC-1 | Scheduled scans run but are not actioned | Add policy test validating alert routing and issue-creation contract; measure SLA conformance |
| R-REC-2 | Scheduled CodeQL introduces long runtimes or failures | Add workflow contract tests for matrix/build mode and canary run verification on sample PR |
| R-REC-3 | Pre-commit and CI drift over time | Add parity checks asserting CI verifier uses same hook baseline and pinned versions |

## Open Questions
1. Should heavyweight security scans be daily only, or daily plus manual dispatch for release branches?
2. Which severity thresholds should block merges immediately vs create follow-up tickets?
3. Should CodeQL run on `main` only, or also on PRs touching high-risk paths (`scripts/security/`, auth, workflow files)?
4. Who owns scheduled scan triage and SLA enforcement (security role vs rotating maintainer)?
5. Should dependency scanning target `requirements.txt`, `requirements-ci.txt`, and lockfiles equally, or prioritize release artifacts?
6. What is the maximum acceptable runtime budget for scheduled scans to avoid CI contention?
7. Should `pre-commit run --all-files` remain the sole CI verifier command, or should minimal explicit governance assertions remain separate for traceability?

## Handoff Notes for @3design
1. Preserve current lightweight CI semantics; avoid reintroducing heavy per-push suites.
2. Treat scheduled security workflows as first-class design artifacts with explicit permissions, cadence, and triage contracts.
3. Maintain one source of truth for fast checks (pre-commit baseline) and formalize parity assertions between local and CI execution.
4. Docs policy selector currently has one pre-existing legacy-file failure outside this project scope (`docs/project/prj0000005/prj005-llm-swarm-architecture.git.md` missing).

## Open Questions
TBD
