# prj0000094-idea-003-mypy-strict-enforcement - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-28_

## Selected Option
Option A - Explicit Allowlist Waves.

Rationale:
1. Preserves the proven strict-lane governance pattern already enforced by existing structure tests and CI checks.
2. Provides deterministic, low-risk strictness expansion using explicit allowlist changes instead of broad package flips.
3. Supports fast rollback by reverting a single `files` expansion in `mypy-strict-lane.ini`.

## Problem Statement And Goals
Current strict-lane enforcement is real but narrow: it blocks CI with a fixed 6-file allowlist in `mypy-strict-lane.ini`.
The design objective is to scale strictness with explicit governance waves while preserving CI determinism, local reproducibility, and low blast radius.

Goals:
1. Define a wave model for expanding strict-lane coverage in `src/core/**`.
2. Keep the CI strict-lane command blocking and contract-tested.
3. Add explicit gating and rollback criteria per wave.
4. Add observability signals for wave health and rollout confidence.

Non-goals:
1. Flip global strictness in `mypy.ini`.
2. Replace the current CI shard architecture.
3. Enforce strict typing for all repository modules in this project.

## Architecture
### Enforcement Topology
1. Baseline lane remains active and blocking:
	- CI command: `python -m mypy --config-file mypy-strict-lane.ini`.
2. Strict-lane scope is expanded only through explicit wave updates to `[mypy] files` in `mypy-strict-lane.ini`.
3. Structure tests remain the control plane for configuration drift prevention.
4. Smoke tests remain the behavioral guard to ensure strict-lane failures are surfaced deterministically.

### Wave Structure
Wave 0 (Baseline, already active):
1. Keep the current 6-file allowlist and existing CI/test contracts unchanged.

Wave 1 (Low-churn contracts and exceptions):
1. Expand allowlist with a small, explicit set of additional `src/core/**` files.
2. Keep expansion cap at a bounded set (default: <= 10 new files per wave unless waived in project artifact updates).

Wave 2 (Adjacent stable models/utilities):
1. Expand from Wave 1 into closely related, low-churn modules with clear type boundaries.
2. Preserve a single blocking lane, no dual-lane complexity in this project.

Wave 3 (Broader core slice):
1. Expand to the next vetted slice once Wave 2 gates pass.
2. End-state remains explicit allowlist governance, with future optional evaluation of hybrid reporting only after project completion.

### Gating Model
Each wave promotion requires all gates below:
1. Contract gate:
	- `tests/structure/test_mypy_strict_lane_config.py` must pass with updated expected allowlist.
2. CI wiring gate:
	- `tests/structure/test_ci_yaml.py` must pass and confirm blocking semantics are unchanged.
3. Behavioral gate:
	- `tests/zzz/test_zzc_mypy_strict_lane_smoke.py` remains deterministic (bad fixture still fails strict lane).
4. Stability gate:
	- No unresolved strict-lane CI failures for the current wave over the defined observation window (default: 5 consecutive green CI runs).
5. Repro gate:
	- Local PowerShell command remains valid and documented:
	  `python -m mypy --config-file mypy-strict-lane.ini`

## Interfaces & Contracts
### IFC-01 Strict Lane Configuration Contract
Files:
1. `mypy-strict-lane.ini`
2. `tests/structure/test_mypy_strict_lane_config.py`

Contract:
1. `[mypy] strict = True`
2. `[mypy] ignore_errors = False`
3. `[mypy] show_error_codes = True`
4. `[mypy] warn_unused_ignores = True`
5. `[mypy] files` is an explicit ordered allowlist governed by wave updates.
6. Expected allowlist in the structure test must exactly match the config value after normalization.

### IFC-02 CI Enforcement Contract
Files:
1. `.github/workflows/ci.yml`
2. `tests/structure/test_ci_yaml.py`

Contract:
1. CI includes strict-lane command:
	- `python -m mypy --config-file mypy-strict-lane.ini`
2. Command stays blocking:
	- no `continue-on-error`
	- no `|| true` / `||true`
	- no `set +e`
3. Strict-lane execution remains part of canonical CI test workflow behavior.

### IFC-03 Strict-Lane Behavioral Contract
Files:
1. `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`
2. `tests/fixtures/mypy_strict_lane/bad_case.py`

Contract:
1. Strict-lane invocation against known-bad fixture exits non-zero.
2. Output contains fixture reference and a concrete error marker.
3. Missing mypy dependency is treated as explicit skip behavior (not false pass).

### IFC-04 Wave Governance Metadata Contract
Project artifact files:
1. `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.design.md`
2. `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.plan.md`
3. `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.test.md`

Contract:
1. Every wave defines:
	- candidate file set,
	- promotion gates,
	- rollback trigger.
2. Traceability table maps each interface and AC to implementation task IDs for @4plan.

## Verification Strategy (Design-Level)
This section defines required verification intent and ownership mapping for @4plan/@5test without prescribing implementation test code details.

1. Config contract verification:
	- Validate strict keys and exact allowlist lockstep between config and structure test.
2. CI enforcement verification:
	- Validate strict-lane command exists and remains blocking.
3. Behavioral verification:
	- Validate strict-lane catches deterministic bad fixture.
4. Wave gating verification:
	- Validate promotion only after contract, CI, behavior, and stability gates pass.

