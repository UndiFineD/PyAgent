# agent-memory-persistence — Exec Notes

_Owner: @7exec_

## Validation commands

```powershell
# Activate venv
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Run tests
pytest tests/test_agent_memory.py -v

# Run full backend test suite to check for regressions
pytest tests/ -v --timeout=30
```

## Expected results

- All 6 tests in `test_agent_memory.py` pass
- No regressions in existing test files

## Runtime notes

- `data/agents/` directory will be created at runtime on first append call
- No migration needed — first write creates the file
- Tests use mocking to avoid actual disk I/O
