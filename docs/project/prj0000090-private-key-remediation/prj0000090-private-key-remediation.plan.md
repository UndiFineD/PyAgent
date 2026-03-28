# prj0000090-private-key-remediation - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-28_

## Overview
Implement the secret-remediation control plane from the approved design and ADR using a strict TDD flow:
@5test defines failing tests first, @6code implements until all checks pass, and lane progression is blocked by
rotation and rewrite safety gates.

## Branch Gate
- Expected branch (from project artifact): prj0000090-private-key-remediation
- Observed branch: prj0000090-private-key-remediation
- Result: PASS

## Policy Compliance
- Code of conduct check: PASS (documentation and process planning only)
- Naming standards check: PASS (planned paths use snake_case and existing project naming)

## Task Chunking For TDD
- Chunk 001 (Guardrails + Rotation Gate): 8 code files, 8 test files
- Chunk 002 (Rewrite + Governance Completion): 8 code files, 7 test files
- Each task below includes objective, target files, AC mapping, acceptance checklist, and validation command.

## Acceptance Criteria Checklist (Design Traceability)
- [ ] AC-001 - Active tree has no exposed key artifact; tree scan PASS
- [ ] AC-002 - Impacted credentials rotated with checkpoint evidence; gate COMPLETE
- [ ] AC-003 - CI blocks merges when secret scan finds HIGH/CRITICAL issues
- [ ] AC-004 - Rewrite process purges signatures across refs/tags; post-verify zero matches
- [ ] AC-005 - Contributor migration runbook published and linked in project artifacts
- [ ] AC-006 - Guardrails remain durable (pre-commit + CI + regression checks)

## Task Roadmap

### Chunk 001 - Guardrails + Rotation Gate (handoff first to @5test)

1. T1 - Define scanner contract tests and deterministic report schema
- Objective: Create failing tests for SecretScanService profiles (tree, refs, history) and deterministic ScanReport output.
- Target files: tests/security/test_secret_scan_service_contract.py, tests/security/test_scan_report_schema.py, tests/security/fixtures/scan_samples.py, src/security/secret_scan_service.py, src/security/models/scan_report.py
- AC IDs: AC-001, AC-004, AC-006
- Acceptance checklist:
	- [ ] Failing tests assert profile-specific scan invocation and deterministic finding keys
	- [ ] ScanReport schema requires status enum PASS/FAIL/ERROR and run_id
	- [ ] Tool execution failure path is fail-closed in tests
- Validation command: python -m pytest -q tests/security/test_secret_scan_service_contract.py tests/security/test_scan_report_schema.py
- Dependency/order: First task in chunk

2. T2 - Implement scanner service and scan-report models
- Objective: Implement production code to satisfy T1 tests and design contract behavior.
- Target files: src/security/secret_scan_service.py, src/security/models/scan_report.py, src/security/models/secret_finding.py, src/security/profiles.py
- AC IDs: AC-001, AC-004, AC-006
- Acceptance checklist:
	- [ ] scan_tree, scan_refs, scan_history return deterministic ScanReport payloads
	- [ ] scanner execution errors produce ERROR status and blocking decision surface
	- [ ] baseline suppression metadata includes expiration support
- Validation command: python -m pytest -q tests/security/test_secret_scan_service_contract.py tests/security/test_scan_report_schema.py
- Dependency/order: After T1

3. T3 - Define rotation-checkpoint gate tests
- Objective: Author failing tests for incident lifecycle, evidence completeness, and gate evaluation transitions.
- Target files: tests/security/test_rotation_checkpoint_service.py, tests/security/test_rotation_gate_decision.py, src/security/rotation_checkpoint_service.py, src/security/models/rotation_gate_decision.py
- AC IDs: AC-002, AC-004
- Acceptance checklist:
	- [ ] begin_incident records incident and fingerprint
	- [ ] record_rotation_step requires evidence_uri
	- [ ] evaluate_gate transitions BLOCKED -> PARTIAL -> COMPLETE deterministically
