# hmac-webhook-verification — Think / Analysis

_Owner: @2think | Status: DONE_

## Problem Statement

`src/github_app.py` blindly accepts all POST requests to `/webhook`. Any actor who
knows the URL can send a crafted payload, potentially triggering CI pipelines,
code pushes, or agent tasks.

GitHub provides a mechanism to prevent this: a shared HMAC secret is configured in the
GitHub repo settings and the webhook URL handling. Every POST carries the header
`X-Hub-Signature-256: sha256=<hex-digest>` where the digest is
`HMAC-SHA256(secret, raw_body)`.

## Why Raw Body Must Be Read First

The current handler calls `await request.json()` immediately. FastAPI parses the body
into a Python dict at that point. The HMAC must be verified against the *raw bytes*
before any deserialization. The fix is to:

```python
body = await request.body()          # raw bytes — for HMAC
payload = json.loads(body)           # re-deserialize after verification
```

## Backward Compatibility Requirement

Many dev environments run without a configured secret. Enforcing HMAC verification in
all cases would break local development immediately. Solution: if `GITHUB_WEBHOOK_SECRET`
environment variable is not set (or is empty), emit a warning log and allow the request
through. Once set, the gate is enforced.

## Timing Attack Risk

A naive `==` comparison leaks information about where disagreement occurs. Python's
`hmac.compare_digest` is constant-time and must be used instead.

## Alternatives Considered

1. **Middleware approach** — Intercept at Starlette middleware level. Rejected: harder
   to test, couples unrelated request paths.
2. **Dependency injection** — FastAPI `Depends(verify_hmac)`. Viable but adds complexity
   for a single endpoint. Rejected in favor of inline call with extracted helper.
3. **Third-party library** — `python-github-webhooks`. Rejected: adds dependency for
   ~15 lines of code.

## Conclusion

Add a standalone `verify_github_signature(secret, body, sig_header)` function.
Call it in the `webhook()` handler after reading raw body bytes. Gate on
`GITHUB_WEBHOOK_SECRET`. This is minimal, testable, and backward-compatible.
