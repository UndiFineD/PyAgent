# ci-security-quality-workflow-consolidation - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-02_

## Selected Option
Option C: Hybrid model with fast pre-commit quality gates on push/PR and heavyweight security scans on a scheduled cadence.

Rationale:
1. Keep current fast feedback path intact (`pre-commit run --all-files` in lightweight CI).
2. Add missing automated security depth (dependency audit + CodeQL).
3. Avoid expensive scans on every PR while preserving on-demand manual execution.

## Problem Statement and Goals
The repository already enforces broad quality/security/governance checks through `.pre-commit-config.yaml` and runs a lightweight CI verifier in `.github/workflows/ci.yml`. The unresolved gap is scheduled, codified heavyweight security scanning and formal test coverage for that workflow contract.

Goals:
1. Add a dedicated scheduled security workflow with least-privilege permissions.
2. Define deterministic contracts for dependency auditing and CodeQL scanning.
3. Add CI tests that enforce workflow structure and prevent contract drift.

## Architecture Overview
This design adds one new workflow and one new test module, plus small contract assertions in an existing CI test module.

### New and Changed Files
1. New: `.github/workflows/security-scheduled.yml`
2. New: `tests/ci/test_security_workflow.py`
3. Change: `tests/ci/test_ci_workflow.py` (pre-commit parity assertion only)

### Unchanged by Design (Non-goal Boundary)
1. `.pre-commit-config.yaml`
2. `.github/workflows/ci.yml` trigger and existing quick-job behavior
3. Source/runtime code under `src/**`, `backend/**`, `rust_core/**`

### High-Level Flow
1. `push`/`pull_request` continue using lightweight CI (`ci.yml`) with `pre-commit run --all-files`.
2. Daily schedule on `main` (plus manual `workflow_dispatch`) runs `security-scheduled.yml`.
3. `dependency-audit` evaluates Python dependencies from `requirements.txt` and `requirements-ci.txt`.
4. `codeql-scan` runs CodeQL for Python and includes custom query pack from `codeql/codeql-custom-queries-python/`.
5. Artifacts and SARIF are published for triage and auditability.

## Component Design

### Component A: Scheduled Security Workflow
Target file: `.github/workflows/security-scheduled.yml`

#### Trigger Contract
1. `on.schedule` daily cron for recurring scans.
2. `on.workflow_dispatch` for on-demand runs.
3. Scope intent: run on `main` schedule context and manual dispatch only.
4. Explicitly not configured as a PR workflow.

#### Permissions Contract
Top-level permissions:
1. `contents: read`
2. `security-events: write`

No broader permissions are required for this design.

#### Job: `dependency-audit`
Purpose: dependency vulnerability detection with severity-aware outcomes.

Inputs:
1. `requirements.txt`
2. `requirements-ci.txt`

Execution pattern:
1. Set up Python runtime.
2. Install `pip-audit` and scan dependencies from both requirement files.
3. Capture machine-readable and human-readable outputs as artifacts.

Failure and triage policy:
1. `CRITICAL`: treated as release-blocking advisory condition.
2. `HIGH`: requires issue creation for tracked remediation.
3. Below `HIGH`: recorded in artifacts; non-blocking by default.

Note: The enforcement above is design policy; exact implementation mechanism (single-step fail gate vs post-processing step) is delegated to @4plan/@6code while preserving this contract.

#### Job: `codeql-scan`
Purpose: static security analysis on Python with repository custom queries.

Inputs:
1. Language matrix: Python only (`python`)
2. Custom query pack path: `codeql/codeql-custom-queries-python/`
3. CodeQL pack metadata source: `codeql/codeql-custom-queries-python/codeql-pack.yml`

Execution pattern:
1. Checkout repository.
2. Initialize CodeQL with Python language matrix and custom queries path.
3. Run analysis and upload SARIF to code scanning.

Scope policy:
1. Run for scheduled `main` scans and manual dispatch only.
2. Do not run on every PR in this phase.

Triage ownership:
1. Rotating maintainer owns initial triage rotation.

### Component B: Security Workflow Tests
Target file: `tests/ci/test_security_workflow.py`

Test contract coverage:
1. Workflow file exists at `.github/workflows/security-scheduled.yml`.
2. Trigger block includes daily `schedule` and `workflow_dispatch`.
3. Top-level permissions include `contents: read` and `security-events: write`.
4. Job names include `dependency-audit` and `codeql-scan`.
5. CodeQL language matrix is Python-only.
6. CodeQL configuration references custom query pack path.

### Component C: Pre-commit Parity Test
Target file: `tests/ci/test_ci_workflow.py`

Additive assertion contract:
1. CI quick job continues to execute `pre-commit run --all-files` as the primary quality gate command.
2. Assertion must inspect the step command text, not only the step name, to prevent silent drift.

## Interfaces & Contracts

### IFACE-SEC-001: Scheduled CI Trigger Contract
Type: workflow trigger interface.

Contract:
1. Security workflow must expose exactly two trigger families for this phase: daily `schedule` and `workflow_dispatch`.
2. PR-trigger execution is out of scope for this phase.

