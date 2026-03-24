# hmac-webhook-verification — Exec Notes

_Owner: @7exec | Status: DONE — 15/15 passed_

## Validation Commands

```powershell
# Activate venv
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Run HMAC-specific tests
pytest tests/test_github_app.py -v

# Full suite smoke
pytest src/ -x -q
```

## Expected Results

- `tests/test_github_app.py`: 15 passed (7 existing + 8 new)
- Full suite: no regressions

## Notes

- If `test_webhook_no_secret_configured` fails with 401, the monkeypatch is not
  reaching the module attribute. Check that `monkeypatch.setattr(gha, "WEBHOOK_SECRET", "")` is used correctly.
- If existing tests fail with 401, confirm that `GITHUB_WEBHOOK_SECRET` env var is
  not set in the test environment.
