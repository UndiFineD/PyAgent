# prj0000100-repo-cleanup-docs-code - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-29_

## Implementation Summary
Completed code-structure indexing accessibility split while preserving canonical governance entrypoint behavior.

- Canonical index at `.github/agents/data/codestructure.md` is now a lightweight manifest that points to six split domain index files.
- Split files were created for `backend`, `rust_core`, `scripts`, `src`, `tests`, and `web` using grouped `## <file>` plus `- line: code` rows.
- Non-target-root entries were preserved in canonical under `## Other` with grouped entries (`### <file>` plus `- line: code`) so no rows were silently dropped.
- Governance tests in `tests/docs/test_codestructure_governance.py` now validate canonical + split existence and row-shape integrity across all index files.

## Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-03 | `.github/agents/data/codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-03 | `.github/agents/data/backend.codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-03 | `.github/agents/data/rust_core.codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-03 | `.github/agents/data/scripts.codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-03 | `.github/agents/data/src.codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-03 | `.github/agents/data/tests.codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-03 | `.github/agents/data/web.codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-04 | `.github/agents/data/allowed_websites.md` | `tests/docs/test_allowed_websites_governance.py` | DONE |
| AC-05 | `.github/copilot-instructions.md` | `tests/docs/test_copilot_instructions_governance.py` | DONE |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `.github/agents/data/codestructure.md` | Converted to lightweight canonical manifest with split-file pointers and `Other` grouped rows | updated |
| `.github/agents/data/backend.codestructure.md` | Added split domain code-structure index for `backend` | added |
| `.github/agents/data/rust_core.codestructure.md` | Added split domain code-structure index for `rust_core` | added |
| `.github/agents/data/scripts.codestructure.md` | Added split domain code-structure index for `scripts` | added |
| `.github/agents/data/src.codestructure.md` | Added split domain code-structure index for `src` | added |
| `.github/agents/data/tests.codestructure.md` | Added split domain code-structure index for `tests` | added |
| `.github/agents/data/web.codestructure.md` | Added split domain code-structure index for `web` | added |
| `tests/docs/test_codestructure_governance.py` | Updated governance to validate canonical manifest, split files, and cross-file row integrity | updated |

## Test Run Results
```
pytest tests/docs/test_codestructure_governance.py
================================ test session starts =================================
platform win32 -- Python 3.13.12, pytest-9.0.2, pluggy-1.6.0
collected 3 items

tests\docs\test_codestructure_governance.py ...                                 [100%]

================================= 3 passed in 1.43s ==================================

pytest tests/docs/test_allowed_websites_governance.py tests/docs/test_copilot_instructions_governance.py
================================ test session starts =================================
platform win32 -- Python 3.13.12, pytest-9.0.2, pluggy-1.6.0
collected 4 items

tests\docs\test_allowed_websites_governance.py ..                               [ 50%]
tests\docs\test_copilot_instructions_governance.py ..                           [100%]

================================= 4 passed in 0.76s ==================================
```

## 2026-03-29 Follow-up Implementation (Memory/Log/Tooling Migration)

### Implementation Summary
- Added optional tooling and PostgreSQL support paths in `install.ps1` with non-fatal install/check behavior and CI-safe check-only fallback.
- Migrated agent memory files to `history.<agent>.memory.md`, created `current.<agent>.memory.md` templates, and updated agent operational references to target `current` files.
- Migrated agent logs to dated filenames (`2026-03-29.<agent>.log.md`) and updated `backend/app.py` log-path behavior to:
	- write to today's dated file,
	- read with fallback order: today -> latest dated file -> legacy non-dated filename.
- Added per-agent tooling and skill guidance docs under `.github/agents/tools/` and `.github/agents/skills/`.
- Updated affected tests for the new memory/log naming model.

### Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-01 | `install.ps1` | `pytest tests/docs/test_agent_workflow_policy_docs.py` | DONE |
| AC-01 | `.github/agents/0master.agent.md` .. `.github/agents/9git.agent.md` | `pytest tests/docs/test_agent_workflow_policy_docs.py` | DONE |
| AC-01 | `.github/agents/data/current.*.memory.md`, `.github/agents/data/history.*.memory.md` | `pytest tests/docs/test_agent_workflow_policy_docs.py` | DONE |
| AC-01 | `.github/agents/tools/*.tools.md`, `.github/agents/skills/*.skills.md` | `pytest tests/docs/test_agent_workflow_policy_docs.py` | DONE |
| AC-05 | `backend/app.py`, `tests/test_orchestration_graph.py` | `pytest tests/test_orchestration_graph.py` | DONE |

### Follow-up Validation Results
```
python -m pytest tests/docs/test_agent_workflow_policy_docs.py
12 passed in 2.72s

python -m pytest tests/test_orchestration_graph.py
5 passed in 3.56s

python -m pytest tests/docs/test_codestructure_governance.py tests/docs/test_allowed_websites_governance.py tests/docs/test_copilot_instructions_governance.py
7 passed in 2.28s
```

## Deferred Items
none
