# mypy-strict-enforcement - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-04_

## Overview
Execution-ready roadmap for progressive strict mypy enforcement beginning with a bounded `src/core` allowlist, using explicit config authority and a warn-to-required promotion path.

Primary rollout goals:
1. Keep broad typing visibility in warning mode.
2. Enforce strict typing in a bounded allowlist with deterministic commands.
3. Promote strict lane from warning to required only after stability evidence.
4. Preserve rollback safety at lane level (required -> warning), not policy abandonment.

Inputs used:
- `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.think.md`
- `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.design.md`
- `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.project.md`
- `mypy.ini`
- `pyproject.toml`

## Branch Gate
- Project ID: `prj0000127`
- Expected branch: `prj0000127-mypy-strict-enforcement`
- Observed branch: `prj0000127-mypy-strict-enforcement`
- Result: PASS

## Implementation Chunks
- Chunk A (warn phase): T-MYPY-001..T-MYPY-006
- Chunk B (required phase): T-MYPY-007..T-MYPY-010

Planned file volume stays within the @4plan chunk boundary target (about 10 code and 10 test artifacts per chunk) by limiting scope to one workflow file, config artifacts, one docs policy test file, and project handoff artifacts.

## RED/GREEN and Owner Model
- RED tasks: owned by `@5test` (create failing-first governance/contract tests).
- GREEN tasks: owned by `@6code` (make strict lane and workflow/config contracts pass).
- EXEC tasks: owned by `@7exec` (run phase gates and produce execution evidence).

## Phase Plan
### Phase W1 - Warn Lane Contract (non-blocking)
Goal: make command/config/allowlist contracts explicit and testable while strict lane remains warning-only.

### Phase W2 - Warn Lane Stabilization
Goal: run repeated warn-lane checks and freeze promotion criteria and rollback checkpoints.

### Phase R1 - Required Lane Promotion
Goal: promote strict allowlist lane from warning to required after passing the defined consecutive-green threshold.

### Phase R2 - Required Lane Steady-State
Goal: keep strict allowlist required, preserve broad lane warning-only, and validate rollback readiness.

## Task List
All tasks satisfy mandatory schema: objective, target files, acceptance criteria, validation command.

