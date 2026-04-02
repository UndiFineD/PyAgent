# prj0000094-idea-003-mypy-strict-enforcement - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
1. The baseline mypy configuration remains permissive (`strict = False`, `ignore_errors = True`), so repo-wide typing is still non-enforcing.
2. A strict-lane pattern already exists and is CI-blocking, but currently covers only a locked 6-file allowlist in `src/core`.
3. Existing structure and smoke tests enforce strict-lane invariants, which is good for deterministic governance but also means expansion must be explicit and test-backed.
4. The rollout must stay practical for current CI/test architecture and Windows PowerShell local workflows.

## Branch and Policy Validation
- Expected branch from project artifact: `prj0000094-idea-003-mypy-strict-enforcement`.
- Observed branch: `prj0000094-idea-003-mypy-strict-enforcement`.
- Branch gate result: PASS.
- Policy references reviewed: `docs/project/code_of_conduct.md`, `docs/project/naming_standards.md`.

## Research Coverage Summary
Task types covered in this discovery:
1. Literature review
2. Alternative enumeration
3. Prior-art search
4. Constraint mapping
5. Stakeholder impact
6. Risk enumeration

Primary evidence paths:
- `mypy.ini`
- `mypy-strict-lane.ini`
- `.github/workflows/ci.yml`
- `tests/structure/test_mypy_strict_lane_config.py`
- `tests/structure/test_ci_yaml.py`
- `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`
- `docs/setup.md`
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.design.md`
- `docs/architecture/archive/8testing-quality.md`

## Constraint Map
1. Keep strict project boundary in discovery artifacts only.
2. Preserve deterministic CI gates and existing shard model.
3. Avoid broad, high-churn refactors during initial enforcement waves.
4. Support Windows PowerShell local commands alongside CI Linux execution.
5. Keep rollback explicit and low-friction.

## Options
### Option A - Explicit Allowlist Waves (Expand the current strict lane in phases)
Approach:
- Keep global `mypy.ini` permissive for now.
- Expand `mypy-strict-lane.ini` allowlist in controlled waves (Wave 1 -> Wave 2 -> Wave 3) inside `src/core/**`.
- Keep CI blocking on strict lane from the first expansion wave.

Research task types used:
- Literature review: current lane and tests already implemented.
- Prior-art search: phase-based pattern in prj0000092 artifacts.
- Constraint mapping: minimal churn and deterministic gating.
- Stakeholder impact: moderate impact to @5test/@6code; low risk for @7exec.
- Risk enumeration: see table below.

Workspace evidence:
- `mypy-strict-lane.ini`
- `tests/structure/test_mypy_strict_lane_config.py`
- `.github/workflows/ci.yml`

Trade-offs:
- Safety: High (scoped and test-locked).
- Developer friction: Medium (incremental typing remediation).
- CI stability: High (small blast radius per wave).
- Rollout speed: Medium (multiple waves).
- Rollback ease: High (revert last allowlist change).

Required CI/Test/Docs changes:
- CI: keep strict-lane step blocking; add optional metadata note for current wave in job name/comment.
- Tests: update allowlist contract test with each approved wave; keep smoke test deterministic.
- Docs: add wave schedule and PowerShell verification commands in project/test artifacts and setup notes.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Allowlist expands to unstable modules, causing merge friction | M | M | PR-gated structure test diff on allowlist plus targeted module pilot run |
| Silent allowlist drift without project approval | M | H | Existing exact-match allowlist contract test must fail on unapproved changes |
| Developers cannot reproduce lane failures locally | M | M | PowerShell command snippets validated in docs and smoke test command examples |

### Option B - Package-Level Strict for `src/core/**` with Temporary Exclusion File
Approach:
- Switch strict lane from explicit file allowlist to package scope (`src/core/**`).
- Maintain a temporary exclusion list (`exclude` or per-module relaxations) that shrinks over time.
- Keep CI blocking strict lane for whole package scope.

Research task types used:
- Alternative enumeration: broader enforcement with carved-out exceptions.
- Literature review: current config style and existing tests.
- Constraint mapping: faster coverage but potentially higher breakage.
- Stakeholder impact: higher pressure on @6code and @7exec due to wider surface.
- Risk enumeration: see table below.

Workspace evidence:
- `mypy.ini`
- `mypy-strict-lane.ini`
- `tests/structure/test_ci_yaml.py`

Trade-offs:
- Safety: Medium (wider initial blast radius).
- Developer friction: High (many files become actionable quickly).
- CI stability: Medium-Low (risk of frequent red builds early).
- Rollout speed: High (coverage grows quickly).
- Rollback ease: Medium (needs coordinated exclude reset).

Required CI/Test/Docs changes:
- CI: keep blocking step; consider dedicated strict job with explicit annotations for excluded paths.
- Tests: replace exact allowlist lock with contract asserting package scope + explicit exclusion governance.
- Docs: define exclusion lifecycle policy (owner, expiry, removal criteria) and local PowerShell commands.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Exclusion list grows and never shrinks | H | H | Structure test requiring max exclusion count and timestamped ownership comments |
| Frequent CI instability from broad surface | M | H | Track strict-lane failure rate per week; require stabilization threshold before expanding |
| Hidden regressions in excluded modules | M | M | Add periodic non-blocking report job over excluded set for visibility |

### Option C - Two-Lane Ratchet (Blocking strict lane + non-blocking core report lane)
Approach:
- Keep current blocking strict allowlist lane.
- Add second non-blocking report lane for broader `src/core/**` type state.
- Ratchet policy: every sprint, move a fixed set from report lane into blocking allowlist.

Research task types used:
- Alternative enumeration: dual-lane transitional governance model.
- Prior-art search: deterministic gate philosophy from architecture/testing doc and existing structure tests.
- Constraint mapping: aligns with CI shard architecture by adding one focused reporting step.
- Stakeholder impact: smoother transition for contributors and reviewers.
- Risk enumeration: see table below.

Workspace evidence:
- `.github/workflows/ci.yml`
- `docs/architecture/archive/8testing-quality.md`
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.plan.md`

Trade-offs:
- Safety: High (blocking lane remains constrained).
- Developer friction: Medium-Low (visibility before hard enforcement).
- CI stability: High (only strict allowlist blocks).
- Rollout speed: Medium-High (ratchet can be regular and measurable).
- Rollback ease: High (pause ratchet without removing hard gate).

Required CI/Test/Docs changes:
- CI: add a second, non-blocking report step for broader scope and publish summary.
- Tests: keep existing strict-lane contract tests; add structure test for report-lane presence and non-blocking semantics.
- Docs: define ratchet cadence, promotion criteria, and rollback trigger in project artifacts.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Report lane ignored because it is non-blocking | M | M | Require trend delta in CI summary and fail governance test if no ratchet movement for N sprints |
| Ratchet moves too quickly and destabilizes strict lane | M | H | Per-wave cap test and checklist in project test artifact before promotion |
| CI time increases beyond acceptable window | M | M | Track CI duration budget and enforce threshold alerts in workflow metrics |

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| Safety | 5/5 | 3/5 | 4/5 |
| Developer friction | 3/5 | 2/5 | 4/5 |
| CI stability | 5/5 | 3/5 | 4/5 |
| Rollout speed | 3/5 | 5/5 | 4/5 |
| Rollback ease | 5/5 | 3/5 | 5/5 |
| Fit with existing strict-lane tests | 5/5 | 3/5 | 4/5 |
| Overall practical fit | 5/5 | 3/5 | 4/5 |

## Recommendation
**Recommended: Option A - Explicit Allowlist Waves.**

Rationale:
1. It best matches the repository's proven strict-lane governance model already implemented in prior art.
2. It gives high safety and rollback control while preserving CI determinism.
3. It minimizes developer disruption by controlling strictness expansion to vetted slices.

Historical prior-art references:
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.design.md`
- `docs/architecture/archive/8testing-quality.md`

Staged rollout milestones:
1. Milestone R1 (Week 1): Baseline verification
	- Re-confirm strict lane and guard tests are green.
	- Document current allowlist as Wave 0 baseline.
2. Milestone R2 (Week 2): Wave 1 expansion
	- Add one low-churn `src/core` slice to allowlist.
	- Update structure test expected allowlist and validate CI stability.
3. Milestone R3 (Week 3): Wave 2 expansion
	- Add second slice only if Wave 1 meets CI stability and remediation SLO.
4. Milestone R4 (Week 4): Governance hardening
	- Add explicit rollback playbook and PowerShell local runbook updates.
5. Milestone R5 (Next cycle): Evaluate transition to Option C hybrid reporting lane if expansion throughput stalls.

Recommendation risk-to-testability mapping:
| Recommendation risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Expansion cadence too slow for target timeline | M | M | Milestone gate requiring minimum modules promoted per cycle |
| Expansion includes unstable modules | M | H | Pre-promotion checklist + targeted strict run on candidate slice |
| Rollback executed without artifact sync | L | H | Structure test requiring allowlist/docs consistency before merge |

## Open Questions
1. Which exact `src/core/**` subpaths should be Wave 1 in prj0000094 (lowest churn, highest value)?
2. Should CI strict lane remain in the shard job or move to a dedicated pre-shard job for clearer failure signal?
3. Do we codify a max-allowed strict-lane CI duration budget before each wave promotion?
4. Should project docs include a standardized PowerShell script snippet for local strict-lane triage?

## Handoff
Next target agent: `@3design`.
Design input: adopt Option A with the milestone sequence above, define concrete Wave 1 module set, and specify exact CI/test/doc deltas for implementation planning.
