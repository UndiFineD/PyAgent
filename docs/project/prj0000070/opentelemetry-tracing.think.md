# opentelemetry-tracing — Think

## Problem
PyAgent's FastAPI backend has no tracing. When agents run, there's no way to see which endpoint was called, how long it took, or what sub-steps were involved — especially important for diagnosing slow responses in the multi-agent swarm.

## Options

### Option A: opentelemetry-sdk + ConsoleSpanExporter (chosen)
- Add `opentelemetry-api` and `opentelemetry-sdk` to requirements
- Create `backend/tracing.py` to initialize a `TracerProvider` with `ConsoleSpanExporter`
- Allows future swap to OTLP without code changes
- **Pro:** Simple, no HTTP outbound, testable with InMemorySpanExporter
- **Con:** Console output is noisy; can be suppressed in production

### Option B: opentelemetry-instrumentation-fastapi (rejected)
- Auto-instruments all FastAPI routes by patching Starlette
- **Pro:** Zero-code instrumentation
- **Con:** Requires `OpenTelemetryMiddleware` lifecycle hooks, conflicts with existing middleware pattern, all tests would need ASGI instrumentation setup

### Option C: Custom span decorator only (rejected)
- Wrap specific functions with `@tracer.start_as_current_span(...)`
- **Con:** Non-standard; doesn't integrate with OTel ecosystem

## Decision
Option A — minimal `backend/tracing.py` exposing `setup_tracing(exporter=None)` and a module-level `tracer` singleton. Tests use `InMemorySpanExporter` with `SimpleSpanProcessor` to avoid BatchProcessor async flush timing issues.
