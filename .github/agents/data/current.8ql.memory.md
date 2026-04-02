# Current Memory - 8ql

## Metadata
- agent: @8ql
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-31
- rollover: At new project start, append this file's entries to history.8ql.memory.md in chronological order, then clear Entries.

## Entries

## Last scan - 2026-04-02
- task_id: prj0000115-ci-security-quality-workflow-consolidation
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000115-ci-security-quality-workflow-consolidation (validated)
- files scanned: .github/workflows/security-scheduled.yml; tests/ci/test_security_workflow.py; tests/ci/test_ci_workflow.py; tests/test_generate_legacy_ideas.py; tests/test_idea_tracker.py; tests/docs/test_agent_workflow_policy_docs.py
- security/quality checks run:
	- git branch --show-current
	- git pull
	- & .\.venv\Scripts\Activate.ps1
	- python -m pytest -q tests/ci/test_security_workflow.py tests/ci/test_ci_workflow.py
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- ruff check .github/workflows/security-scheduled.yml tests/ci/test_security_workflow.py tests/ci/test_ci_workflow.py tests/test_generate_legacy_ideas.py tests/test_idea_tracker.py
	- python -m pip_audit -r requirements.txt -r requirements-ci.txt
- findings:
	- PASS: branch gate validated and branch is up to date with remote
	- PASS: required CI/security workflow selectors passed (14 passed)
	- BASELINE NON-BLOCKING: docs policy selector has known legacy missing file only (`docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`)
	- NON-BLOCKING: Ruff reported 65 invalid-syntax errors when parsing workflow YAML as Python due to command target mix; no Python-file lint findings reported
	- PASS: dependency audit returned no vulnerabilities; HIGH/CRITICAL findings = 0
	- PASS: workflow security sanity review confirms minimal permissions and no PR-based trigger surface
- handoff target: @9git
- overall: CLEAN (PASS; no HIGH/CRITICAL blockers)

