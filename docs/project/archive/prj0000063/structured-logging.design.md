# structured-logging — Design
_Owner: @3design | Status: DONE_

## Architecture

```
backend/
├── logging_config.py      ← NEW: JSON formatter, logger factory
└── app.py                 ← MODIFY: CorrelationIdMiddleware + health log

tests/
└── test_structured_logging.py  ← NEW: 5 tests
```

## Module: backend/logging_config.py

### `setup_logging(level: str = "INFO") -> logging.Logger`
- Creates the `pyagent.backend` logger (idempotent — skips if handlers already exist)
- Attaches a `StreamHandler` with `JsonFormatter`
- Format fields: `asctime`, `name`, `levelname`, `message`, `correlation_id`, `endpoint`
- Returns the configured logger

### `get_logger(name: str = "pyagent.backend") -> logging.Logger`
- Returns `logging.getLogger(name)` — alias for consistent usage

## Middleware: CorrelationIdMiddleware

- `BaseHTTPMiddleware` subclass on `app`
- Reads `X-Correlation-ID` header; falls back to `str(uuid.uuid4())`
- Passes request through, then writes `X-Correlation-ID` onto the response
- Registered **before** other app-level middleware to ensure all routes benefit

## app.py Changes

| Location | Change |
|---|---|
| Top-level imports | `from .logging_config import setup_logging, get_logger` |
| After `app = FastAPI(...)` | `_logger = setup_logging(); _logger.info("PyAgent backend starting")` |
| After CORS middleware | Add `CorrelationIdMiddleware` |
| `GET /health` | `get_logger().info("Health check", extra={"correlation_id": "health", "endpoint": "/health"})` |

## Data Flow

```
Request → CorrelationIdMiddleware
              ↓
         extract/generate correlation_id
              ↓
         call_next(request) → endpoint handler
              ↓  (get_logger().info(..., extra={"correlation_id": cid, "endpoint": path}))
         JSON log line written to stderr
              ↓
         set X-Correlation-ID on response
              ↓
Response to caller
```

## Dependencies

| Package | Version | Justification |
|---|---|---|
| `python-json-logger` | `>=2.0.0` | JsonFormatter for stdlib logging |
| `starlette` | transitive from FastAPI | BaseHTTPMiddleware |
