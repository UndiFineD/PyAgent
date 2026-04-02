# opentelemetry-tracing — Code Notes

## Files Changed

### `backend/tracing.py` (new)
- Minimal OTel setup module
- `setup_tracing(exporter=None)`: configures TracerProvider, sets as global, returns tracer
- Module-level `tracer` singleton initialized on import
- Uses `BatchSpanProcessor` + `ConsoleSpanExporter` by default (tests pass their own exporter)

### `backend/app.py` (modified)
- Added `from .tracing import tracer` import
- No additional changes needed — import triggers module-level `setup_tracing()` call

### `requirements.txt` (modified)
- Added `opentelemetry-api>=1.20`
- Added `opentelemetry-sdk>=1.20`

### `requirements-ci.txt` (modified)
- Same OTel additions for CI environment

## Code Health Notes
- Module uses `SimpleSpanProcessor` in test path, `BatchSpanProcessor` in production — this is by design
- The global `trace.set_tracer_provider()` is only set once on first import; subsequent imports reuse the module cache
- `ConsoleSpanExporter` output goes to stderr — not a problem for tests since tests use InMemorySpanExporter
