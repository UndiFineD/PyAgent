# hmac-webhook-verification — Implementation Plan

_Owner: @4plan | Status: DONE_

## Task Breakdown

### T1 — Update imports in `src/github_app.py`

Add `hashlib`, `hmac`, `json`, `os`, `Optional` (from typing) to the import block.
Replace `await request.json()` with raw-body approach (see T3).

### T2 — Add module-level constant

```python
WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
```

Place after imports, before handler definitions.

### T3 — Add `verify_github_signature()` function

New function, module-level, before the `webhook` endpoint definition.
Signature: `(secret: str, body: bytes, signature_header: Optional[str]) -> bool`
Uses `hmac.compare_digest`. Returns `False` for missing/malformed header or empty secret.

### T4 — Modify `webhook()` endpoint

1. Add `x_hub_signature_256: Optional[str] = Header(default=None)` parameter.
2. Replace `payload = await request.json()` with:
   ```python
   body = await request.body()
   if WEBHOOK_SECRET:
       if not verify_github_signature(WEBHOOK_SECRET, body, x_hub_signature_256):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Invalid or missing webhook signature")
   payload = json.loads(body)
   ```

### T5 — Write tests in `tests/test_github_app.py`

New test cases to add:
1. `test_webhook_valid_hmac` — valid signature → 200
2. `test_webhook_invalid_hmac` — wrong signature → 401
3. `test_webhook_missing_signature_header` — secret set, no header → 401
4. `test_webhook_malformed_signature` — header lacks `sha256=` prefix → 401
5. `test_webhook_no_secret_configured` — no secret, no header → 200 (pass-through)
6. `test_verify_signature_helper_true` — unit test helper returns True for valid
7. `test_verify_signature_helper_false_wrong` — unit test helper returns False for wrong
8. `test_verify_signature_helper_false_empty_secret` — empty secret → False

### T6 — Validation

```powershell
pytest tests/test_github_app.py -v
```

All 6 existing tests + 8 new tests = 14 total expected to pass.

## Files Changed

| File | Change |
|---|---|
| `src/github_app.py` | Add helper + modify webhook endpoint |
| `tests/test_github_app.py` | Add 8 HMAC test cases |

## Validation Commands

```powershell
pytest tests/test_github_app.py -v
pytest src/ -x -q   # full suite smoke check
```
