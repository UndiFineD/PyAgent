# idea000016-mixin-architecture-base - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-30_

## Branch Plan
Expected branch: prj0000105-idea000016-mixin-architecture-base.

## Branch Validation
- PASS: Expected branch declared in project artifact.
- PASS: Observed branch matches expected (`git branch --show-current` -> `prj0000105-idea000016-mixin-architecture-base`).

## Scope Validation
- PASS: Plan defines only implementation/test files required by approved design scope.
- PASS: Naming standards applied for new Python modules and tests (snake_case modules, PascalCase classes).
- PASS: Code of conduct reviewed; no harmful or exclusionary content in plan outputs.

## Failure Disposition
None at planning stage.

## Overview
This plan translates the selected design (incremental migration with compatibility shims) into executable, gated tasks for @5test -> @6code -> @7exec -> @8ql -> @9git.

Delivery is sequenced in two implementation chunks:
1. Chunk A (T001-T006): canonical namespace, host contract, and compatibility shims.
2. Chunk B (T007-T013): parity/import/expiry/observability gates plus docs policy closure.

Every task includes objective, target files, acceptance criteria mapping, and at least one validation command.

## Task List
- [ ] T001 - Objective: Create canonical base mixin package exports | Files: `src/core/base/mixins/__init__.py` | Acceptance: AC-MX-001 | Validation: `python -m pytest -q tests/core/base/mixins/test_export_contract.py -k canonical_exports`
- [ ] T002 - Objective: Add deterministic export ordering and symbol contract guard | Files: `src/core/base/mixins/__init__.py`, `tests/core/base/mixins/test_export_contract.py` | Acceptance: AC-MX-001 | Validation: `python -m pytest -q tests/core/base/mixins/test_export_contract.py`
- [ ] T003 - Objective: Define host protocol and base validation contract | Files: `src/core/base/mixins/host_contract.py`, `src/core/base/mixins/base_behavior_mixin.py`, `tests/core/base/mixins/test_host_contract.py` | Acceptance: AC-MX-002 | Validation: `python -m pytest -q tests/core/base/mixins/test_host_contract.py`
- [ ] T004 - Objective: Integrate host contract checks in first-wave canonical mixins | Files: `src/core/base/mixins/audit_mixin.py`, `src/core/base/mixins/sandbox_mixin.py`, `tests/core/base/mixins/test_host_validation_in_mixins.py` | Acceptance: AC-MX-002 | Validation: `python -m pytest -q tests/core/base/mixins/test_host_validation_in_mixins.py`
- [ ] T005 - Objective: Implement compatibility shim for audit and sandbox legacy imports | Files: `src/core/audit/AuditTrailMixin.py`, `src/core/sandbox/SandboxMixin.py`, `tests/core/base/mixins/test_legacy_shim_imports.py` | Acceptance: AC-MX-003 | Validation: `python -m pytest -q tests/core/base/mixins/test_legacy_shim_imports.py -k audit_or_sandbox`
- [ ] T006 - Objective: Implement compatibility shim for replay legacy imports with deprecation metadata | Files: `src/core/replay/ReplayMixin.py`, `tests/core/base/mixins/test_legacy_shim_imports.py`, `tests/core/base/mixins/test_shim_deprecation_policy.py` | Acceptance: AC-MX-003 | Validation: `python -m pytest -q tests/core/base/mixins/test_shim_deprecation_policy.py`
- [ ] T007 - Objective: Build old-vs-new behavioral parity harness for migrated mixins | Files: `tests/core/base/mixins/test_mixin_behavior_parity.py`, `tests/core/base/mixins/parity_cases.py` | Acceptance: AC-MX-004 | Validation: `python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py`
- [ ] T008 - Objective: Add differential parity fixtures for failure-path equivalence | Files: `tests/core/base/mixins/conftest.py`, `tests/core/base/mixins/test_mixin_behavior_parity.py` | Acceptance: AC-MX-004 | Validation: `python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py -k failure`
- [ ] T009 - Objective: Add clean-interpreter import smoke and circular dependency checks | Files: `tests/core/base/mixins/test_import_smoke.py` | Acceptance: AC-MX-005 | Validation: `python -m pytest -q tests/core/base/mixins/test_import_smoke.py`
- [ ] T010 - Objective: Enforce shim expiry fail-closed gate | Files: `tests/core/base/mixins/test_shim_expiry_gate.py`, `src/core/base/mixins/shim_registry.py` | Acceptance: AC-MX-006 | Validation: `python -m pytest -q tests/core/base/mixins/test_shim_expiry_gate.py`
- [ ] T011 - Objective: Add migration observability event emission contract | Files: `src/core/base/mixins/migration_observability.py`, `tests/core/base/mixins/test_migration_events.py` | Acceptance: AC-MX-007 | Validation: `python -m pytest -q tests/core/base/mixins/test_migration_events.py`
- [ ] T012 - Objective: Maintain AC/interface traceability artifact consistency | Files: `docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.design.md`, `docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.plan.md` | Acceptance: AC-MX-008 | Validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
- [ ] T013 - Objective: Execute docs workflow policy gate for updated project artifacts | Files: `docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.plan.md` | Acceptance: AC-MX-009 | Validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

