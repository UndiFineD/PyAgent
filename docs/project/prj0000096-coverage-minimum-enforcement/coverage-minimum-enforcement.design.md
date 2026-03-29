# coverage-minimum-enforcement - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-28_

## Policy Alignment
- Code of conduct check: PASS (`docs/project/code_of_conduct.md` reviewed; no conflicting behavior in scope).
- Naming standards check: PASS (`docs/project/naming_standards.md` reviewed; only existing snake_case file paths and current CI naming are used).

## Selected Option
Selected option: Option B - staged ratchet to target baseline.

Rationale:
1. It restores actual CI enforcement now while avoiding a high-risk big-bang jump to 70.
2. It keeps one threshold source of truth in `pyproject.toml` and prevents command drift.
3. It fits current CI governance constraints by extending the existing `CI (minimal)` workflow instead of adding a new workflow file.

## Problem and Goals
Problem:
- Coverage minimum is configured (`fail_under`) but not enforced in the blocking CI workflow path.

Goals:
1. Add deterministic CI enforcement of global minimum coverage.
2. Keep threshold management centralized and ratcheted by explicit policy.
3. Preserve workflow-count and CI-structure constraints already enforced by tests.

## Architecture
### High-Level Flow
1. CI continues to run test shards in `.github/workflows/ci.yml` job `test`.
2. A new blocking step in the same workflow runs a canonical coverage command after dependency setup and Rust build.
3. The command reads the threshold from `pyproject.toml` via coverage config resolution (`coverage report --fail-under` behavior governed by `[tool.coverage.report] fail_under`).
4. If measured coverage is below threshold, CI fails the job.
5. Structure tests and config tests enforce that the gate remains present, blocking, and tied to the source-of-truth threshold.

### Source-of-Truth Threshold Contract
- Authoritative threshold location: `pyproject.toml` `[tool.coverage.report] fail_under`.
- CI command contract: do not hardcode a duplicate threshold value in workflow commands.
- Ratchet updates happen by editing `fail_under` only, plus updating rollout record in project artifacts.

### Ratchet Schedule
Initial staged ratchet path for idea-008:
1. Stage 1: `fail_under = 40` (first enforcement slice)
2. Stage 2: `fail_under = 55`
3. Stage 3: `fail_under = 70`

Each promotion requires meeting promotion criteria in the rollout controls section.

## First Implementation Slice
### Exact Files Expected to Change
1. `.github/workflows/ci.yml`
2. `pyproject.toml`
3. `tests/structure/test_ci_yaml.py`
4. `tests/test_coverage_config.py`
5. `docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md`

### Slice Boundaries
In scope for slice 1:
1. Introduce one blocking coverage gate in existing CI workflow.
2. Raise threshold from 30 to 40 as first ratchet step.
3. Add/extend tests that assert gate presence, blocking semantics, and source-of-truth consistency.
4. Record baseline and gate outcome method in project test artifact.

Out of scope for slice 1:
1. Per-package coverage floors.
2. Additional workflow files.
3. Broad test-suite refactors unrelated to enabling first ratchet gate.

## Interfaces and Contracts
### IFC-01: CI Coverage Gate Contract
Interface:
- Workflow file: `.github/workflows/ci.yml`
- Job: `jobs.test`
- Step requirement: at least one pytest-cov execution and one blocking coverage evaluation path.

Rules:
1. Must be in existing `CI (minimal)` workflow.
2. Must not use `continue-on-error`, `|| true`, `||true`, or `set +e` in coverage-gate step.
3. Must execute on pull_request and push to main under same workflow.

### IFC-02: Threshold Source-of-Truth Contract
Interface:
- Config file: `pyproject.toml`
- Section: `[tool.coverage.report]`
- Key: `fail_under`

Rules:
1. Threshold is defined once in config.
2. CI gate must honor this value and avoid duplicate hardcoded threshold constants in workflow script.
3. Ratchet promotions are done by changing this single key.

### IFC-03: Structure Guard Contract
Interface:
- Tests: `tests/structure/test_ci_yaml.py`, `tests/test_coverage_config.py`

Rules:
1. Tests must fail if CI coverage gate is removed.
2. Tests must fail if CI gate is softened to non-blocking behavior.
3. Tests must fail if threshold-source linkage drifts from `pyproject.toml`.

### IFC-04: Workflow-Count Compatibility Contract
Interface:
- Existing workflow-count checks (`tests/ci/test_workflow_count.py`) remain authoritative.

Rules:
1. No new workflow files are introduced.
2. Coverage enforcement is integrated into existing `.github/workflows/ci.yml`.