- Validation command: python -m pytest -q tests/security/test_rotation_checkpoint_service.py tests/security/test_rotation_gate_decision.py
- Dependency/order: After T2

4. T4 - Implement rotation-checkpoint service
- Objective: Implement checkpoint registry and gate evaluation logic that satisfies T3.
- Target files: src/security/rotation_checkpoint_service.py, src/security/models/rotation_checkpoint.py, src/security/models/rotation_gate_decision.py, src/security/storage/rotation_checkpoint_store.py
- AC IDs: AC-002, AC-004
- Acceptance checklist:
	- [ ] Missing dependent systems are returned in missing_systems
	- [ ] Evidence count matches persisted evidence references
	- [ ] Gate cannot emit COMPLETE unless required systems have evidence
- Validation command: python -m pytest -q tests/security/test_rotation_checkpoint_service.py tests/security/test_rotation_gate_decision.py
- Dependency/order: After T3

5. T5 - Define local guardrail and CI policy tests
- Objective: Create failing tests for pre-commit secret scan policy and CI merge-block behavior.
- Target files: tests/security/test_secret_guardrail_policy.py, tests/security/test_ci_secret_guardrail_job.py, tests/security/test_pre_commit_secret_hook.py, .github/workflows/security.yml, .pre-commit-config.yaml
- AC IDs: AC-003, AC-006
- Acceptance checklist:
	- [ ] HIGH/CRITICAL findings force BLOCK in policy tests
	- [ ] CI workflow test asserts required job and fail-closed exit behavior
	- [ ] Local hook test validates scan invocation before commit
- Validation command: python -m pytest -q tests/security/test_secret_guardrail_policy.py tests/security/test_ci_secret_guardrail_job.py tests/security/test_pre_commit_secret_hook.py
- Dependency/order: After T4

6. T6 - Implement guardrail policy wiring
- Objective: Implement policy code and config wiring for local + CI guardrails.
- Target files: src/security/secret_guardrail_policy.py, src/security/models/guardrail_decision.py, .github/workflows/security.yml, .pre-commit-config.yaml, scripts/security/run_secret_scan.py
- AC IDs: AC-003, AC-006
- Acceptance checklist:
	- [ ] validate_pr and validate_push return BLOCK on HIGH/CRITICAL findings
	- [ ] Security CI job blocks merge on non-zero secret scan finding threshold
	- [ ] Pre-commit hook executes same scanner profile used by CI
- Validation command: python -m pytest -q tests/security/test_secret_guardrail_policy.py tests/security/test_ci_secret_guardrail_job.py tests/security/test_pre_commit_secret_hook.py
- Dependency/order: After T5

7. T7 - Containment operation tests and active-tree cleanup checks
- Objective: Add tests that enforce secret artifact removal and replacement/runbook correctness.
- Target files: tests/security/test_containment_cleanup.py, tests/security/test_private_key_artifact_absence.py, rust_core/2026-03-11-keys.priv, docs/security/private-key-remediation-runbook.md
- AC IDs: AC-001, AC-005
- Acceptance checklist:
	- [ ] Tests fail if sensitive artifact remains with key-like payload
	- [ ] Runbook includes containment evidence section with incident ID linkage
	- [ ] Cleanup rules are deterministic and repo-path scoped
- Validation command: python -m pytest -q tests/security/test_containment_cleanup.py tests/security/test_private_key_artifact_absence.py
- Dependency/order: After T6

8. T8 - Implement containment cleanup and runbook baseline
- Objective: Implement removal/replacement behavior and operational runbook content to satisfy T7.
- Target files: rust_core/2026-03-11-keys.priv, docs/security/private-key-remediation-runbook.md, scripts/security/verify_no_key_material.py
- AC IDs: AC-001, AC-005
- Acceptance checklist:
	- [ ] Active tree scan returns PASS in automated check path
	- [ ] Runbook references rotation checkpoint gate prerequisite for rewrite
	- [ ] Verification script exits non-zero if key signatures are detected
