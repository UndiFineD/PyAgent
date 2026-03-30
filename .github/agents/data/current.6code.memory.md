# Current Memory - 6code

## Metadata
- agent: @6code
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-29
- rollover: At new project start, append this file's entries to history.6code.memory.md in chronological order, then clear Entries.

## Entries

## 2026-03-30 — prj0000102 T5/T6 implementation
- task_id: prj0000102-pyproject-requirements-sync
- lifecycle: DONE
- branch: prj0000102-pyproject-requirements-sync (validated)
- changed files:
	- src/tools/dependency_audit.py
	- scripts/ci/run_checks.py
	- tests/tools/test_dependency_audit.py
	- tests/structure/test_dependency_drift_ci.py
	- requirements.txt
	- docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.code.md
- implementation summary:
	- Added canonical dependency reader from pyproject `[project.dependencies]`.
	- Added deterministic requirements emitter and generation mode.
	- Added drift diff detection and policy enforcement (duplicate, malformed, critical package operators).
	- Wired blocking dependency sync gate into shared precommit/ci checks.
	- Added selector-aligned tests for canonical/deterministic/drift/policy contracts.
- verification commands:
	- python -m pytest -q tests -k "dependency and canonical and pyproject"
	- python -m pytest -q tests -k "requirements and deterministic"
	- python -m pytest -q tests/structure -k "dependency and drift and ci"
	- python -m pytest -q tests -k "dependency and policy"
	- ruff check --fix src/tools/dependency_audit.py scripts/ci/run_checks.py tests/tools/test_dependency_audit.py
	- ruff check src/tools/dependency_audit.py scripts/ci/run_checks.py tests/tools/test_dependency_audit.py
	- python -m mypy src/tools/dependency_audit.py scripts/ci/run_checks.py
- unresolved risks:
	- Existing repository-wide placeholder ellipsis instances outside scoped files remain and are not modified in this task.
- handoff target: @7exec
- commit: 5658a0e00

## 2026-03-30 — prj0000102 post-merge shard 10 dependency hotfix
- task_id: prj0000102-pyproject-requirements-sync
- lifecycle: DONE
- branch: prj0000102-pyproject-requirements-sync (validated)
- changed files:
	- pyproject.toml
	- requirements.txt
	- docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.code.md
- implementation summary:
	- Added `python-json-logger` for `pythonjsonlogger` test import.
	- Added `PyJWT` for `jwt` import from backend auth path.
	- Regenerated derived `requirements.txt` via `src.tools.dependency_audit --generate`.
- verification commands:
	- python -m pytest -q tests/test_structured_logging.py tests/test_watchdog.py
	- python -m pytest -q tests/tools/test_dependency_audit.py tests/structure/test_dependency_drift_ci.py
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
- unresolved risks:
	- none observed in scoped validation.
- handoff target: @7exec

