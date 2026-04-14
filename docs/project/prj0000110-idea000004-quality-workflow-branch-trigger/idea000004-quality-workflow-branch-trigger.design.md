# idea000004-quality-workflow-branch-trigger - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-01_

## Selected Option
Option B from `@2think`: keep full-quality workflows narrow to `main` and add a targeted branch-governance quality gate for project-branch pull requests.

Rationale summary:
1. Preserves the current low-redundancy workflow topology from prior-art (`prj0000075`).
2. Delivers earlier, branch-local governance signal without running full suites on every project push.
3. Reuses existing branch and docs governance controls (`scripts/enforce_branch.py`, `tests/docs/test_agent_workflow_policy_docs.py`).

## Problem Statement and Goals
The idea requires quality workflow behavior to trigger for project branches, but current active workflows are mostly `main`-centric. The design must provide deterministic, branch-aware quality signal while avoiding legacy workflow sprawl.

Goals:
1. Add an explicit governance quality signal for project branch pull requests.
2. Keep required checks deterministic and avoid stuck/pending skip states.
3. Preserve existing full-suite quality model on `main`.
4. Provide explicit interface/test contracts for `@4plan` and `@5test`.

Non-goals:
1. Reintroducing deprecated legacy `quality.yml` workflow topology.
2. Running all full build/test/security suites for every project branch push.
3. Broad CI architecture redesign outside this project lane.

## Constraints
1. Branch must remain `prj0000110-idea000004-quality-workflow-branch-trigger` for this lane.
2. Scope remains project docs plus required `@3design` memory/log artifacts.
3. Naming and terminology must follow project naming standards.
4. Conduct and governance language must remain compliant with project code of conduct.
5. Downstream artifacts must be testable with deterministic command evidence.

## Architecture Overview
### Logical flow
1. Contributor opens/updates a PR from a project branch.
2. A lightweight governance gate workflow/job runs for that PR event context.
3. Gate invokes branch/scope/docs policy validations and emits explicit pass/fail signal.
4. Reviewer receives a deterministic required check representing governance conformance.
5. Full quality suites remain triggered by existing `main`-focused CI/security workflows.

### Components
1. `Workflow Trigger Layer`: PR event filter for project branches with least-privilege permissions.
2. `Governance Gate Job`: orchestrates branch and docs policy checks.
3. `Validation Engine`: reuses `scripts/enforce_branch.py` and docs policy pytest selector.
4. `Check Reporting Contract`: stable check/job naming and explicit gate scope messaging.
5. `Downstream Planning Contract`: task IDs and test contracts for `@4plan`/`@5test`.

## Interfaces and Contracts
| Interface ID | Interface/Contract | Inputs | Outputs | Invariants | Failure Contract |
|---|---|---|---|---|---|
| IFACE-QWB-001 | Project branch trigger contract | PR metadata: source branch, target branch, event type | Gate run starts or is intentionally skipped with explicit reason | Trigger pattern must match project branch naming policy; no ambiguous wildcard behavior | If branch metadata missing or non-conformant, gate fails closed |
| IFACE-QWB-002 | Governance execution contract | Repo checkout, branch plan metadata, project artifact paths | Deterministic pass/fail exit code and step summary | Must invoke canonical branch governance entrypoint (`scripts/enforce_branch.py`) | Any command failure produces explicit failing status |
| IFACE-QWB-003 | Docs policy validation contract | Project docs artifact paths | Pytest selector result for docs policy | Must run `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | Non-zero exit blocks gate |
| IFACE-QWB-004 | Required-check identity contract | Workflow/job metadata | Stable check name visible to reviewers | Check name remains stable across revisions to prevent branch protection drift | Name mismatch versus documented contract is treated as failure |
| IFACE-QWB-005 | Scope boundary contract | Changed files list in PR | In-scope/out-of-scope decision with evidence | Must enforce one-project-one-branch and declared scope boundary | Out-of-scope modifications fail gate with actionable message |
| IFACE-QWB-006 | Security permissions contract | Workflow permissions/event definitions | Least-privilege permission map | Use non-escalating PR context and deny-by-default permissions | Elevated permission diff from baseline blocks approval |
| IFACE-QWB-007 | Downstream handoff contract | Design AC IDs + interface table | Implementable plan task map and test hooks | Every acceptance criterion and interface maps to planned task IDs | Missing traceability blocks handoff to `@4plan` |

## Acceptance Criteria
| AC ID | Acceptance Criterion | Verification Evidence | Interfaces |
|---|---|---|---|
| AC-QWB-001 | A governance quality gate is triggered for project-branch PR events according to documented branch policy. | Workflow trigger contract test and event simulation evidence | IFACE-QWB-001, IFACE-QWB-004 |
| AC-QWB-002 | Gate execution reuses canonical branch governance enforcement and fails closed on policy violations. | Failing and passing command evidence for `scripts/enforce_branch.py` | IFACE-QWB-002, IFACE-QWB-005 |
| AC-QWB-003 | Docs policy validation is executed in the gate and blocks merge on non-compliance. | Command result for `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | IFACE-QWB-003 |
| AC-QWB-004 | Required-check identity is stable and unambiguous for branch protection policies. | Workflow/job name contract assertions in test artifacts | IFACE-QWB-004 |
| AC-QWB-005 | Workflow event and permission configuration remain least-privilege and non-escalating. | Static workflow policy assertions and review evidence | IFACE-QWB-006 |
| AC-QWB-006 | Design provides complete interface-to-task and AC-to-task traceability for downstream planning/testing. | Traceability tables present and complete | IFACE-QWB-007 |