- Validation command: python -m pytest -q tests/security/test_containment_cleanup.py tests/security/test_private_key_artifact_absence.py
- Dependency/order: After T7

### Chunk 002 - Rewrite + Governance Completion

9. T9 - Define rewrite coordinator preflight/execute/post-verify tests
- Objective: Create failing tests for rewrite preflight gating, execution sequencing, and post-verify zero-match contract.
- Target files: tests/security/test_history_rewrite_coordinator.py, tests/security/test_rewrite_preflight_report.py, tests/security/test_rewrite_verification_report.py, src/security/history_rewrite_coordinator.py
- AC IDs: AC-004
- Acceptance checklist:
	- [ ] preflight requires RotationGateDecision COMPLETE
	- [ ] execute is blocked unless freeze-window flag is active
	- [ ] post_verify fails on any residual secret signature
- Validation command: python -m pytest -q tests/security/test_history_rewrite_coordinator.py tests/security/test_rewrite_preflight_report.py tests/security/test_rewrite_verification_report.py
- Dependency/order: After T8

10. T10 - Implement rewrite coordinator and reports
- Objective: Implement rewrite orchestration logic to satisfy T9 with deterministic reports.
- Target files: src/security/history_rewrite_coordinator.py, src/security/models/rewrite_preflight_report.py, src/security/models/rewrite_result.py, src/security/models/rewrite_verification_report.py, scripts/security/rewrite_history.ps1
- AC IDs: AC-004
- Acceptance checklist:
	- [ ] preflight fails closed when prerequisites are missing
	- [ ] execute stores run_id and scope summary for audit
	- [ ] post_verify reports zero matches across refs/tags on success
- Validation command: python -m pytest -q tests/security/test_history_rewrite_coordinator.py tests/security/test_rewrite_preflight_report.py tests/security/test_rewrite_verification_report.py
- Dependency/order: After T9

11. T11 - Define governance reporter and artifact sync tests
- Objective: Create failing tests for governance reporting and status artifact update flows.
- Target files: tests/security/test_governance_reporter.py, tests/security/test_project_status_sync.py, src/security/governance_reporter.py, docs/project/kanban.md, data/projects.json
- AC IDs: AC-005, AC-006
- Acceptance checklist:
	- [ ] Reporter output includes phase status, run_id, and blocking reasons
	- [ ] Artifact sync tests verify lane/status updates are deterministic
	- [ ] Missing required artifact link fails validation
- Validation command: python -m pytest -q tests/security/test_governance_reporter.py tests/security/test_project_status_sync.py
- Dependency/order: After T10

12. T12 - Implement governance reporting and status synchronization
- Objective: Implement governance reporter and project artifact sync logic for remediation lifecycle outputs.
- Target files: src/security/governance_reporter.py, scripts/security/sync_project_status.py, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.exec.md, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.ql.md
- AC IDs: AC-005, AC-006
- Acceptance checklist:
	- [ ] Governance report is generated for each phase transition
	- [ ] Incomplete signals keep status BLOCKED with explicit reason
	- [ ] Artifact links are emitted for @7exec/@8ql/@9git downstream verification
- Validation command: python -m pytest -q tests/security/test_governance_reporter.py tests/security/test_project_status_sync.py
- Dependency/order: After T11

13. T13 - Define contributor migration runbook tests
- Objective: Add failing tests that assert migration runbook completeness and communication checklist presence.
- Target files: tests/security/test_contributor_migration_runbook.py, docs/security/contributor-history-rewrite-migration.md
- AC IDs: AC-005
- Acceptance checklist:
	- [ ] Runbook includes reset/rebase/reclone paths and verification commands
	- [ ] Communication checklist includes owner and completion status fields
	- [ ] Missing rollback guidance fails tests