## Last scan - 2026-04-01
- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000110-idea000004-quality-workflow-branch-trigger (validated)
- files scanned: .github/workflows/ci.yml; tests/test_enforce_branch.py; tests/docs/test_agent_workflow_policy_docs.py; tests/ci/test_ci_workflow.py; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.plan.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.test.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.code.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.exec.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.ql.md
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- git diff --name-only HEAD -- .github/workflows/*.yml
	- python -m pytest -q tests/test_enforce_branch.py tests/docs/test_agent_workflow_policy_docs.py tests/ci/test_ci_workflow.py
	- .venv\Scripts\ruff.exe check src/ --select S --output-format concise
	- python -c <pip_audit_results baseline parser>
- findings:
	- PASS: branch gate matches expected project branch
	- PASS: required T-QWB-008 selector suite is green (44 passed)
	- PASS: workflow injection review on `.github/workflows/ci.yml` found no HIGH/CRITICAL conditions and explicit least-privilege permissions
	- PASS: dependency baseline file parsed (`BASELINE_DEPS_WITH_VULNS=0`)
	- MEDIUM/LOW/INFO baseline debt: existing Ruff S findings in `src/` outside active project scope (S310/S311/S101)
- unresolved quality debt:
	- none newly created for this project; existing cross-project ledger entries remain unchanged
- handoff target: @9git
- overall: CLEAN (no HIGH/CRITICAL security blockers)

## Last scan - 2026-03-31
- task_id: prj0000109-idea000002-missing-compose-dockerfile
- lifecycle: OPEN -> IN_PROGRESS -> BLOCKED
- branch: prj0000109-idea000002-missing-compose-dockerfile (validated)
- files scanned: deploy/compose.yaml; deploy/docker-compose.yaml; deploy/Dockerfile.pyagent; deploy/Dockerfile.fleet; tests/deploy/test_compose_dockerfile_paths.py; tests/deploy/test_compose_context_contract.py; tests/deploy/test_compose_dockerfile_regression_matrix.py; tests/deploy/test_compose_file_selection.py; tests/deploy/test_compose_non_goal_guardrails.py; tests/deploy/test_compose_scope_boundary_markers.py; tests/docs/test_agent_workflow_policy_docs.py; docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md; docs/project/kanban.json
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- git diff --name-only HEAD -- .github/workflows/*.yml
	- python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_context_contract.py tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- .venv\Scripts\ruff.exe check --select S --output-format concise -- tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_context_contract.py tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py tests/docs/test_agent_workflow_policy_docs.py
	- .venv\Scripts\ruff.exe format --check tests/deploy/test_compose_scope_boundary_markers.py tests/docs/test_agent_workflow_policy_docs.py
	- python scripts/project_registry_governance.py validate
	- pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json
	- python -c <pip baseline vs current CVE delta parser>
- findings:
	- PASS: branch gate matches expected project branch
	- PASS: targeted deploy gate (19 passed) and docs policy gate (15 passed)
	- PASS: exact formatter blocker recheck is green (`2 files already formatted`)
	- INFO: scoped Ruff S findings are test-only S101 asserts (non-blocking)
	- MEDIUM: baseline CVE drift vs committed `pip_audit_results.json` persists (requests/cryptography/pygments)
	- BLOCKER: `project_registry_governance.py validate` fails for prj0000109 lane mismatch (`json='Review'`, `kanban='Discovery'`) and pre-existing `docs/project/kanban.json` drift is out-of-scope per user constraint
- handoff target: @1project
- overall: BLOCKED (quality governance blocker; no HIGH/CRITICAL security findings)

## Last scan - 2026-03-31
- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000108-idea000019-crdt-python-ffi-bindings (validated)
- files scanned: docs/project/kanban.json; docs/project/kanban.md; docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.ql.md
- security/quality checks run:
	- git branch --show-current
	- git status --short
	- python scripts/project_registry_governance.py validate
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
- findings:
	- PASS: expected branch matches observed branch
	- PASS: exact blocker command re-run (`python scripts/project_registry_governance.py validate`) now returns `VALIDATION_OK`
	- PASS: docs policy gate remains green (`12 passed`)
	- MEDIUM: baseline CVE drift vs committed `pip_audit_results.json` persists (requests/cryptography/pygments), tracked as baseline quality debt outside lane-sync scope
- blocker remediation evidence:
	- prior blocker: lane mismatch for prj0000108 (`json='Review'`, `kanban='Discovery'`)
	- current state: lane normalized to `In Sprint` in registry artifacts; governance validator returns `VALIDATION_OK`
- handoff target: @9git
- overall: CLEAN (governance blocker closed; no HIGH/CRITICAL security blockers)

## Last scan - 2026-03-31
- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
- lifecycle: OPEN -> IN_PROGRESS -> BLOCKED
- branch: prj0000108-idea000019-crdt-python-ffi-bindings (validated)
- files scanned: src/core/crdt_bridge.py; tests/test_crdt_bridge.py; tests/test_crdt_ffi_contract.py; tests/test_crdt_ffi_validation.py; tests/test_crdt_payload_codec.py; tests/test_crdt_merge_determinism.py; tests/test_crdt_error_mapping.py; tests/test_crdt_ffi_observability.py; tests/test_crdt_ffi_feature_flag.py; tests/test_crdt_ffi_parity.py; tests/test_crdt_ffi_performance.py; docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.ql.md; docs/project/kanban.json
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- git diff --name-only origin/main...HEAD
	- git diff --name-only HEAD -- .github/workflows/*.yml
	- .venv\Scripts\ruff.exe check src/ --select S --output-format concise
	- .venv\Scripts\ruff.exe check --select S --output-format concise -- src/core/crdt_bridge.py tests/test_crdt_bridge.py tests/test_crdt_ffi_contract.py tests/test_crdt_ffi_validation.py tests/test_crdt_payload_codec.py tests/test_crdt_merge_determinism.py tests/test_crdt_error_mapping.py tests/test_crdt_ffi_observability.py tests/test_crdt_ffi_feature_flag.py tests/test_crdt_ffi_parity.py tests/test_crdt_ffi_performance.py
	- pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json
	- python -c <pip baseline vs current CVE delta parser>
	- python scripts/project_registry_governance.py validate
	- python scripts/architecture_governance.py validate
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
- findings:
	- PASS: branch gate and project scope inventory captured
	- PASS: workflow injection gate skipped (no workflow file changes)
	- PASS: architecture governance (`VALIDATION_OK`) and docs policy (`12 passed`)
	- INFO: scope-local Ruff S findings are test-only S101 asserts (non-blocking)
	- MEDIUM: baseline CVE drift vs committed `pip_audit_results.json` persists (requests/cryptography/pygments)
	- BLOCKER: registry governance lane mismatch for prj0000108 (`json='Review'`, `kanban='Discovery'`) with user constraint not to edit pre-existing unstaged `docs/project/kanban.json`
- handoff target: @1project
- overall: BLOCKED (quality governance blocker; no HIGH/CRITICAL security findings)

## Last scan - 2026-03-31
- task_id: prj0000107-idea000015-specialized-agent-library
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000107-idea000015-specialized-agent-library (validated)
- files scanned: docs/project/kanban.json; docs/project/kanban.md; .github/agents/0master.agent.md; .github/agents/1project.agent.md; .github/agents/2think.agent.md; .github/agents/3design.agent.md; .github/agents/4plan.agent.md; .github/agents/5test.agent.md; .github/agents/6code.agent.md; .github/agents/7exec.agent.md; .github/agents/8ql.agent.md; .github/agents/9git.agent.md; .github/agents/governance/shared-governance-checklist.md; docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.ql.md
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- git diff --name-only origin/main...HEAD
	- rg -n "kanban\\.md" .github/agents/0master.agent.md .github/agents/1project.agent.md .github/agents/2think.agent.md .github/agents/3design.agent.md .github/agents/4plan.agent.md .github/agents/5test.agent.md .github/agents/6code.agent.md .github/agents/7exec.agent.md .github/agents/8ql.agent.md .github/agents/9git.agent.md .github/agents/governance/shared-governance-checklist.md
	- .venv\Scripts\ruff.exe check --select S --output-format concise -- <HEAD .py files>
	- python scripts/project_registry_governance.py validate
	- python scripts/project_registry_governance.py set-lane --id prj0000107 --lane Review
	- python scripts/project_registry_governance.py validate
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json
	- python -c <pip baseline vs current CVE delta parser>
- findings:
	- PASS: branch gate and scope inventory capture
	- PASS: requested agent/governance files contain no `kanban.md` references
	- PASS: docs policy gate (12 passed)
	- PASS: registry governance after lane sync remediation (`set-lane` then `VALIDATION_OK`)
	- MEDIUM: baseline CVE drift persists outside active docs/governance scope (requests/cryptography/pygments)
- unresolved quality debt:
	- id: QD-8QL-0005
	- owner: @6code
	- originating project: prj0000107-idea000015-specialized-agent-library
	- status: OPEN
	- exit criteria: update or risk-accept requests/cryptography/pygments CVEs and refresh committed pip_audit_results.json baseline
- handoff target: @9git
- overall: CLEAN (no HIGH/CRITICAL security blockers; quality debt recorded)

## Last scan - 2026-03-30
- task_id: prj0000106-idea000080-smart-prompt-routing-system
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000106-idea000080-smart-prompt-routing-system (validated)
- files scanned: src/core/routing/*; tests/core/routing/*; tests/test_core_routing_*; tests/test_conftest.py; docs/project/prj0000106-idea000080-smart-prompt-routing-system/*; docs/project/kanban.json
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- git diff --name-only HEAD -- .github/workflows/*.yml
	- .venv\Scripts\ruff.exe check src/ --select S --output-format concise
	- .venv\Scripts\ruff.exe check src/core/routing tests/core/routing tests/test_core_routing_classifier_schema.py tests/test_core_routing_confidence_calibration.py tests/test_core_routing_fallback_reason_taxonomy.py tests/test_core_routing_guardrail_policy_engine.py tests/test_core_routing_policy_versioning.py tests/test_core_routing_prompt_semantic_classifier.py tests/test_core_routing_request_normalizer.py tests/test_core_routing_routing_fallback_policy.py tests/test_core_routing_routing_models.py tests/test_core_routing_routing_policy_loader.py tests/test_core_routing_shadow_mode_router.py --select S --output-format concise
	- pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json
	- python -c <pip baseline vs current CVE delta parser>
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- python scripts/project_registry_governance.py validate
	- python scripts/architecture_governance.py validate
- findings:
	- PASS: branch gate, workflow-change gate, docs policy gate, architecture governance gate
	- PASS: scoped routing security posture shows test-only S101 findings; no HIGH/CRITICAL issues
	- MEDIUM: project registry governance lane mismatch for prj0000106 (`json='Review'`, `kanban='Discovery'`)
	- MEDIUM: baseline CVE drift outside active routing scope (requests/cryptography/pygments)
- handoff target: @9git
- overall: CLEAN (no HIGH/CRITICAL security blockers; quality debts tracked in unresolved ledger)

### Lesson
- Pattern: Registry lane mismatch between `data/projects.json` and `docs/project/kanban.md` can recur even after prior remediation if lane updates are not validated at project close.
- Root cause: Lifecycle lane transition was not synchronized across both registry sources before @8ql gate.
- Prevention: Require a mandatory paired lane update and immediate `python scripts/project_registry_governance.py validate` during project lifecycle transitions before @7exec/@8ql handoff.
- First seen: prj0000105-idea000016-mixin-architecture-base
- Seen in: prj0000105-idea000016-mixin-architecture-base, prj0000106-idea000080-smart-prompt-routing-system, prj0000107-idea000015-specialized-agent-library, prj0000108-idea000019-crdt-python-ffi-bindings, prj0000109-idea000002-missing-compose-dockerfile
- Recurrence count: 5
- Promotion status: HARD

## Last scan - 2026-03-30
- task_id: prj0000105-idea000016-mixin-architecture-base
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000105-idea000016-mixin-architecture-base (validated)
- files scanned: src/core/base/mixins/*; src/core/audit/AuditTrailMixin.py; src/core/sandbox/SandboxMixin.py; src/core/replay/ReplayMixin.py; src/tools/dependency_audit.py; tests/core/base/mixins/*; tests/test_core_base_mixins_*; docs/project/prj0000105-idea000016-mixin-architecture-base/*; docs/project/kanban.json; docs/project/kanban.md; docs/architecture/adr/0003-base-mixin-canonical-namespace-and-shim-policy.md
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py tests/core/base/mixins/test_import_smoke.py tests/core/base/mixins/test_shim_expiry_gate.py tests/core/base/mixins/test_migration_events.py
	- python scripts/project_registry_governance.py validate
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- .venv\Scripts\ruff.exe check --select S --output-format concise -- <changed .py files>
	- python -m pytest -q tests/core/base/mixins tests/test_core_quality.py::test_each_core_has_test_file tests/test_core_quality.py::test_validate_function_exists
	- python scripts/architecture_governance.py validate
	- pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json
	- python -c <pip baseline vs current delta parser>
- findings:
	- PASS: exact prior failing selector bundle rerun first -> 13 passed
	- PASS: registry governance -> VALIDATION_OK
	- PASS: docs policy -> 12 passed
	- PASS: aggregate mixin + core-quality selectors -> 27 passed
	- INFO: Ruff S scan found S101 in src/core/sandbox/SandboxMixin.py only
	- MEDIUM: CVE baseline drift persists (requests/cryptography/pygments), tracked as unresolved baseline quality debt QD-8QL-0001
- handoff target: @9git
- overall: CLEAN (no HIGH/CRITICAL security findings; all project quality gates pass)

## Last scan - 2026-03-30
- task_id: prj0000105-idea000016-mixin-architecture-base
- lifecycle: OPEN -> IN_PROGRESS -> BLOCKED
- branch: prj0000105-idea000016-mixin-architecture-base (validated)
- files scanned: src/core/base/mixins/*; src/core/audit/AuditTrailMixin.py; src/core/sandbox/SandboxMixin.py; src/core/replay/ReplayMixin.py; src/tools/dependency_audit.py; tests/core/base/mixins/*; tests/test_core_base_mixins_*; docs/project/kanban.json; docs/project/kanban.md; docs/project/prj0000105-idea000016-mixin-architecture-base/*; docs/architecture/adr/0003-base-mixin-canonical-namespace-and-shim-policy.md
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- git diff --name-only origin/main...HEAD
	- .venv\Scripts\ruff.exe check src/core/base/mixins src/core/audit/AuditTrailMixin.py src/core/sandbox/SandboxMixin.py src/core/replay/ReplayMixin.py src/tools/dependency_audit.py tests/core/base/mixins tests/test_core_base_mixins_audit_mixin.py tests/test_core_base_mixins_base_behavior_mixin.py tests/test_core_base_mixins_replay_mixin.py tests/test_core_base_mixins_sandbox_mixin.py --select S --output-format concise
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- python scripts/project_registry_governance.py validate
	- python scripts/architecture_governance.py validate
	- python -m pytest -q tests/core/base/mixins
	- python -m pytest -q tests/core/base/mixins/test_mixin_behavior_parity.py tests/core/base/mixins/test_import_smoke.py tests/core/base/mixins/test_shim_expiry_gate.py tests/core/base/mixins/test_migration_events.py
	- python -c <plan-target file existence audit>
	- python -c <pip_audit_results.json parser>
- findings:
	- BLOCKER: project registry governance failure (`Lane mismatch for prj0000105: json='Review', kanban='Discovery'`)
	- BLOCKER: missing T007-T011 planned deliverables (8 files absent)
	- BLOCKER: AC-MX-004/005/006/007 selector evidence missing (test files absent)
	- INFO: Ruff S101 findings only (2 production-scope asserts, remainder in tests); no HIGH/CRITICAL security issue
	- INFO: pip-audit baseline shows 0 vulnerable dependencies
- handoff target: @6code
- overall: BLOCKED (quality/delivery blockers; security clean for HIGH/CRITICAL)

### Lesson
- Pattern: Registry lane drift between `docs/project/kanban.json` and `docs/project/kanban.md` can survive until governance validation is run at @8ql.
- Root cause: Registry updates in one representation were not mirrored in the other.
- Prevention: Require paired lane update plus immediate `python scripts/project_registry_governance.py validate` before @7exec handoff.
- First seen: prj0000105-idea000016-mixin-architecture-base
- Seen in: prj0000105-idea000016-mixin-architecture-base
- Recurrence count: 1
- Promotion status: CANDIDATE

### Lesson
- Pattern: Chunked implementation scopes create closure ambiguity when undelivered plan tasks are not listed in `## Deferred Items`.
- Root cause: `code.md` reported DONE for Chunk A but did not explicitly defer T007-T011.
- Prevention: When partial plan execution is intentional, mandate explicit deferred-task table with AC impact and next owner before @8ql handoff.
- First seen: prj0000105-idea000016-mixin-architecture-base
- Seen in: prj0000105-idea000016-mixin-architecture-base
- Recurrence count: 1
- Promotion status: CANDIDATE

## Last scan - 2026-03-29
- task_id: prj0000101-pending-definition
- lifecycle: IN_PROGRESS -> DONE
- branch: prj0000101-pending-definition (validated)
- files scanned: backend/app.py; tests/backend/test_health_probes_contract.py; tests/backend/test_health_probes_access_control.py; tests/backend/test_health_probes_security.py
- security/quality checks run:
	- python -m ruff check backend/app.py tests/backend/test_health_probes_contract.py tests/backend/test_health_probes_access_control.py tests/backend/test_health_probes_security.py
	- python -m mypy --config-file mypy.ini backend/app.py
- findings: LOW (lint-only) in backend/app.py, remediated in-scope
- rerun evidence: ruff PASS; mypy PASS
- handoff target: @9git
- overall: CLEAN (requested slice scope)

## Last scan - 2026-03-30
- task_id: prj0000104-idea000014-processing
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- branch: prj0000104-idea000014-processing (validated)
- files scanned: scripts/deps/generate_requirements.py; scripts/deps/check_dependency_parity.py; install.ps1; requirements-ci.txt; tests/deps/*; tests/structure/test_kanban.py; docs/project/prj0000104-idea000014-processing/*
- security/quality checks run:
	- git branch --show-current
	- git diff --name-only HEAD
	- git ls-files --others --exclude-standard
	- .venv\Scripts\ruff.exe check scripts/deps/check_dependency_parity.py scripts/deps/generate_requirements.py tests/deps/test_dependency_parity_gate.py tests/deps/test_generate_requirements_deterministic.py tests/deps/test_install_compatibility_contract.py tests/deps/test_manual_requirements_edit_detected.py tests/deps/test_pyproject_parse_failure.py tests/structure/test_kanban.py --select S --output-format concise
	- python -m pytest -q tests/deps
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- python scripts/project_registry_governance.py validate
	- pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json
- findings:
	- MEDIUM: CVE baseline drift detected (current audit reports 3 CVEs while committed baseline reports 0)
	- INFO: Ruff S101/S603 findings in test files only (non-blocking)
- rerun evidence: exact failing selector rerun captured in exec artifact (`tests/deps/test_generate_requirements_deterministic.py` => 3 passed)
- unresolved quality debt:
	- id: QD-8QL-0001
	- owner: @6code
	- originating project: prj0000104-idea000014-processing
	- status: OPEN
	- exit criteria: update or risk-accept requests/cryptography/pygments CVEs and refresh committed pip_audit_results.json baseline
- handoff target: @9git
- overall: CLEAN (no HIGH/CRITICAL blockers)

### Lesson
- Pattern: `pip-audit --output json` is not reliable across environments; explicit `-f json` is required for machine-readable comparison.
- Root cause: Output-format flag mismatch produced table output and broke JSON baseline parsing.
- Prevention: Standardize `pip-audit -f json -o <file>` in @8ql procedure and verify JSON parse before delta classification.
- First seen: prj0000104-idea000014-processing
- Seen in: prj0000104-idea000014-processing
- Recurrence count: 1
- Promotion status: CANDIDATE

### Lesson
- Pattern: CVE baseline drift can emerge as non-project-specific debt and still requires explicit owner and closure criteria.
- Root cause: committed baseline lagged current environment audit state.
- Prevention: Always run `pip-audit -f json -o .github/agents/data/pip_audit_current_8ql.json` and classify findings as baseline debt when drift is outside active project scope; require explicit ledger owner and exit criteria before @9git handoff.
- First seen: prj0000104-idea000014-processing
- Seen in: prj0000104-idea000014-processing, prj0000105-idea000016-mixin-architecture-base, prj0000107-idea000015-specialized-agent-library
- Recurrence count: 3
- Promotion status: HARD

## Promotions
## Promotion - 2026-03-30
- Lesson: Registry lane mismatch between `data/projects.json` and `docs/project/kanban.md` must be prevented with paired updates and immediate validation.
- Promoted to: .github/agents/8ql.agent.md § Learning loop rules
- Trigger project: prj0000106

## Promotion - 2026-03-30
- Lesson: CVE baseline drift can emerge as non-project-specific debt and still requires explicit owner and closure criteria.
- Promoted to: .github/agents/8ql.agent.md § Learning loop rules
- Trigger project: prj0000105

## Unresolved Quality Debt Ledger
- QD-8QL-0001 | owner=@6code | origin=prj0000104-idea000014-processing | status=OPEN | exit=upgrade or accept risk for CVE-2026-25645, CVE-2026-34073, CVE-2026-4539 and refresh committed baseline
- QD-8QL-0004 | owner=@1project | origin=prj0000106-idea000080-smart-prompt-routing-system | status=OPEN | exit=synchronize lane state for prj0000106 in data/projects.json and docs/project/kanban.md, then rerun project_registry_governance.py validate to VALIDATION_OK
- QD-8QL-0005 | owner=@6code | origin=prj0000107-idea000015-specialized-agent-library | status=OPEN | exit=upgrade or accept risk for CVE-2026-25645, CVE-2026-34073, CVE-2026-4539 and refresh committed baseline
- QD-8QL-0007 | owner=@6code | origin=prj0000108-idea000019-crdt-python-ffi-bindings | status=OPEN | exit=upgrade or accept risk for CVE-2026-25645, CVE-2026-34073, CVE-2026-4539 and refresh committed baseline
- QD-8QL-0008 | owner=@1project | origin=prj0000109-idea000002-missing-compose-dockerfile | status=OPEN | exit=synchronize lane state for prj0000109 in data/projects.json and docs/project/kanban.json, then rerun project_registry_governance.py validate to VALIDATION_OK

