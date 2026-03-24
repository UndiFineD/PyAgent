# hmac-webhook-verification — Security / QL Review

_Owner: @8ql | Status: CLEARED_

## OWASP Top 10 Review

### Injection (A03)

- `json.loads(body)` is called on untrusted bytes. Python's `json` module is safe
  against injection; it does not evaluate code.
- The secret is never interpolated into shell commands or SQL queries.

### Cryptographic Failures (A02)

- HMAC-SHA256 is the algorithm specified by GitHub. **Do not downgrade** to MD5 or
  SHA1.
- `hmac.compare_digest` prevents timing side-channels. **Must not** be replaced
  with `==`.

### Identification and Authentication Failures (A07)

- If `GITHUB_WEBHOOK_SECRET` is not set, requests are allowed through with a warning.
  This is intentional for dev mode. Production deployments **must** set the env var.
- The 401 response detail must not reveal the computed hash or the secret.

### Broken Access Control (A01)

- Verification runs before any event handler, preventing bypass.

### Security Misconfiguration (A05)

- Warn loudly (log at WARNING level) when secret is absent, so operators notice.

## CodeQL Notes

- No new `exec()`, `eval()`, or shell calls introduced.
- No new SQL or template injection surfaces.
- `hmac.compare_digest` satisfies timing-safe comparison rule.

## Checklist

- [x] `hmac.compare_digest` used (not `==`)
- [x] Secret read from env, not hardcoded
- [x] 401 detail message does not leak hash or secret
- [x] Warning logged when secret is absent
- [x] No new untrusted string interpolation
