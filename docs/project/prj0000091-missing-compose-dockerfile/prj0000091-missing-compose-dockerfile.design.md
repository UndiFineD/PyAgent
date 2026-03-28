# missing-compose-dockerfile - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-28_

## Selected Option
**Option C - normalize deploy Docker layout with minimal blast radius**

Rationale:
- Fixes the immediate clean-checkout failure by removing a reference to a non-existent path.
- Keeps deploy artifacts co-located under `deploy/`.
- Avoids broad compose consolidation in this project.

## Problem Statement and Goals
`deploy/compose.yaml` currently references `src/infrastructure/docker/Dockerfile`, which does not exist. Clean-checkout users cannot build the compose service reliably.

Goals:
- Restore deterministic compose path validity on clean checkout.
- Define a stable Dockerfile path strategy for `deploy/compose.yaml`.
- Add regression guards so missing Dockerfile references fail fast in automated checks.

## Architecture
High-level design:
1. Keep `deploy/compose.yaml` as the canonical compose file in this project scope.
2. Redirect its `build.dockerfile` to a deploy-local target.
3. Use a dedicated service Dockerfile (`deploy/Dockerfile.pyagent`) to decouple from unrelated images.
4. Add deterministic validation that parses compose build references and asserts Dockerfile path existence.

Compose path strategy:
- `build.context` remains `..`.
- `build.dockerfile` is set to `deploy/Dockerfile.pyagent`.
- Path resolution is treated as repository-root relative after compose context expansion.

Component responsibilities:
- `deploy/compose.yaml`: runtime/deploy entrypoint contract for the `pyagent` service.
- `deploy/Dockerfile.pyagent`: canonical build recipe for this compose service.
- Compose Dockerfile path guard test: verifies all compose `build.dockerfile` references exist.

## Interfaces & Contracts
### IFC-01 Compose Build Contract
- File: `deploy/compose.yaml`
- Service: `pyagent`
- Behavior:
	- Must define `build.context` and `build.dockerfile`.
	- `build.dockerfile` must resolve to an existing file from repository root.
	- Must point to `deploy/Dockerfile.pyagent`.

### IFC-02 Dockerfile Contract
- File: `deploy/Dockerfile.pyagent` (new)
- Behavior:
	- Must build the same runtime role currently expected by `pyagent` compose service.
	- Must avoid assumptions on absent repository paths.
	- Must remain deploy-local (no migration into `src/infrastructure/`).

### IFC-03 Regression Guard Contract
- File (planned): `tests/deploy/test_compose_dockerfile_paths.py`
- Behavior:
	- Enumerate compose files in scope (at minimum `deploy/compose.yaml`).
	- Parse `services.*.build.dockerfile`.
	- Resolve each path and assert file existence.
	- Fail with actionable message listing missing path(s).

## Target Files and Planned Changes
Implementation target set for @4plan/@6code:

1. `deploy/compose.yaml`
- Change `services.pyagent.build.dockerfile` from non-existent `src/infrastructure/docker/Dockerfile` to `deploy/Dockerfile.pyagent`.

2. `deploy/Dockerfile.pyagent` (new)
- Add dedicated Dockerfile for the compose `pyagent` service.

3. `tests/deploy/test_compose_dockerfile_paths.py` (new)
- Add deterministic regression guard for missing Dockerfile references.

4. `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.exec.md`
- Record validation command outputs.

5. `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.code.md`
- Record exact implemented path changes and diffs summary.

## Acceptance Criteria
| AC ID | Requirement | Verification |
|---|---|---|
| AC-001 | `deploy/compose.yaml` no longer references missing `src/infrastructure/docker/Dockerfile`. | Inspect compose file diff. |
| AC-002 | Compose `pyagent` service uses deploy-local Dockerfile path strategy. | `build.dockerfile == deploy/Dockerfile.pyagent`. |
| AC-003 | Target Dockerfile file exists in repository at the configured path. | Filesystem assertion in regression guard test. |
| AC-004 | Deterministic regression guard fails when any compose Dockerfile path is missing. | Negative test by temporary path mutation in unit test fixture. |
| AC-005 | Validation logs are captured in project exec artifact and are reproducible. | `*.exec.md` includes command + pass/fail output summary. |
| AC-006 | Scope is limited to compose/Dockerfile path fix and guardrails, without full compose consolidation. | Diff review against non-goals and scope boundary. |

## Interface-to-Task Traceability
| Planned Task ID (@4plan) | Interface/Contract | Target File(s) | Acceptance Criteria |
|---|---|---|---|
| T1 | IFC-01 Compose Build Contract | `deploy/compose.yaml` | AC-001, AC-002 |
| T2 | IFC-02 Dockerfile Contract | `deploy/Dockerfile.pyagent` | AC-003 |
| T3 | IFC-03 Regression Guard Contract | `tests/deploy/test_compose_dockerfile_paths.py` | AC-004 |
| T4 | Validation evidence contract | `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.exec.md` | AC-005 |
| T5 | Scope guard contract | project doc artifacts and PR diff | AC-006 |

## Non-Functional Requirements
- Performance: Validation guard must complete in under 5 seconds in local CI conditions (single compose parse + path checks).
- Security: No new secret material, credentials, or network-dependent runtime steps are introduced by the guard.
- Testability: Path checks are deterministic and do not require Docker daemon availability.

## Deterministic Validation Strategy
Primary deterministic checks:
1. `pytest -q tests/deploy/test_compose_dockerfile_paths.py`
2. Static compose parse path check from repository checkout state (no runtime container launch required).

Optional smoke (non-blocking for deterministic gate):
1. `docker compose -f deploy/compose.yaml config`
2. `docker compose -f deploy/compose.yaml build pyagent`

Determinism notes:
- Gate decisions rely on static path validation, not network pulls or environment-specific daemon state.
- Optional docker commands provide extra confidence but do not replace the static deterministic guard.

## Regression Guards
- Add targeted test `tests/deploy/test_compose_dockerfile_paths.py`.
- Wire test into existing CI test selection where deploy regression checks are run.
- Failure message template must include compose file, service name, and missing resolved path.

## Rollback Strategy
Rollback trigger:
- Compose service fails build/start in environments where it previously worked.

Rollback steps:
1. Revert `deploy/compose.yaml` Dockerfile path change.
2. Revert/remove `deploy/Dockerfile.pyagent` if newly introduced.
3. Revert guard test addition if it blocks emergency rollback branch.
4. Log rollback reasoning and follow-up action in project exec artifact.

Rollback blast radius:
- Limited to deploy compose path and related guard files.

## Non-Goals
- Do not consolidate `deploy/compose.yaml` and `deploy/docker-compose.yaml` in this project.
- Do not redesign image strategy for unrelated services.
- Do not refactor unrelated runtime/application code.
- Do not add CI platform-wide workflow redesign outside targeted regression guard integration.

## Open Questions
1. Should @4plan place the regression guard under `tests/deploy/` or fold it into an existing deploy validation module if one is discovered during planning?
2. Should optional docker smoke checks be documented as local-only or also added as a non-blocking CI job?

## Handoff Readiness
Design is implementation-ready for @4plan with explicit contracts, file targets, AC IDs, traceability, validation, rollback, and non-goals.
