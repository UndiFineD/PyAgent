# coverage-minimum-enforcement - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-05_

## Overview
Execution-ready roadmap for reconnecting the existing coverage baseline in `pyproject.toml` to one dedicated blocking CI job without broadening this project into a general workflow redesign.

Primary rollout goals:
1. Preserve `jobs.quick` as the lightweight hygiene lane.
2. Add exactly one required `coverage` job in `.github/workflows/ci.yml`.
3. Keep `[tool.coverage.report].fail_under = 40` as the only threshold authority.
4. Encode fail-closed workflow-shape and command-contract checks before implementation begins.
5. Constrain rollback to threshold-only correction if runtime evidence proves the current floor invalid.

Inputs used:
- `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md`
- `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.design.md`
- `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.project.md`
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/structure/test_ci_yaml.py`
- `tests/test_coverage_config.py`

## Branch Gate
- Project ID: `prj0000128`
- Expected branch: `prj0000128-coverage-minimum-enforcement`
- Observed branch: `prj0000128-coverage-minimum-enforcement`
- Result: PASS

## Implementation Chunks
- Chunk A (single bounded slice): `T-COV-001..T-COV-006`

Planned file volume stays within the @4plan chunk boundary target because the rollout is limited to one workflow file, two existing test files, and project handoff artifacts.

## RED/GREEN and Owner Model
- RED tasks: owned by `@5test`.
- GREEN tasks: owned by `@6code`.
- EXEC tasks: owned by `@7exec`.

Dependency order:
`T-COV-001 || T-COV-002` -> `T-COV-003` -> `T-COV-004` -> `T-COV-005` -> `T-COV-006`

## Warn/Required Distinction
This rollout has no warn phase for coverage enforcement.

Required behavior for this slice:
1. The new `coverage` job is blocking from its first implementation commit.
2. Existing warn-only mypy lanes remain unchanged and are out of scope.
3. No temporary `continue-on-error`, `|| true`, or threshold duplication is allowed to simulate a soft launch.

## Task List
All tasks include objective, target files, acceptance criteria, validation command, and rollback checkpoint.

| Task ID | Mode | Parallel Class | Owner | Objective | Target Files | Acceptance Criteria | Validation Command | Rollback Checkpoint |
|---|---|---|---|---|---|---|---|---|
| T-COV-001 | RED | parallel-safe | @5test | Replace stale absence assertions with workflow-shape tests that require exactly one `coverage` job and preserve `jobs.quick`. | `tests/structure/test_ci_yaml.py` | Tests fail until CI defines one `coverage` job, `jobs.quick` still exists, and `coverage.needs` requires `quick`. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py -k "coverage or quick"` | If selector proves too broad or noisy, narrow the assertion surface before any GREEN work starts. |
| T-COV-002 | RED | parallel-safe | @5test | Add fail-closed command-contract tests for the dedicated coverage path. | `tests/structure/test_ci_yaml.py` | Tests fail until the workflow requires the canonical pytest-cov markers (`--cov=src`, `--cov-branch`, `--cov-config=pyproject.toml`, `--cov-report=term-missing`, `--cov-report=xml`) and rejects `--cov-fail-under`, `continue-on-error`, `|| true`, and `set +e`. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py -k "coverage and blocking"` | If canonical-command detection creates false positives, prefer explicit job-name plus flag assertions rather than weakening the fail-closed contract. |
| T-COV-003 | RED | sequential-only | @5test | Converge RED evidence and confirm config-authority coverage remains anchored to `pyproject.toml`. | `tests/test_coverage_config.py`, `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md` | `tests/test_coverage_config.py` continues to enforce `fail_under >= 40`; handoff notes capture the failing selectors for `T-COV-001` and `T-COV-002` and state that coverage has no warn phase. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/test_coverage_config.py` | If config-authority assertions need expansion, add them without moving threshold ownership out of `pyproject.toml`. |
| T-COV-004 | GREEN | sequential-only | @6code | Add the dedicated blocking `coverage` job to the existing workflow with `needs: quick` and the canonical pytest-cov command. | `.github/workflows/ci.yml` | Workflow contains exactly one `coverage` job, keeps `quick` intact, uses the canonical command, and does not hardcode `--cov-fail-under`. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py` | If the gate fails because the baseline is invalid, rollback may adjust only `[tool.coverage.report].fail_under`; the `coverage` job must remain present and blocking. |
| T-COV-005 | EXEC | sequential-only | @7exec | Produce deterministic local evidence that workflow-shape and config-authority selectors pass after implementation. | `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.exec.md` | Execution artifact records passing results for `tests/structure/test_ci_yaml.py`, `tests/test_coverage_config.py`, and `tests/docs/test_agent_workflow_policy_docs.py`. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py; python -m pytest -q tests/test_coverage_config.py; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | If any selector is interrupted or inconclusive, re-run the exact failed selector first and do not mark execution done. |
| T-COV-006 | EXEC | sequential-only | @7exec | Capture runtime coverage-gate evidence and freeze rollback disposition for downstream quality/git handoff. | `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.exec.md`, `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.project.md` | Execution artifact records the canonical coverage command outcome and whether rollback is unnecessary or threshold-only; project status reflects that the design shipped as required coverage enforcement with no warn phase. | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest tests -q --cov=src --cov-branch --cov-config=pyproject.toml --cov-report=term-missing --cov-report=xml` | If runtime evidence shows tooling or baseline mismatch, document the incident and apply only threshold-level rollback; never remove or soften the coverage job. |

