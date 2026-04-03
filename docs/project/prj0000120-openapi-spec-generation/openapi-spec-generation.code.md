# openapi-spec-generation - Code Artifacts

_Status: HANDED_OFF_
_Coder: @6code | Updated: 2026-04-03_

## Implementation Summary
Implemented the minimal phase-one green path without broadening scope beyond the declared files. The new generator script imports `backend.app` only, writes a deterministic committed artifact to `docs/api/openapi/backend_openapi.json`, the API docs index now links to that JSON as a consumer-only asset, and lightweight CI now runs only the existing drift selector `tests/docs/test_backend_openapi_drift.py -q` without adding generation or MkDocs build ownership.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| scripts/generate_backend_openapi.py | Added explicit backend-only OpenAPI generator entrypoint. | +57/-0 |
| docs/api/openapi/backend_openapi.json | Generated and committed canonical backend OpenAPI artifact from `backend.app.openapi()`. | +5602/-0 |
| docs/api/index.md | Added consumer-only link to the committed backend OpenAPI JSON artifact. | +6/-0 |
| .github/workflows/ci.yml | Added lightweight backend drift selector step to the quick CI job. | +2/-0 |
| docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.code.md | Recorded implementation evidence, AC mapping, and validation results. | +10/-3 |
| .github/agents/data/current.6code.memory.md | Recorded task lifecycle, validation evidence, and lesson. | +20/-0 |
| .github/agents/data/2026-04-03.6code.log.md | Recorded the prj0000120 implementation session. | +7/-0 |

## AC Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-OAS-001 | `scripts/generate_backend_openapi.py` | `c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/generate_backend_openapi.py` | PASS |
| AC-OAS-002 | `docs/api/openapi/backend_openapi.json` | `tests/docs/test_backend_openapi_drift.py` | PASS |
| AC-OAS-003 | `docs/api/openapi/backend_openapi.json`, `scripts/generate_backend_openapi.py` | `tests/docs/test_backend_openapi_drift.py` | PASS |
| AC-OAS-004 | `.github/workflows/ci.yml` | `rg -n "test_backend_openapi_drift.py|pytest tests/docs/test_backend_openapi_drift.py -q|generate_backend_openapi|mkdocs build" .github/workflows/ci.yml` | PASS |
| AC-OAS-005 | `docs/api/index.md` | `rg -n "openapi/backend_openapi.json|OpenAPI Artifact|docs site consumes it" docs/api/index.md` | PASS |
| AC-OAS-006 | `scripts/generate_backend_openapi.py` | `tests/docs/test_backend_openapi_drift.py`; `rg -n "backend\.app|src\.github_app|src\.chat\.api|from backend\.app import app" scripts/generate_backend_openapi.py` | PASS |

## Test Run Results
```
Generator:
- & c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/generate_backend_openapi.py
- Result: PASS
- Output: Wrote backend OpenAPI artifact to C:\Dev\PyAgent\docs\api\openapi\backend_openapi.json

Lint/docstrings:
- c:/Dev/PyAgent/.venv/Scripts/ruff.exe check --fix scripts/generate_backend_openapi.py
- c:/Dev/PyAgent/.venv/Scripts/ruff.exe check scripts/generate_backend_openapi.py
- c:/Dev/PyAgent/.venv/Scripts/ruff.exe check --select D scripts/generate_backend_openapi.py
- Result: PASS

Pytest selectors:
- tests/docs/test_backend_openapi_drift.py -> <summary passed=3 failed=0 />
- tests/docs/test_agent_workflow_policy_docs.py -> <summary passed=17 failed=0 />

Scope/contract checks:
- docs/api/index.md grep -> PASS (artifact link present)
- .github/workflows/ci.yml grep -> PASS (narrow drift selector present; no generation or mkdocs build step added)
- scripts/generate_backend_openapi.py placeholder scan -> PASS (no forbidden placeholders)
```

## Deferred Items
None.