# opentelemetry-tracing — Security Review

## OWASP Top 10 Scan

### Injection
- No user input is passed to span names or attributes in this implementation
- Span names are hardcoded strings only — no injection vector

### Cryptographic Failures
- N/A — no cryptographic operations

### Security Misconfiguration
- `ConsoleSpanExporter` outputs to stderr — may log sensitive data if custom spans include user data
- Mitigation: document that span attributes must not include PII; production config should use redacting exporter

### Vulnerable Components
- `opentelemetry-api>=1.20` and `opentelemetry-sdk>=1.20` are actively maintained
- Pin to specific minor version in production lockfile

### Server-Side Request Forgery (SSRF)
- `ConsoleSpanExporter` makes no outbound HTTP — no SSRF risk
- If OTLP exporter is added in future, the endpoint must be validated against an allowlist

## Verdict
PASS — no security issues in this minimal implementation.
