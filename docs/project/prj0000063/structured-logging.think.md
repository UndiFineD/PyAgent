# structured-logging — Think / Analysis
_Owner: @2think | Status: DONE_

## Existing Logging Analysis

The FastAPI backend (`backend/app.py`) currently relies on:
1. `logging.getLogger(__name__)` — standard Python logging, unformatted
2. No structured fields — no correlation ID, no endpoint, no request context
3. No middleware for propagating request identifiers

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| Print statements | Zero setup | Unstructured, no levels, hard to parse |
| Standard logging | Built-in, flexible | Plain text, hard to aggregate at scale |
| python-json-logger | JSON output, custom fields, stdlib-compatible | Extra dep |
| structlog | Powerful, context-aware | Heavier dependency, different API |
| OpenTelemetry Logs | Full observability integration | Overkill for this scope, see prj0000070 |

## Decision: python-json-logger

- `python-json-logger` is a minimal, well-maintained adapter over Python's standard `logging`
- Produces machine-readable JSON lines compatible with log aggregators (ELK, Loki, Datadog)
- `LogRecord` extra fields map directly to JSON keys — simple to inject `correlation_id`
- Middleware approach cleanly separates concern: header extraction vs logging logic
- Zero API changes to existing log call sites (just adds new structured fields)

## Correlation ID Strategy

- **Source of truth:** `X-Correlation-ID` request header (caller-supplied)
- **Fallback:** `uuid.uuid4()` — auto-generated per request
- **Echo:** Middleware always sets `X-Correlation-ID` on response, so callers can trace
- **Propagation:** Currently per-endpoint call-site; future improvement is to use
  `contextvars.ContextVar` for automatic propagation across all calls in a request

## Security Considerations

- Correlation IDs from headers are not sanitised for log injection (mitigated by JSON
  encoding — the value is always a JSON string, never interpreted as control characters)
- Never log authentication tokens, secrets, or PII in structured logs