| Task ID | Mode | Parallel Class | Owner | Objective | Target Files | Acceptance Criteria | Validation Command | Rollback Checkpoint |
|---|---|---|---|---|---|---|---|---|
| T-MYPY-001 | RED | parallel-safe | @5test | Add failing-first docs governance tests that assert strict-lane contract includes explicit config source and phase-1 allowlist entries. | `tests/docs/test_agent_workflow_policy_docs.py`, `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.plan.md` | Test fails until plan defines strict-lane command, explicit `--config-file`, and all phase-1 allowlist files from design. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -k "prj0000127 or mypy"` | If unstable selector behavior appears, hold on warning mode and keep gate non-required. |
| T-MYPY-002 | RED | parallel-safe | @5test | Add failing-first docs test coverage for warn-to-required promotion policy and consecutive-green threshold contract (`N=5`). | `tests/docs/test_agent_workflow_policy_docs.py`, `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.plan.md` | Test fails until plan contains explicit `N=5` promotion threshold and required preconditions. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -k "prj0000127 or promotion or mypy"` | If evidence cannot be produced for five consecutive runs, remain in warn phase. |
| T-MYPY-003 | RED | sequential-only | @5test | Converge RED slices into one handoff artifact for `@6code` with deterministic failing selectors and ownership boundaries. | `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.test.md` | Handoff doc records failing selectors for T-MYPY-001 and T-MYPY-002; no overlap with implementation-owned files. | `rg -n "T-MYPY-001|T-MYPY-002|failing|selector" docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.test.md` | If overlap is found, reject handoff and keep RED phase open. |
| T-MYPY-004 | GREEN | parallel-safe | @6code | Implement strict allowlist command contract in CI as warning-only lane with explicit config authority and deterministic target list. | `.github/workflows/ci.yml`, `pyproject.toml` | CI includes strict allowlist command with `--config-file pyproject.toml`; check runs in warn mode and publishes diagnostics without failing merge. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m mypy --config-file pyproject.toml src/core/base/mixins/base_behavior_mixin.py src/core/base/mixins/host_contract.py src/core/base/mixins/shim_registry.py src/core/agent_registry.py src/core/agent_state_manager.py` | F1 rollback trigger: if config authority is ambiguous, revert to last known-good warn-only command block. |
| T-MYPY-005 | GREEN | parallel-safe | @6code | Preserve broad visibility lane in warning mode and make command distinction explicit from strict lane. | `.github/workflows/ci.yml`, `mypy.ini` | Broad lane remains non-blocking and does not mask strict allowlist regressions. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m mypy --config-file mypy.ini src` | If broad lane noise spikes and obscures strict-lane signal, narrow broad lane target list but keep strict lane unchanged. |
| T-MYPY-006 | GREEN | sequential-only | @6code | Document rollback taxonomy and promotion/rollback runbook in project artifacts. | `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md`, `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.plan.md` | Runbook includes F1/F2/F3 classes, required->warning downgrade process, and re-promotion rules. | `rg -n "F1|F2|F3|required -> warning|re-promotion|N=5" docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.plan.md docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md` | If rollback steps are missing or incomplete, do not promote to required. |
| T-MYPY-007 | EXEC | sequential-only | @7exec | Execute warn-phase gate repeatedly and capture promotion evidence. | `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md` | Evidence shows five consecutive green strict-lane runs (`N=5`) and passing docs policy selector. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | If any run fails, reset consecutive-green count to zero and remain warning-only. |
| T-MYPY-008 | GREEN | sequential-only | @6code | Promote strict allowlist lane from warning to required status in CI after T-MYPY-007 evidence. | `.github/workflows/ci.yml`, `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md` | Strict allowlist check is required for PR merge on target branch; broad lane remains warning-only. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -k "prj0000127 or mypy"` | If required gate causes sustained flakiness (F3), downgrade strict lane back to warning mode and document incident. |
| T-MYPY-009 | EXEC | sequential-only | @7exec | Validate required-phase behavior and rollback readiness with focused lane checks and docs policy gate. | `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md`, `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.ql.md` | Required strict lane is stable; rollback criteria remain testable and documented. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | If instability appears, execute lane-level rollback and keep evidence in exec artifact. |
| T-MYPY-010 | EXEC | sequential-only | @7exec | Freeze phased rollout completion state and hand off expansion readiness notes for next project slice. | `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md`, `docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.project.md` | Exec artifact includes final status for warn phase and required phase, plus explicit “expand allowlist later” boundary. | `rg -n "warn phase|required phase|expansion" docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md` | If expansion readiness is ambiguous, keep scope closed to phase-1 allowlist only. |

## Parallel Planning Boundaries
### Parallel-safe tasks
- `T-MYPY-001` and `T-MYPY-002` are parallel-safe (same file, but non-overlapping assertions and selector focus).
- `T-MYPY-004` and `T-MYPY-005` are parallel-safe (shared workflow context, distinct lane responsibilities).

### Sequential-only tasks
- `T-MYPY-003`, `T-MYPY-006`, `T-MYPY-007`, `T-MYPY-008`, `T-MYPY-009`, `T-MYPY-010`.

### Convergence step
- Convergence owner: `@0master` decision, execution by assigned phase owner.
- Required convergence checkpoints:
	1. RED convergence: complete `T-MYPY-003` before any GREEN task begins.
	2. Warn convergence: complete `T-MYPY-007` before required-phase promotion in `T-MYPY-008`.

## Warn-to-Required Rollout Contract
1. Warn phase active by default.
2. Strict lane remains non-blocking until exactly five consecutive green runs are recorded (`N=5`).
3. Promotion to required is a discrete change after evidence capture.
4. Broad lane remains warning-only throughout this project.
5. Any F1 or F3 class incident triggers required -> warning rollback.

## Warn-Phase Runbook Notes (T-MYPY-006)
- F1: Config authority mismatch for strict lane command/config source.
- F2: Deterministic strict-allowlist regression.
- F3: CI instability or flapping in strict lane outcomes.
- Promotion prerequisite marker: `N=5` consecutive green strict-lane runs in warn mode.
- This warn-phase slice does not perform required-phase promotion.

## Rollback Checkpoints
| Checkpoint | Trigger | Action | Re-entry Condition |
|---|---|---|---|
| RC-1 | F1 config authority mismatch | Revert strict lane to last known-good warning command and document incident. | Config precedence assertion passes and docs policy gate is green. |
| RC-2 | F2 strict-lane regression in allowlist | Keep required gate if deterministic fix is immediate; otherwise temporarily downgrade to warning with owner/expiry note. | Targeted strict selector passes and no open regression in allowlist. |
| RC-3 | F3 CI instability/flapping | Downgrade strict lane required -> warning; preserve diagnostics. | New set of five consecutive green runs (`N=5`) in warn mode. |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | RED governance contracts prepared | T-MYPY-001..T-MYPY-003 | PLANNED |
| M2 | Warn phase implemented and stabilized | T-MYPY-004..T-MYPY-007 | PLANNED |
| M3 | Required phase promoted and validated | T-MYPY-008..T-MYPY-010 | PLANNED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Branch gate
git branch --show-current

# Docs policy gate (mandatory for project artifact updates)
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# Strict allowlist lane command (explicit strict config authority)
python -m mypy --config-file pyproject.toml src/core/base/mixins/base_behavior_mixin.py src/core/base/mixins/host_contract.py src/core/base/mixins/shim_registry.py src/core/agent_registry.py src/core/agent_state_manager.py

# Broad warning lane command (explicit permissive config)
python -m mypy --config-file mypy.ini src
```

## First Handoff Slice to @5test
Start with RED tasks in this order:
1. `T-MYPY-001`
2. `T-MYPY-002`
3. `T-MYPY-003` convergence

No GREEN task may start until `T-MYPY-003` confirms failing selectors and ownership boundaries.


