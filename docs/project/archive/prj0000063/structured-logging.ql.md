# structured-logging — CodeQL / Security Review
_Owner: @8ql | Status: DONE_

## Security Review

### Threat Model

| Threat | Severity | Mitigated? |
|---|---|---|
| Log injection via `X-Correlation-ID` header | Medium | ✅ JSON encoding prevents control-character injection |
| PII leakage in logs | High | ✅ Only correlation ID + endpoint logged; no user data |
| Correlation ID spoofing | Low | Acceptable: correlation IDs are tracing aids, not auth signals |
| JSON formatter crash → service degradation | Low | ✅ Idempotent guard prevents reconfiguration loops |

### OWASP Top 10 Checklist

| # | Category | Status |
|---|---|---|
| A01 | Broken Access Control | Not applicable — logging module has no auth |
| A02 | Cryptographic Failures | Not applicable — no secrets in log entries |
| A03 | Injection | ✅ JSON encoding sanitises header values |
| A04 | Insecure Design | ✅ Structured logging improves auditability |
| A05 | Security Misconfiguration | ✅ Log level configurable via env; default INFO |
| A06 | Vulnerable Components | ✅ `python-json-logger>=2.0.0` — no known CVEs |
| A07 | Auth Failures | Not applicable |
| A08 | Software Integrity Failures | Not applicable |
| A09 | Security Logging & Monitoring | ✅ This project IS the improvement |
| A10 | SSRF | Not applicable |

### CodeQL Queries Run

- `python/log-injection` — CLEAN
- `python/clear-text-logging-sensitive-data` — CLEAN

### Recommendation

Extend `CorrelationIdMiddleware` to store `correlation_id` in a `ContextVar` in a
future sprint so all log sites in a request chain automatically carry the ID without
explicit `extra={}` passing.
