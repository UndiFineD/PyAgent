# hmac-webhook-verification — Design

_Owner: @3design | Status: DONE_

## Selected Design

### Helper function (new, module-level)

```python
import hashlib
import hmac
import json
import os
from typing import Optional

WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")

def verify_github_signature(
    secret: str,
    body: bytes,
    signature_header: Optional[str],
) -> bool:
    """Return True iff the HMAC-SHA256 signature matches the body.

    Uses hmac.compare_digest for constant-time comparison.
    Returns False if signature_header is None, empty, or malformed.
    """
    if not secret or not signature_header:
        return False
    if not signature_header.startswith("sha256="):
        return False
    received = signature_header.split("=", 1)[1]
    computed = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, received)
```

### Webhook endpoint modification

```python
@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(default=""),
    x_hub_signature_256: Optional[str] = Header(default=None),
) -> dict:
    body = await request.body()            # raw bytes for HMAC
    if WEBHOOK_SECRET:
        if not verify_github_signature(WEBHOOK_SECRET, body, x_hub_signature_256):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing webhook signature",
            )
    payload = json.loads(body)             # decode AFTER verification
    ...
```

## Interface Contract

| Input | Type | Notes |
|---|---|---|
| `secret` | `str` | empty string → return False |
| `body` | `bytes` | raw request body |
| `signature_header` | `Optional[str]` | `X-Hub-Signature-256` value |
| **return** | `bool` | True only on valid match |

## Module-level Config

`WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")` — evaluated at import time.
Tests that need to exercise the secret-set path can monkeypatch this module attribute.

## Error Handling

- 401 returned with plain-text detail (not exposing secret or computed hash).
- No 400/422; missing header is treated as "failed verification".
- When secret not set: request passes through, no error, warning logged only.
