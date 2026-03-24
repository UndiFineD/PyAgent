# hmac-webhook-verification — Code Notes

_Owner: @6code | Status: DONE_

## Implementation Checklist

- [ ] Update imports: `hashlib`, `hmac`, `json`, `os`, `Optional`
- [ ] Add `WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")`
- [ ] Add `verify_github_signature()` function
- [ ] Modify `webhook()` to read `body = await request.body()` + verify + `json.loads(body)`
- [ ] Add `x_hub_signature_256: Optional[str] = Header(default=None)` parameter
- [ ] Write 8 test cases in `tests/test_github_app.py`

## Notes

- Do NOT import `verify_github_signature` into tests with a relative import;
  use `import src.github_app as gha` + `monkeypatch.setattr(gha, "WEBHOOK_SECRET", ...)`.
- `hmac.new()` vs `hmac.HMAC()`: both work; prefer `hmac.new()` for clarity.
- FastAPI converts header name `X-Hub-Signature-256` → param `x_hub_signature_256`
  with lowercase + underscores automatically.
