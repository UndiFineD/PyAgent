# n8n-workflow-bridge - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-27_

## Implementation Summary
Implemented `src/core/n8nbridge/` v1 runtime package for green phase:
1. Added typed config model with `from_env()` parsing and `validate()` constraints.
2. Added event adapter with inbound/outbound canonical payload validation and mapping.
3. Added stdlib async HTTP client using `urllib.request` with timeout, retries, and response parsing.
4. Added bridge core orchestration with inbound idempotency TTL handling and outbound trigger result shaping.
5. Added mixin delegation helpers for host classes and a typed exception taxonomy.
6. Adjusted package exports to preserve monkeypatch module-path compatibility in tests.
7. Coverage blocker fix: expanded deterministic tests in `tests/test_n8n_bridge.py` to exercise previously uncovered config validation, adapter edge handling, HTTP retry/error branches, parser/backoff helpers, and module validation hook.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `src/core/n8nbridge/N8nBridgeConfig.py` | create | +111/-0 |
| `src/core/n8nbridge/N8nEventAdapter.py` | create | +126/-0 |
| `src/core/n8nbridge/N8nHttpClient.py` | create | +149/-0 |
| `src/core/n8nbridge/N8nBridgeCore.py` | create | +212/-0 |
| `src/core/n8nbridge/N8nBridgeMixin.py` | create | +65/-0 |
| `src/core/n8nbridge/exceptions.py` | create | +31/-0 |
| `src/core/n8nbridge/__init__.py` | create | +24/-0 |
| `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.code.md` | update | +4/-3 |

## Test Run Results
```
pytest tests/test_n8n_bridge.py -q --tb=short
31 passed in 1.77s

pytest tests/test_n8n_bridge.py --cov=src/core/n8nbridge --cov-report=term-missing --cov-fail-under=90 -q
Required test coverage of 90% reached. Total coverage: 99.11%
31 passed in 2.87s

python -m mypy src/core/n8nbridge --strict
Success: no issues found in 7 source files

python -m ruff check src/core/n8nbridge tests/test_n8n_bridge.py tests/test_N8nBridgeConfig.py tests/test_N8nEventAdapter.py tests/test_N8nHttpClient.py tests/test_N8nBridgeCore.py tests/test_N8nBridgeMixin.py
All checks passed!

.venv\Scripts\ruff.exe check --fix src/core/n8nbridge
Found 20 errors (20 fixed, 0 remaining)

.venv\Scripts\ruff.exe check src/core/n8nbridge
All checks passed!

python -m mypy --strict src/core/n8nbridge
Success: no issues found in 7 source files

rg --type py "raise NotImplementedError|raise NotImplemented\b|#\s*(TODO|FIXME|HACK|STUB|PLACEHOLDER)" src/core/n8nbridge tests/test_n8n_bridge.py tests/test_N8nBridgeConfig.py tests/test_N8nEventAdapter.py tests/test_N8nHttpClient.py tests/test_N8nBridgeCore.py tests/test_N8nBridgeMixin.py
rg --type py "^\s*\.\.\.\s*$" src/core/n8nbridge
No matches
```

## Deferred Items
none