## Chunking Plan
| Chunk | Tasks | Estimated Code Files | Estimated Test Files | Deliverable |
|---|---|---|---|---|
| Chunk A | T001-T006 | 9 | 5 | Canonical namespace + host contract + compatibility shims |
| Chunk B | T007-T013 | 3 | 7 | Parity/smoke/expiry/observability gates + policy closure |

## AC-To-Task Mapping
| AC ID | Tasks | Target Files | Validation Commands |
|---|---|---|---|
| AC-MX-001 | T001, T002 | `src/core/base/mixins/__init__.py`; `tests/core/base/mixins/test_export_contract.py` | `python -m pytest -q tests/core/base/mixins/test_export_contract.py` |
| AC-MX-002 | T003, T004 | `src/core/base/mixins/host_contract.py`; `src/core/base/mixins/base_behavior_mixin.py`; `src/core/base/mixins/audit_mixin.py`; `src/core/base/mixins/sandbox_mixin.py`; host-contract tests | `python -m pytest -q tests/core/base/mixins/test_host_contract.py`; `python -m pytest -q tests/core/base/mixins/test_host_validation_in_mixins.py` |
| AC-MX-003 | T005, T006 | `src/core/audit/AuditTrailMixin.py`; `src/core/sandbox/SandboxMixin.py`; `src/core/replay/ReplayMixin.py`; shim tests | `python -m pytest -q tests/core/base/mixins/test_legacy_shim_imports.py`; `python -m pytest -q tests/core/base/mixins/test_shim_deprecation_policy.py` |
| AC-MX-004 | T007, T008 | `tests/core/base/mixins/test_mixin_behavior_parity.py`; parity fixtures | `python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py` |
| AC-MX-005 | T009 | `tests/core/base/mixins/test_import_smoke.py` | `python -m pytest -q tests/core/base/mixins/test_import_smoke.py` |
| AC-MX-006 | T010 | `src/core/base/mixins/shim_registry.py`; `tests/core/base/mixins/test_shim_expiry_gate.py` | `python -m pytest -q tests/core/base/mixins/test_shim_expiry_gate.py` |
| AC-MX-007 | T011 | `src/core/base/mixins/migration_observability.py`; `tests/core/base/mixins/test_migration_events.py` | `python -m pytest -q tests/core/base/mixins/test_migration_events.py` |
| AC-MX-008 | T012 | Design + plan artifact pair | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| AC-MX-009 | T013 | Plan artifact | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |

## Downstream Execution Sequence
| Phase | Agent | Entry Gate | Work Package | Exit Gate | Fail Outcome | Rollback Contingency |
|---|---|---|---|---|---|---|
| P1 | @5test | Plan artifact status DONE with branch PASS | Author/adjust tests for T001-T013 in red state first | Red tests fail for intended reasons and selectors are deterministic | BLOCKED if tests are flaky/ambiguous | Reduce selector scope to file-level tests; rerun isolated failing selectors |
| P2 | @6code | Deterministic red tests from @5test | Implement minimal code to satisfy T001-T013 | Green on all task selectors with no placeholder logic | BLOCKED on behavior drift or partial implementation | Revert latest task-scope commit or file group; re-apply previous stable implementation path |
| P3 | @7exec | Green task selectors and branch/scope still PASS | Execute integration/runtime checks for import and host paths | Runtime/import commands return PASS with normal completion | BLOCKED on import errors/circularity | Roll back last migrated mixin/shim pair and rerun smoke suite |
| P4 | @8ql | Runtime gates PASS | Quality/security verification and policy conformance checks | Quality gates PASS with evidence and no unresolved blocker | BLOCKED on unresolved risk finding | Apply minimal remediation patch, re-run exact failing gate first |
| P5 | @9git | All prior gates PASS and narrow scope validated | Stage, commit, push, PR with governance evidence | Clean commit and PR metadata match project/branch policy | BLOCKED on branch/scope mismatch | Return to @0master for reassignment; no staging on mismatched branch |

