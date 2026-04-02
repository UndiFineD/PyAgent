# structured-logging — Code Notes
_Owner: @6code | Status: DONE_

## Files Created / Modified

### NEW: `backend/logging_config.py`

```python
setup_logging(level="INFO") -> logging.Logger
get_logger(name="pyagent.backend") -> logging.Logger
```

Key decisions:
- Idempotent: skips configuration if handlers already attached (safe for hot-reload)
- Logger name `pyagent.backend` namespaces all backend logs
- `JsonFormatter` format string includes all six required fields

### MODIFIED: `backend/app.py`

Changes (minimal, scoped):
- `from .logging_config import setup_logging, get_logger` added to imports
- `_logger = setup_logging()` call after `app = FastAPI(...)` block
- `CorrelationIdMiddleware` class defined and registered with `app.add_middleware()`
- `GET /health` now calls `get_logger().info(...)` with structured extra fields
- Existing `import logging` / `logger = logging.getLogger(__name__)` kept for other endpoints

### MODIFIED: `backend/requirements.txt`

```
python-json-logger>=2.0.0
```
Added at end of file.

## Implementation Notes

- `CorrelationIdMiddleware` extends `starlette.middleware.base.BaseHTTPMiddleware`
  which is already a FastAPI/Starlette transitive dependency — no new package needed
- `uuid` is in the Python standard library — no new import needed in app.py
  (imported as `_uuid_mod` to avoid shadowing any future local variable)
- The `/health` endpoint log uses `extra={"correlation_id": "health", "endpoint": "/health"}`
  — a static value for the health check is acceptable since it's a synthetic trace point
- All `extra` keys must match the `JsonFormatter` format string fields exactly to appear in JSON output
