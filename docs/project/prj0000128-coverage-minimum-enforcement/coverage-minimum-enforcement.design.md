# coverage-minimum-enforcement - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-05_

## Policy Alignment
- Branch gate: PASS. Observed branch `prj0000128-coverage-minimum-enforcement` matches the expected branch in the project overview.
- Code of conduct: PASS. No scope or handoff behavior in this design conflicts with [docs/project/code_of_conduct.md](docs/project/code_of_conduct.md).
- Naming standards: PASS. The design keeps existing snake_case file names and uses a new CI job key that remains naming-compliant.
- ADR impact: none required for this slice. The change introduces a bounded CI enforcement path inside the existing workflow rather than a new architectural subsystem.

## Selected Option
Option B - add one dedicated blocking coverage job inside the existing `.github/workflows/ci.yml`.

Rationale:
1. The original idea is partially stale. The repository already enforces `[tool.coverage.report].fail_under = 40` in `pyproject.toml`, so the current gap is not threshold absence.
2. The real defect is enforcement drift: the active lightweight CI workflow does not execute a blocking coverage path, so the configured floor is never exercised in required CI.
3. A dedicated `coverage` job is the smallest valuable next slice because it restores blocking enforcement without changing the meaning of the existing `quick` job.

## Stale-Idea Reconciliation
Historical premise from `idea000008`:
- Coverage enforcement was described as effectively non-enforcing because CI behavior and threshold policy had drifted apart.

Current repository truth:
- `pyproject.toml` already defines `fail_under = 40`.
- `tests/test_coverage_config.py` already protects the existence and minimum baseline of that threshold.
- `.github/workflows/ci.yml` still lacks a blocking coverage execution path.
- `tests/structure/test_ci_yaml.py` currently encodes the stale assumption by asserting that lightweight CI should not contain any coverage gate path.

Design consequence:
- This project must not raise the threshold or redesign CI broadly.
- This project must reconnect CI to the already-configured `40` baseline with one explicit blocking job and aligned structure tests.

## Scope
In scope:
1. Add one dedicated blocking `coverage` job to `.github/workflows/ci.yml`.
2. Keep `[tool.coverage.report].fail_under = 40` unchanged and treat it as the only threshold authority.
3. Define one canonical coverage command that consumes `pyproject.toml` rather than hardcoding a second threshold value in YAML.
4. Replace the stale CI structure expectation with tests that require one blocking coverage job.
5. Define rollback boundaries that preserve the gate while allowing bounded reversion of the baseline if the signal proves invalid.

Out of scope:
1. Raising the coverage baseline above `40`.
2. Splitting CI into additional workflow files or redesigning unrelated jobs.
3. Introducing per-package coverage floors.
4. Changing local developer workflows beyond documenting the canonical command.
5. Defining the full implementation task plan. That belongs to @4plan.

## Non-Goals
1. Do not make `quick` the coverage job.
2. Do not duplicate the threshold in workflow YAML with `--cov-fail-under=40`.
3. Do not turn warn-only mypy lanes into required gates as part of this project.
4. Do not broaden the project into a general CI modernization effort.

## Architecture
### High-Level Design
The workflow remains a single file, but it gains a second explicit blocking path:

1. `jobs.quick` stays responsible for fast hygiene checks and existing lightweight signals.
2. New `jobs.coverage` runs after `quick` via `needs: quick`.
3. `coverage` installs the same Python dependencies as `quick`, then executes one canonical coverage-producing pytest command.
4. `pytest-cov` reads coverage settings from `pyproject.toml`, including `[tool.coverage.report].fail_under = 40`.
5. Any test failure or coverage shortfall causes the `coverage` job to fail, which fails the workflow.

### Workflow Shape Contract
Required workflow shape in `.github/workflows/ci.yml`:
- Keep the existing `quick` job.
- Add exactly one job named `coverage`.
- Set `coverage.needs: quick`.
- Do not add `continue-on-error: true` at the job or step level for the coverage path.
- Do not add a second coverage-producing job or a second threshold gate inside `quick`.

