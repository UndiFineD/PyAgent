# opentelemetry-tracing — Design

## Interface

```python
# backend/tracing.py

_TRACER_NAME = "pyagent.backend"

def setup_tracing(exporter=None) -> trace.Tracer:
    """Configure a TracerProvider with the given exporter (default: ConsoleSpanExporter).
    Sets it as the global tracer provider and returns a named tracer."""

tracer: trace.Tracer = setup_tracing()
```

## Key Design Choices

- `exporter` parameter allows tests to inject `InMemorySpanExporter` + `SimpleSpanProcessor`
- Module-level `tracer` is a singleton for use throughout the backend  
- `BatchSpanProcessor` is used in production (default `None` path); `SimpleSpanProcessor` in tests
- `trace.set_tracer_provider(provider)` sets global state — tests that call `setup_tracing()` directly should pass their own exporter to avoid contaminating the global
- `backend/app.py` just imports `tracer` from the module — no additional startup call needed (import triggers `setup_tracing()`)

## Dependencies
- `opentelemetry-api>=1.20`
- `opentelemetry-sdk>=1.20`

No `opentelemetry-instrumentation-fastapi` — deferred to future work.

## Test Strategy
Use isolated `TracerProvider` instances per test rather than calling `setup_tracing()`, except for the module-attribute introspection tests.
