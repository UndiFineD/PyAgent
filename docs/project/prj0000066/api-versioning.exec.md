# api-versioning — Exec Notes

_Owner: @7exec_

## Validation

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
pytest tests/test_api_versioning.py -v
pytest tests/test_backend_worker.py -v
```

## Expected

- 6/6 versioning tests pass
- Existing backend worker tests pass (no regressions)