### Canonical Coverage Command
The coverage job must run exactly one canonical command surface:

```text
python -m pytest tests -q --cov=src --cov-branch --cov-config=pyproject.toml --cov-report=term-missing --cov-report=xml
```

Command contract:
1. `--cov=src` keeps measurement aligned with `[tool.coverage.run].source = ["src"]`.
2. `--cov-branch` matches the configured branch coverage expectation.
3. `--cov-config=pyproject.toml` removes ambiguity about config discovery.
4. No `--cov-fail-under` flag is allowed in YAML, because the threshold must come from `pyproject.toml`.
5. XML output is allowed for downstream tooling, but no extra post-processing step is required in this slice.

### Pass/Fail Semantics
The new `coverage` job is fail-closed:

Pass when all conditions are true:
1. Dependency installation succeeds.
2. The canonical pytest command exits `0`.
3. Total measured coverage satisfies the current baseline from `pyproject.toml`.

Fail when any condition is true:
1. Pytest exits non-zero because tests fail.
2. Coverage exits non-zero because measured total is below `fail_under = 40`.
3. The workflow uses a soft-fail pattern such as `continue-on-error`, `|| true`, `set +e`, or equivalent shell suppression on the coverage path.

Blocking semantics:
1. The workflow must expose `coverage` as a distinct required status check candidate.
2. Repository policy can mark that job required at the branch-protection layer, but the repository-local contract here is that the job itself fails hard and therefore blocks the workflow.

### Rollback Path
Rollback is bounded and must preserve enforcement:

Allowed rollback:
1. Revert only the baseline value in `[tool.coverage.report].fail_under` to the previous known-good value if the 40 baseline proves invalid due to measurement/tooling error.
2. Keep the `coverage` job present and blocking.
3. Record the reason, owner, and re-promotion condition in downstream project/test artifacts.

Forbidden rollback:
1. Removing the `coverage` job.
2. Moving the gate to a warning-only mode.
3. Reintroducing duplicate threshold constants in workflow YAML.

## Interfaces & Contracts
| Interface ID | Contract | Input | Output | Owner (next) |
|---|---|---|---|---|
| IFACE-COV-001 | CI coverage job contract | `.github/workflows/ci.yml` job graph | one blocking `coverage` job with `needs: quick` | @4plan/@6code |
| IFACE-COV-002 | Canonical coverage command contract | coverage job run command | deterministic pytest-cov invocation using `pyproject.toml` | @4plan/@6code |
| IFACE-COV-003 | Threshold authority contract | `[tool.coverage.report].fail_under` | single source of truth for baseline enforcement | @4plan/@5test |
| IFACE-COV-004 | Blocking semantics contract | job/step YAML flags and shell command shape | failure on tests, failure on low coverage, no soft-fail path | @4plan/@5test/@7exec |
| IFACE-COV-005 | CI structure guard contract | `tests/structure/test_ci_yaml.py` | tests fail if coverage job is missing, duplicated, or softened | @4plan/@5test |
| IFACE-COV-006 | Config guard contract | `tests/test_coverage_config.py` | tests fail if the baseline drops below 40 or config authority drifts | @4plan/@5test |
| IFACE-COV-007 | Rollback contract | rollback trigger evidence | bounded threshold-only rollback while preserving gate presence | @4plan/@7exec |

## Planned Implementation Tasks (for @4plan decomposition)
| Task ID | Description | Primary artifacts |
|---|---|---|
| TSK-COV-01 | Add the dedicated blocking `coverage` job to the existing workflow with `needs: quick` | `.github/workflows/ci.yml` |
| TSK-COV-02 | Install the canonical coverage command without duplicating the threshold in YAML | `.github/workflows/ci.yml` |
| TSK-COV-03 | Update CI structure tests from stale absence assertions to explicit presence/blocking assertions | `tests/structure/test_ci_yaml.py` |
| TSK-COV-04 | Keep config authority anchored to `pyproject.toml` and confirm the 40 baseline remains the active floor | `pyproject.toml`, `tests/test_coverage_config.py` |
| TSK-COV-05 | Add rollback/runbook notes and executable validation commands to downstream project artifacts | `docs/project/prj0000128-coverage-minimum-enforcement/*` |

