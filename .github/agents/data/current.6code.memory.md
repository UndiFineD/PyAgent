# Current Memory - 6code

## Metadata
- agent: @6code
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-30
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

## 2026-03-30 — prj0000104 green implementation
- task_id: prj0000104-idea000014-processing
- lifecycle: DONE
- branch: prj0000104-idea000014-processing (validated)
- changed files:
	- scripts/deps/generate_requirements.py
	- scripts/deps/check_dependency_parity.py
	- install.ps1
	- requirements-ci.txt
	- docs/project/prj0000104-idea000014-processing/idea000014-processing.code.md
- implementation summary:
	- Added deterministic `pyproject.toml` -> `requirements.txt` generator command.
	- Added parity check command with explicit remediation command text and manual-edit detection output.
	- Added install parity preflight invocation in install flow.
	- Added CI requirements guidance text that runtime requirements are generated from `pyproject.toml`.
- verification commands:
	- python -m pytest -q tests/deps/test_generate_requirements_deterministic.py
	- python -m pytest -q tests/deps
	- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	- ruff check --fix scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
	- ruff check scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
	- ruff check --select D scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
	- rg --type py "raise NotImplementedError|raise NotImplemented\\b|#\\s*(TODO|FIXME|HACK|STUB|PLACEHOLDER)" scripts/deps
	- rg --type py "^\\s*\\.\\.\\.\\s*$" scripts/deps
- unresolved risks:
	- none observed in task scope.
- handoff target: @7exec

## 2026-03-30 — prj0000104 @7exec deterministic-no-op blocker remediation
- task_id: prj0000104-idea000014-processing
- lifecycle: DONE
- branch: prj0000104-idea000014-processing (validated)
- changed files:
	- scripts/deps/generate_requirements.py
	- scripts/deps/check_dependency_parity.py
	- requirements.txt
	- docs/project/prj0000104-idea000014-processing/idea000014-processing.code.md
- implementation summary:
	- Added package-token normalization that preserves existing `requirements.txt` casing via canonical-name matching.
	- Applied identical normalization in parity checker expected-content generation.
	- Restored committed canonical casing for `pyjwt` and `sqlalchemy` in `requirements.txt`.
- verification commands:
	- .venv\Scripts\ruff.exe check --fix scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
	- .venv\Scripts\ruff.exe check scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
	- .venv\Scripts\ruff.exe check --select D scripts/deps/generate_requirements.py scripts/deps/check_dependency_parity.py
	- python -m pytest -q tests/deps
	- python -m pytest -q tests/deps/test_generate_requirements_deterministic.py tests/deps/test_dependency_parity_gate.py
	- python scripts/deps/generate_requirements.py --output requirements.txt
	- python scripts/deps/check_dependency_parity.py --check
	- git diff --exit-code -- requirements.txt
	- rg --type py "raise NotImplementedError|raise NotImplemented\\b|#\\s*(TODO|FIXME|HACK|STUB|PLACEHOLDER)" scripts/deps
	- rg --type py "^\\s*\\.\\.\\.\\s*$" scripts/deps
- unresolved risks:
	- none observed in scope.
- handoff target: @7exec

## 2026-03-30 — prj0000104 pre-commit E501 blocker remediation
- task_id: prj0000104-idea000014-processing
- lifecycle: DONE
- branch: prj0000104-idea000014-processing (validated)
- changed files:
	- tests/structure/test_kanban.py
	- docs/project/prj0000104-idea000014-processing/idea000014-processing.code.md
	- .github/agents/data/current.6code.memory.md
	- .github/agents/data/2026-03-30.6code.log.md
- implementation summary:
	- Applied a minimal non-behavioral line-wrap fix for the single overlong assert at line 154.
	- No refactors or logic changes were introduced.
- verification commands:
	- pre-commit run --files tests/structure/test_kanban.py
- unresolved risks:
	- none observed in scope.
- handoff target: @7exec

### Lesson
- Pattern: Dependency parity tests are satisfied fastest by a small deterministic CLI pair (generate/check) with explicit remediation output.
- Root cause: Required command contracts were absent (`scripts/deps` scripts and install/parity text contracts).
- Prevention: For dependency-governance tasks, scaffold generator/parity scripts first, then wire install/CI contract strings and run targeted selectors before aggregate gate.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing
- Recurrence count: 1
- Promotion status: Candidate

