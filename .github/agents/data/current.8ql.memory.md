# Current Memory - 8ql

## Metadata
- agent: @8ql
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-29
- rollover: At new project start, append this file's entries to history.8ql.memory.md in chronological order, then clear Entries.

## Entries

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
- Seen in: prj0000105-idea000016-mixin-architecture-base, prj0000106-idea000080-smart-prompt-routing-system, prj0000107-idea000015-specialized-agent-library
- Recurrence count: 3
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