Provider: `.github/workflows/security-scheduled.yml`
Consumer: GitHub Actions scheduler and manual dispatch invoker.

### IFACE-SEC-002: `dependency-audit` Job Contract
Type: dependency security scan interface.

Inputs:
1. `requirements.txt`
2. `requirements-ci.txt`

Outputs:
1. Artifactized audit report(s) suitable for forensic review.
2. Exit status and policy signal for severity handling.

Failure modes:
1. Tool/runtime setup failure -> job fails.
2. Detected `CRITICAL` vulnerability -> blocking advisory failure.
3. Detected `HIGH` vulnerability -> issue-generation obligation (and optional failure per final policy implementation).

### IFACE-SEC-003: `codeql-scan` Job Contract
Type: CodeQL analysis interface.

Inputs:
1. Codebase checkout on workflow target ref.
2. Python language matrix entry.
3. Custom query pack path under `codeql/codeql-custom-queries-python/`.

Outputs:
1. SARIF uploaded through CodeQL action with `security-events: write` permission.

Failure modes:
1. CodeQL initialization/analysis/upload failure -> job fails.
2. Misconfigured custom query path -> contract test failure.

### IFACE-SEC-004: Workflow Compliance Test Contract
Type: repository policy test interface.

Contract:
1. `tests/ci/test_security_workflow.py` enforces scheduled security workflow shape.
2. `tests/ci/test_ci_workflow.py` enforces pre-commit parity in lightweight CI.
3. Any contract drift must fail CI tests deterministically.

## Acceptance Criteria

| AC ID | Criterion | Verification signal |
|---|---|---|
| AC-SEC-001 | New workflow exists at `.github/workflows/security-scheduled.yml` with daily `schedule` and `workflow_dispatch` triggers and no PR trigger. | `tests/ci/test_security_workflow.py` trigger assertions pass. |
| AC-SEC-002 | Workflow declares least-privilege top-level permissions including `contents: read` and `security-events: write`. | Permission assertions in `tests/ci/test_security_workflow.py` pass. |
| AC-SEC-003 | Workflow defines `dependency-audit` and `codeql-scan`; CodeQL matrix is Python-only and references custom query pack. | Job/matrix/query-path assertions in `tests/ci/test_security_workflow.py` pass. |
| AC-SEC-004 | Lightweight CI remains pre-commit-first using `pre-commit run --all-files` as primary quality gate command. | Added parity assertions in `tests/ci/test_ci_workflow.py` pass. |

## Interface-to-Task Traceability

| Interface | Planned implementation task (for @4plan) | Target file(s) | Related AC |
|---|---|---|---|
| IFACE-SEC-001 | Add workflow trigger block (`schedule` + `workflow_dispatch`) and keep PR triggers absent. | `.github/workflows/security-scheduled.yml` | AC-SEC-001 |
| IFACE-SEC-002 | Implement `dependency-audit` job: install tooling, scan both requirements files, publish artifacts, encode severity policy outcomes. | `.github/workflows/security-scheduled.yml` | AC-SEC-002, AC-SEC-003 |
| IFACE-SEC-003 | Implement `codeql-scan` job with Python matrix, custom query path, and SARIF upload permissions. | `.github/workflows/security-scheduled.yml` | AC-SEC-002, AC-SEC-003 |
| IFACE-SEC-004 | Add workflow compliance tests and pre-commit parity test assertion. | `tests/ci/test_security_workflow.py`, `tests/ci/test_ci_workflow.py` | AC-SEC-001, AC-SEC-002, AC-SEC-003, AC-SEC-004 |

## Non-Functional Requirements
1. Performance: keep PR CI path lightweight; heavyweight security scans run on daily/manual cadence only.
2. Security: enforce least-privilege workflow permissions and codify scan outputs for auditable triage.
3. Testability: workflow contracts are enforced through deterministic YAML-structure tests in `tests/ci/`.
4. Operability: define triage ownership (rotating maintainer) and severity response policy to prevent alert drift.

## Open Questions Resolution (from @2think)
1. Scan cadence: daily scheduled scan plus manual `workflow_dispatch`; not on every PR.
2. Severity response: `CRITICAL` = block release advisory; `HIGH` = create tracking issue.
3. CodeQL scope: run on scheduled `main` and manual dispatch only; no PR trigger in this phase.
4. Triage owner: rotating maintainer.

## Non-Goals
1. No changes to `.pre-commit-config.yaml`.
2. No changes to `.github/workflows/ci.yml` triggers or existing quick test jobs.
3. No migration of heavyweight scans into per-PR lightweight CI.

## Rollback Plan
If scheduled security workflow causes CI resource contention:
1. Delete `.github/workflows/security-scheduled.yml`.
2. Delete `tests/ci/test_security_workflow.py`.
3. Revert only the additive parity assertion in `tests/ci/test_ci_workflow.py` if added in the same implementation wave.

No other files are part of rollback scope for this design.

## ADR Impact
No new cross-cutting architecture ADR is required for this change. This design refines CI workflow topology within existing governance direction.
