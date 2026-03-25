# api-versioning — Security Review

_Owner: @8ql_

## OWASP review

| Risk | Assessment |
|---|---|
| A01 Broken Access Control | Both `/api/` and `/api/v1/` protected by same `require_auth` dependency |
| A02 Cryptographic Failures | N/A |
| A03 Injection | No user input in routing logic |
| A04 Insecure Design | Backwards-compatible aliasing — no data exposure increase |
| A05 Misconfiguration | VersionHeaderMiddleware does not interfere with CORS or RateLimit headers |
| A06 Components | No new dependencies |
| A07 Auth Failures | Both prefixes use same auth dependency |
| A08 Data Integrity | N/A |
| A09 Logging | No change to logging |
| A10 SSRF | N/A |

## No critical findings.