## Parallel Planning Boundaries
### Parallel-safe tasks
- `T-COV-001` and `T-COV-002` are parallel-safe because they share one test file but assert disjoint contracts: workflow shape vs fail-closed command semantics.

### Sequential-only tasks
- `T-COV-003`, `T-COV-004`, `T-COV-005`, `T-COV-006`.

### Convergence step
- Convergence owner: `@0master`.
- Required convergence checkpoint: complete `T-COV-003` before `T-COV-004` begins.

## Rollback Checkpoints
| Checkpoint | Trigger | Action | Re-entry Condition |
|---|---|---|---|
| RC-COV-1 | RED selectors detect the wrong workflow surface or ambiguous command matching | Narrow test predicates to the dedicated `coverage` job and rerun RED selectors before GREEN handoff. | `tests/structure/test_ci_yaml.py` fails only on intended coverage-gate expectations. |
| RC-COV-2 | Implemented gate fails because `fail_under = 40` is proven invalid due measurement/tooling error | Roll back only `[tool.coverage.report].fail_under` to the last known-good integer and keep the `coverage` job blocking. | `tests/test_coverage_config.py` and the canonical coverage command both pass on the revised floor. |
| RC-COV-3 | Runtime validation is flaky or inconclusive | Re-run the exact failing selector or command and keep the gate blocking; do not introduce warn-only behavior. | One complete, conclusive passing run exists for all required selectors and the canonical coverage command. |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | RED contracts prepared | T-COV-001..T-COV-003 | PLANNED |
| M2 | Coverage job implemented | T-COV-004 | PLANNED |
| M3 | Execution evidence recorded | T-COV-005..T-COV-006 | PLANNED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Branch gate
git branch --show-current

# Docs policy gate (mandatory for this plan update and later exec handoff)
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# Workflow structure gate
python -m pytest -q tests/structure/test_ci_yaml.py

# Coverage config authority gate
python -m pytest -q tests/test_coverage_config.py

# Canonical runtime command
python -m pytest tests -q --cov=src --cov-branch --cov-config=pyproject.toml --cov-report=term-missing --cov-report=xml
```

## First Handoff Slice to @5test
Start with RED tasks in this order:
1. `T-COV-001`
2. `T-COV-002`
3. `T-COV-003`

No GREEN work may begin until `T-COV-003` records the failing selectors and confirms that coverage enforcement ships as required-from-first-merge behavior.


