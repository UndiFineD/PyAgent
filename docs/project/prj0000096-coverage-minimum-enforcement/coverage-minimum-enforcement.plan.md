# coverage-minimum-enforcement - Implementation Plan

_Status: HANDED_OFF_
_Planner: @4plan | Updated: 2026-03-28_

## Overview
Implement slice 1 of coverage minimum enforcement using a strict TDD sequence:
1. Add failing guard tests first.
2. Implement the smallest CI/config changes to pass those tests.
3. Record rollout evidence format for deterministic ratchet governance.

This plan intentionally limits scope to the first ratchet stage (`fail_under = 40`) in one coding wave.

## Slice Scope (Wave 1)
In scope:
1. Add blocking CI coverage-gate assertions.
2. Raise threshold from 30 to 40 in one source of truth.
3. Preserve workflow-count constraints.
4. Record stage-1 baseline evidence format.

Out of scope:
1. Stage-2 and Stage-3 threshold promotions.
2. Per-package floors.
3. New workflow files or broad CI refactors.

## Task List (TDD-First, Slice 1)
| Task ID | Owner | Objective | Target Files (exact) | Acceptance Criteria | Validation Command (PowerShell) | Status | Milestone |
|---|---|---|---|---|---|---|---|
| T1 | @5test | Add failing structure tests that require a blocking coverage gate in CI and reject soft-fail operators. | `tests/structure/test_ci_yaml.py` | Tests fail when gate is missing or when `continue-on-error`, `|| true`, `||true`, or `set +e` appears in gate path. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py` | READY | M1 |
| T2 | @5test | Add failing config tests for threshold source-of-truth and stage-1 target value. | `tests/test_coverage_config.py` | Tests require `[tool.coverage.report].fail_under` to be present and equal to stage-1 value (40) and fail on drift. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/test_coverage_config.py` | READY | M1 |
| T3 | @6code | Implement blocking CI coverage gate in existing `CI (minimal)` workflow job without adding workflows. | `.github/workflows/ci.yml` | T1 passes; gate runs in existing workflow path and remains blocking. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py` | READY | M2 |
| T4 | @6code | Set stage-1 threshold in canonical config and keep command/config linkage deterministic. | `pyproject.toml`, `.github/workflows/ci.yml` | T2 passes; `fail_under = 40` is the single policy knob for threshold management. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/test_coverage_config.py tests/structure/test_ci_yaml.py` | READY | M2 |
| T5 | @6code | Record stage-1 baseline evidence and ratchet promotion/rollback evidence format for operations handoff. | `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md` | Artifact contains canonical measurement command, stage value (40), and promotion/pause/rollback evidence fields. | `Select-String -Path docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md -Pattern "stage|fail_under|promotion|rollback"` | READY | M3 |

## Dependency Order
1. T1 -> T2
2. T1/T2 must be committed by @5test before @6code starts implementation.
3. T3 -> T4
4. T5 runs after T3/T4 are green to capture actual executed evidence format.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Red TDD guards authored by @5test | T1-T2 | READY_FOR_@5TEST |
| M2 | Minimal implementation to green by @6code | T3-T4 | READY_FOR_@6CODE_AFTER_M1 |
| M3 | Governance evidence format recorded | T5 | READY_FOR_@6CODE_AFTER_M2 |

## Handoff Contract
1. Handoff target: `@5test` for T1-T2 only.
2. `@6code` must not start T3-T5 until T1-T2 exist and fail for the expected reasons.
3. No file edits outside this slice's target files.

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/structure/test_ci_yaml.py
python -m pytest -q tests/test_coverage_config.py
python -m pytest -q tests/ci/test_workflow_count.py
python -m pytest -q tests/structure/test_ci_yaml.py tests/test_coverage_config.py tests/ci/test_workflow_count.py
Select-String -Path docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md -Pattern "stage|fail_under|promotion|rollback"
```