## Pass/Fail Gates
| Gate ID | Stage | Pass Condition | Fail Condition | Owner |
|---|---|---|---|---|
| G1 | Branch | `git branch --show-current` == expected branch | Any mismatch | @4plan, @9git |
| G2 | Test Design | Red tests exist and are deterministic | Flaky/non-deterministic selectors | @5test |
| G3 | Implementation | Task selectors pass without placeholder code | Any task selector failing | @6code |
| G4 | Runtime | Import + execution checks finish PASS | Circular import or runtime contract error | @7exec |
| G5 | Quality | Security/quality blockers closed with evidence | Any unresolved high-severity blocker | @8ql |
| G6 | Docs Policy | `tests/docs/test_agent_workflow_policy_docs.py` passes | Any policy test failure | @4plan, @8ql |
| G7 | Git Handoff | Narrow staging, branch/scope compliance, PR metadata valid | Broad staging, wrong branch, invalid metadata | @9git |

## Rollback Matrix
| Trigger | Detection Command | Immediate Action | Rollback Step | Re-entry Gate |
|---|---|---|---|---|
| Parity regression | `python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py` | Freeze wave progression | Restore prior canonical/shim mapping for affected mixin | Parity selector passes |
| Circular import | `python -m pytest -q tests/core/base/mixins/test_import_smoke.py` | Stop merge path | Revert most recent shim chain modification | Import smoke passes |
| Host contract violation | `python -m pytest -q tests/core/base/mixins/test_host_contract.py` | Disable host adoption path | Revert host-integration changes for failing mixin | Host contract tests pass |
| Expired shim still used | `python -m pytest -q tests/core/base/mixins/test_shim_expiry_gate.py` | Block promotion | Extend expiry only with explicit approval or remove remaining legacy imports | Expiry gate passes |
| Docs policy drift | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | Block handoff | Fix artifact schema/order fields and rerun policy test | Docs policy gate passes |

## Command Matrix
| Command ID | Command | Purpose | Owner Phase |
|---|---|---|---|
| CMD-01 | `git branch --show-current` | Branch gate verification | @4plan, @9git |
| CMD-02 | `python -m pytest -q tests/core/base/mixins/test_export_contract.py` | Canonical export contract | @5test, @6code |
| CMD-03 | `python -m pytest -q tests/core/base/mixins/test_host_contract.py` | Host protocol contract | @5test, @6code |
| CMD-04 | `python -m pytest -q tests/core/base/mixins/test_legacy_shim_imports.py` | Legacy import compatibility | @5test, @6code |
| CMD-05 | `python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py` | Behavioral parity | @5test, @6code, @7exec |
| CMD-06 | `python -m pytest -q tests/core/base/mixins/test_import_smoke.py` | Circular/import smoke | @7exec |
| CMD-07 | `python -m pytest -q tests/core/base/mixins/test_shim_expiry_gate.py` | Expiry fail-closed enforcement | @7exec, @8ql |
| CMD-08 | `python -m pytest -q tests/core/base/mixins/test_migration_events.py` | Observability event contract | @6code, @7exec |
| CMD-09 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | Docs policy gate | @4plan, @8ql |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Chunk A test-first package | T001-T006 | NOT_STARTED |
| M2 | Chunk B quality gates | T007-T011 | NOT_STARTED |
| M3 | Artifact closure + policy | T012-T013 | DONE |
| M4 | Handoff to @5test | Sequence P1 ready | READY |

## Policy Gate Results
| Gate | Command | Result |
|---|---|---|
| Docs workflow policy | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` | PASS (`12 passed in 2.82s`) |

## Validation Commands
```powershell
git branch --show-current
python -m pytest -q tests/core/base/mixins/test_export_contract.py
python -m pytest -q tests/core/base/mixins/test_host_contract.py
python -m pytest -q tests/core/base/mixins/test_legacy_shim_imports.py
python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py
python -m pytest -q tests/core/base/mixins/test_import_smoke.py
python -m pytest -q tests/core/base/mixins/test_shim_expiry_gate.py
python -m pytest -q tests/core/base/mixins/test_migration_events.py
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

## Handoff Readiness For @5test
READY. Start with Chunk A (T001-T006) in strict red-first mode, then proceed through the downstream sequence gates.