- Validation command: python -m pytest -q tests/security/test_contributor_migration_runbook.py
- Dependency/order: After T12

14. T14 - Implement contributor migration runbook and communication checklist
- Objective: Implement runbook content and checklist docs satisfying T13.
- Target files: docs/security/contributor-history-rewrite-migration.md, docs/security/private-key-remediation-runbook.md
- AC IDs: AC-005
- Acceptance checklist:
	- [ ] Migration steps are explicit, ordered, and branch-safe
	- [ ] Communication checklist includes responsible roles and completion evidence
	- [ ] Rollback guidance is present and aligned with rewrite coordinator behavior
- Validation command: python -m pytest -q tests/security/test_contributor_migration_runbook.py
- Dependency/order: After T13

15. T15 - End-to-end remediation scenario tests
- Objective: Add and pass integration tests that exercise containment -> verification -> rewrite -> stabilization flow.
- Target files: tests/security/test_secret_remediation_e2e.py, tests/security/fixtures/remediation_scenarios.py, src/security/control_plane_orchestrator.py
- AC IDs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006
- Acceptance checklist:
	- [ ] Scenario passes only when all phase gates are satisfied
	- [ ] Any gate failure yields deterministic BLOCKED outcome with reasons
	- [ ] Audit output includes incident_id, run_id, and artifact links
- Validation command: python -m pytest -q tests/security/test_secret_remediation_e2e.py
- Dependency/order: After T14

16. T16 - Implement orchestrator glue and final verification command bundle
- Objective: Implement final orchestration wiring and validation bundle for downstream agents.
- Target files: src/security/control_plane_orchestrator.py, scripts/security/validate_remediation_bundle.ps1, docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.test.md
- AC IDs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006
- Acceptance checklist:
	- [ ] Orchestrator executes phases in design-defined order with gate checks
	- [ ] Validation bundle command fails closed on any unresolved finding
	- [ ] Test artifact records command outputs and pass/fail summary
- Validation command: python -m pytest -q tests/security/test_secret_remediation_e2e.py
- Dependency/order: After T15

## Rollback And Safety Checkpoints

| Checkpoint | Phase Gate | Required Signal | Rollback Action if Failed |
|---|---|---|---|
| CP-01 | Before containment close | Tree scan PASS, no live key payload detected | Re-open containment; block all merges; rerun cleanup and tree scan |
| CP-02 | Before rewrite preflight | Rotation gate COMPLETE with evidence for every dependent system | Keep rewrite blocked; rotate missing systems; attach evidence URIs |
| CP-03 | Before rewrite execution | Freeze window activated and branch protection checks green | Abort rewrite run; cancel freeze; publish incident update |
| CP-04 | After rewrite execution | Post-verify zero matches across refs/tags | Revert rewritten refs from backup mirror; re-run rewrite with corrected scope |
| CP-05 | Before lane advancement to Review | Guardrail regression tests PASS (pre-commit + CI) | Keep lane In Sprint; repair policy wiring; rerun regression suite |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Chunk 001 tests authored and failing | T1, T3, T5, T7 | READY_FOR_@5test |
| M2 | Chunk 001 implementations complete | T2, T4, T6, T8 | PENDING_@6code |
| M3 | Chunk 002 tests authored and failing | T9, T11, T13, T15 | PENDING |
| M4 | Chunk 002 implementations complete | T10, T12, T14, T16 | PENDING |

## Handoff To @5test
- Handoff chunk: Chunk 001 only (T1, T3, T5, T7 first)
- TDD gate: @6code must not start T2/T4/T6/T8 until corresponding tests fail and are committed in working tree
- Definition of ready for @6code: all Chunk 001 test tasks have deterministic failing assertions and documented fixtures

## Global Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/security
python -m mypy src/security
python -m ruff check src/security tests/security
```