## Interface-to-Task Traceability for @4plan
Planned implementation task IDs reserved for `@4plan` decomposition:

| Planned Task ID | Planned Deliverable | Interfaces | AC IDs |
|---|---|---|---|
| PLAN-QWB-001 | Add/adjust workflow trigger pattern for project-branch PR events | IFACE-QWB-001, IFACE-QWB-004 | AC-QWB-001, AC-QWB-004 |
| PLAN-QWB-002 | Add governance gate job orchestration using canonical branch enforcement | IFACE-QWB-002, IFACE-QWB-005 | AC-QWB-002 |
| PLAN-QWB-003 | Wire docs policy selector execution into gate | IFACE-QWB-003 | AC-QWB-003 |
| PLAN-QWB-004 | Enforce least-privilege permissions and event safety assertions | IFACE-QWB-006 | AC-QWB-005 |
| PLAN-QWB-005 | Add workflow-level tests/assertions for trigger and required-check identity contracts | IFACE-QWB-001, IFACE-QWB-004 | AC-QWB-001, AC-QWB-004 |
| PLAN-QWB-006 | Add governance docs updates and explicit gate scope language | IFACE-QWB-007 | AC-QWB-006 |

Traceability gate:
1. `@4plan` must preserve these task IDs or map them one-to-one to concrete successor IDs.
2. Any unmapped interface or AC blocks planning handoff.

## Testability Contract for @5test
| Test Contract ID | What must be tested | Minimum deterministic command/evidence |
|---|---|---|
| TEST-QWB-001 | Trigger contract executes on valid project-branch PR event and does not execute on non-matching events | Workflow structure/event assertion tests plus event fixture evidence |
| TEST-QWB-002 | Branch governance failure path blocks gate | Run branch enforcement with known violating fixture and assert non-zero exit |
| TEST-QWB-003 | Docs policy failure path blocks gate | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` with failing fixture expectation |
| TEST-QWB-004 | Required-check name stability | Assert exact expected check/job identifier in workflow contract tests |
| TEST-QWB-005 | Permission hardening | Static assertion for permissions map and disallowed privileged events |
| TEST-QWB-006 | Scope boundary rejection | Execute branch/scope enforcement against out-of-scope change fixture and assert failure |

Minimum green signal for lane completion:
1. Governance trigger contract tests pass.
2. Branch/scope enforcement pass/fail scenarios are both covered.
3. Docs policy selector passes in CI gate context.

## Non-Functional Requirements
1. Performance: governance gate should remain lightweight and complete significantly faster than full CI suite.
2. Security: use least-privilege workflow permissions; avoid privileged event contexts.
3. Reliability: fail-closed behavior for missing/invalid branch or scope metadata.
4. Maintainability: prefer canonical governance scripts/tests over duplicating logic in YAML.
5. Observability: gate output must explicitly describe whether failure is branch, scope, docs policy, or permissions related.

## ADR Impact
No new ADR is required for this lane at design stage because the selected option applies repository-established governance and CI architecture patterns rather than introducing a new architectural style. If `@4plan` expands this into net-new workflow topology (for example multi-workflow orchestration), create an ADR before implementation.

## Open Questions for @4plan
1. Should the governance gate be PR-only blocking, or also run informationally on project-branch push?
2. Should `security.yml` include a mirrored governance precheck or remain unchanged with explicit rationale?
3. Is `merge_group` trigger support deferred to a dedicated follow-up lane?

## Handoff Readiness
1. Selected option is explicit and justified from `@2think`.
2. Interfaces/contracts are concrete with invariants and failure contracts.
3. Acceptance criteria have unique AC IDs and verification evidence.
4. Interface-to-task traceability is complete and blocking if incomplete.
5. Testability expectations are explicit for `@5test`.