## Interface-to-Task Traceability
| Interface ID | Task IDs | Trace note |
|---|---|---|
| IFACE-COV-001 | TSK-COV-01 | Defines where the dedicated blocking job lives and how it joins the workflow graph |
| IFACE-COV-002 | TSK-COV-01, TSK-COV-02 | Pins the exact command surface that produces the blocking coverage signal |
| IFACE-COV-003 | TSK-COV-04 | Prevents YAML/config threshold drift |
| IFACE-COV-004 | TSK-COV-01, TSK-COV-03 | Ensures the gate is fail-closed rather than advisory |
| IFACE-COV-005 | TSK-COV-03 | Encodes the workflow-shape contract in structure tests |
| IFACE-COV-006 | TSK-COV-04 | Preserves the 40-floor authority in config tests |
| IFACE-COV-007 | TSK-COV-05 | Constrains rollback to threshold-only changes while keeping enforcement intact |

## Acceptance Criteria
| AC ID | Acceptance criterion | Executable check |
|---|---|---|
| AC-COV-001 | The design explicitly reconciles the stale idea premise with current repo truth | Review `coverage-minimum-enforcement.design.md` for the `Stale-Idea Reconciliation` section |
| AC-COV-002 | The active workflow contains exactly one dedicated blocking `coverage` job and `quick` remains present | `python -m pytest -q tests/structure/test_ci_yaml.py` |
| AC-COV-003 | The coverage job runs the canonical pytest-cov command and does not hardcode `--cov-fail-under` | `python -m pytest -q tests/structure/test_ci_yaml.py` |
| AC-COV-004 | The threshold authority remains `[tool.coverage.report].fail_under` and stays at or above 40 in this slice | `python -m pytest -q tests/test_coverage_config.py` |
| AC-COV-005 | The coverage path is fail-closed and rejects soft-fail operators | `python -m pytest -q tests/structure/test_ci_yaml.py` |
| AC-COV-006 | The canonical coverage command fails when total coverage is below the configured floor and passes when it meets the floor | `python -m pytest tests -q --cov=src --cov-branch --cov-config=pyproject.toml --cov-report=term-missing --cov-report=xml` |
| AC-COV-007 | Project milestone M2 is marked DONE after the design artifact is finalized | Review `coverage-minimum-enforcement.project.md` milestones table |
| AC-COV-008 | Project docs remain workflow-policy compliant after design updates | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |

## Non-Functional Requirements
- Performance:
	- The new `coverage` job should add one bounded Python test run only. This slice must not turn `quick` into a long-running composite gate.
- Security:
	- No workflow permission broadening. `permissions: contents: read` remains sufficient.
	- No soft-fail patterns are permitted on the blocking coverage path.
- Testability:
	- Structure tests and config tests must be enough to detect gate removal, duplication, softening, or threshold drift.
- Operability:
	- The rollback action changes one config key at most and leaves the gate in place.

## Open Questions
1. Should the downstream implementation cache Python dependencies in the new `coverage` job, or keep the initial slice simpler and accept duplicated install time?
2. Should the structure test identify the canonical command by job name, by coverage flags, or by both to minimize false positives?

## Handoff
- Target agent: @4plan
- Design readiness: actionable
- Required downstream focus:
	1. Convert `TSK-COV-01` through `TSK-COV-05` into concrete implementation and test tasks.
	2. Preserve `AC-COV-*` IDs verbatim for plan/test traceability.
	3. Keep the first implementation slice scoped to one blocking job in the existing workflow.