## CI Enforcement Flow and Workflow-Count Compatibility
Enforcement flow:
1. Checkout and Python setup.
2. Dependency installation and Rust extension build.
3. Existing test shard execution remains intact.
4. Coverage gate step runs in same workflow and fails below current ratchet threshold.
5. Structure tests verify gate integrity and blocking semantics.

Compatibility with workflow-count constraints:
1. Design does not add new workflow YAML files.
2. Design modifies only existing `ci.yml` internals.
3. Existing workflow-count tests continue to pass because workflow inventory remains unchanged.

## Rollout and Risk Controls
### Promotion Criteria (to raise threshold)
Promote from one stage to the next only when all conditions are true:
1. Minimum 10 consecutive green CI runs on default branch with current threshold.
2. No open flake category where coverage gate is the primary failure reason for more than 3 consecutive runs.
3. Measured coverage exceeds next target by at least 1 percentage point in two independent runs.
4. Project test artifact updated with promotion evidence and date.

### Pause Criteria
Pause ratchet progression when either condition occurs:
1. Coverage gate causes more than 20% of CI failures over any rolling 7-day window.
2. Median CI duration regresses by more than 15% compared to pre-gate baseline.

### Rollback Criteria
Rollback to previous threshold when either condition occurs:
1. Two consecutive business days with unresolved red default-branch CI due to threshold only.
2. Confirmed false-positive or tooling regression in coverage computation that invalidates gate signal.

Rollback method:
1. Revert only `fail_under` to prior stage in `pyproject.toml`.
2. Keep CI gate active.
3. Record rollback reason and corrective action in test artifact.

## Acceptance Criteria
| AC ID | Requirement | Verifiable Check | Evidence Location |
|---|---|---|---|
| AC-001 | CI has one blocking coverage-gate path in existing workflow | Inspect `.github/workflows/ci.yml` and assert coverage step exists and fails on low coverage | `tests/structure/test_ci_yaml.py` |
| AC-002 | Threshold source-of-truth is singular and explicit | Assert `[tool.coverage.report] fail_under` exists and is the only policy threshold knob | `pyproject.toml`, `tests/test_coverage_config.py` |
| AC-003 | First ratchet stage is enforced | CI fails when measured coverage is below stage-1 threshold (40) | CI run log + `coverage-minimum-enforcement.test.md` |
| AC-004 | Gate cannot be silently softened | Tests fail if `continue-on-error`, `|| true`, `||true`, or `set +e` appears in gate path | `tests/structure/test_ci_yaml.py` |
| AC-005 | Workflow-count constraints remain compliant | Workflow-count tests remain green with no added workflow file | `tests/ci/test_workflow_count.py` CI output |
| AC-006 | Promotion and rollback controls are explicit and operable | Promotion, pause, rollback criteria documented and referenced by implementation/test artifacts | `coverage-minimum-enforcement.design.md`, `coverage-minimum-enforcement.test.md` |

## Interface-to-Task Traceability
| Interface/Contract | Implementation Task ID (for @4plan) | Task Intent | Acceptance Criteria |
|---|---|---|---|
| IFC-01 CI Coverage Gate Contract | T1 | Add blocking coverage gate step to `.github/workflows/ci.yml` without soft-fail operators | AC-001, AC-004 |
| IFC-02 Threshold Source-of-Truth Contract | T2 | Set and manage stage threshold in `pyproject.toml` only (`fail_under = 40` for slice 1) | AC-002, AC-003 |
| IFC-03 Structure Guard Contract | T3 | Extend `tests/structure/test_ci_yaml.py` and `tests/test_coverage_config.py` for gate/linkage assertions | AC-001, AC-002, AC-004 |
| IFC-04 Workflow-Count Compatibility Contract | T4 | Verify no workflow-file expansion and preserve workflow-count invariants | AC-005 |
| Ratchet Governance Record | T5 | Update project test artifact with baseline command, stage value, promotion/rollback evidence format | AC-003, AC-006 |

## Non-Functional Requirements
- Performance: coverage enforcement must not increase median CI duration by more than 15% from pre-gate baseline at stage 1.
- Security: no secret material in coverage artifacts; no workflow permission broadening beyond read-only contents.
- Testability: all enforcement conditions are validated by deterministic structure/config tests and reproducible CI commands.
- Operability: rollback changes only one threshold key and does not disable coverage gate.

## Open Questions for @4plan
1. Whether to run the coverage gate as a dedicated post-shard command in the same job or as a single dedicated non-sharded command path in that workflow job while preserving runtime budget.
2. Whether baseline evidence for stage promotion should be sourced from default-branch nightly snapshots or from merged PR runs only.