## Acceptance Criteria
| AC ID | Requirement | Contract(s) | Verification Anchor | Owner |
|---|---|---|---|---|
| AC-01 | Wave-based strict-lane expansion model is explicitly defined with promotion gates | IFC-04 | Design artifact section "Wave Structure" + "Gating Model" | @3design |
| AC-02 | Strict-lane config contract remains explicit and deterministic during wave updates | IFC-01 | `test_mypy_strict_lane_config.py` exact-allowlist checks | @5test |
| AC-03 | CI strict-lane command remains present and blocking for all waves | IFC-02 | `test_ci_yaml.py` blocking checks | @5test |
| AC-04 | Strict-lane behavioral failure remains deterministic | IFC-03 | `test_zzc_mypy_strict_lane_smoke.py` bad fixture failure | @5test/@7exec |
| AC-05 | Each wave has documented rollback trigger and rollback action path | IFC-04 | Design rollback section and plan/test artifact propagation | @4plan |
| AC-06 | Wave rollout exposes observable health signals for promotion decisions | IFC-02, IFC-03, IFC-04 | CI run outcomes + strict-lane failure trend notes | @7exec |
| AC-07 | Interface-to-task traceability exists for all contracts and ACs | IFC-01, IFC-02, IFC-03, IFC-04 | Traceability matrix in this design artifact | @3design/@4plan |

## Interface-To-Task Traceability (Handoff Seeds For @4plan)
| Interface/Contract | AC IDs | Task Seed ID | Planned Implementation Task |
|---|---|---|---|
| IFC-01 Strict Lane Configuration Contract | AC-02, AC-07 | TSK-A1 | Update `mypy-strict-lane.ini` allowlist per wave and update strict-lane config structure assertions |
| IFC-02 CI Enforcement Contract | AC-03, AC-06, AC-07 | TSK-A2 | Preserve/adjust CI strict-lane step naming or metadata without changing blocking semantics |
| IFC-03 Strict-Lane Behavioral Contract | AC-04, AC-07 | TSK-A3 | Keep smoke fixture contract deterministic while allowlist waves evolve |
| IFC-04 Wave Governance Metadata Contract | AC-01, AC-05, AC-06, AC-07 | TSK-A4 | Update project `design/plan/test` artifacts with wave candidate set, gate outcomes, and rollback notes |
| Wave 1 promotion package | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06 | TSK-A5 | Implement Wave 1 candidate expansion and execute all promotion gates |
| Wave 2 promotion package | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06 | TSK-A6 | Implement Wave 2 candidate expansion after Wave 1 stability window passes |
| Wave 3 promotion package | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06 | TSK-A7 | Implement Wave 3 candidate expansion after Wave 2 stability window passes |

## Rollback Plan
### Rollback Triggers
1. Strict-lane introduces repeated CI instability in current wave window.
2. Wave promotion causes blocking failures outside expected remediation budget.
3. Strict-lane command or contract tests need emergency stabilization.

### Rollback Actions
1. Revert only the most recent wave addition in `mypy-strict-lane.ini` `files`.
2. Revert matching expected allowlist updates in strict-lane structure tests.
3. Keep CI strict-lane step active and blocking unless emergency exception is explicitly approved in project artifacts.
4. Record rollback reason, impact, and re-entry condition in project plan/test artifacts.

### Roll-forward Condition
1. Root cause identified and documented.
2. Candidate set reduced or remediated.
3. Gates re-run and pass before re-attempting promotion.

## Observability Plan
### Required Signals
1. Strict-lane CI pass/fail per run (baseline signal).
2. Failure reason category (config drift, CI wiring drift, true typing failure).
3. Wave progression state (`Wave 0`, `Wave 1`, `Wave 2`, `Wave 3`) captured in project artifacts.
4. Consecutive-green counter used for promotion gate decisions.

### Operational Readout
1. CI provides immediate strict-lane outcome via existing blocking step.
2. Structure tests identify governance drift root cause quickly.
3. Smoke test identifies tooling/behavior regressions independent of allowlist growth.

### Minimal Metrics For Decisioning
1. `strict_lane_pass_rate` over observation window.
2. `strict_lane_failures_by_category` for triage.
3. `wave_promotion_lead_time` between wave readiness and gate completion.

## Non-Functional Requirements
- Performance:
  - Strict-lane runtime overhead should remain bounded and acceptable for current CI budget; wave size caps are used to control runtime growth.
- Security:
  - No secrets handling changes; enforcement uses static typing checks only and does not expand runtime attack surface.
- Testability:
  - Deterministic config, CI, and smoke contracts must continue to provide fast-fail diagnostics for wave governance.

## Policy Compliance
1. Code of conduct: design introduces no harmful or exclusionary process constraints.
2. Naming standards: all referenced files/tests/config paths follow current repository naming conventions and existing strict-lane test naming patterns.

## Open Questions For @4plan
1. Which exact `src/core/**` file set is approved for Wave 1 under low-churn criteria?
2. Should wave metadata be captured only in project artifacts, or additionally in CI step naming for quick visibility?
3. Is the default promotion window of 5 consecutive green runs acceptable, or should @4plan tune this threshold?

## Recommended Handoff
Next agent: @4plan.

Handoff objective:
1. Convert `TSK-A1` through `TSK-A7` into an implementation roadmap with explicit file-by-file changes and gate execution order.
2. Define concrete Wave 1 candidate files and rollback-ready sequencing.
3. Ensure test artifact updates preserve existing strict-lane contracts in `tests/structure` and `tests/zzz`.
