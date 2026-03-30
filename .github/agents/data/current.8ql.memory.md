# Current Memory - 8ql

## Metadata
- agent: @8ql
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-29
- rollover: At new project start, append this file's entries to history.8ql.memory.md in chronological order, then clear Entries.

## Entries

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
- Prevention: track unresolved quality debt ledger entry with owner, source project, and exit criteria before @9git handoff.
- First seen: prj0000104-idea000014-processing
- Seen in: prj0000104-idea000014-processing
- Recurrence count: 1
- Promotion status: CANDIDATE

## Promotions
- none in this scan

## Unresolved Quality Debt Ledger
- QD-8QL-0001 | owner=@6code | origin=prj0000104-idea000014-processing | status=OPEN | exit=upgrade or accept risk for CVE-2026-25645, CVE-2026-34073, CVE-2026-4539 and refresh committed baseline

