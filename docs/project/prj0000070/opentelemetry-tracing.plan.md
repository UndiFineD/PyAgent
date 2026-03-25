# opentelemetry-tracing — Plan

## Tasks

1. **Add dependencies**
   - `requirements.txt`: add `opentelemetry-api>=1.20` and `opentelemetry-sdk>=1.20`
   - `requirements-ci.txt`: same additions (for CI installs)

2. **Create `backend/tracing.py`**
   - Import `opentelemetry.trace`, `TracerProvider`, `BatchSpanProcessor`, `ConsoleSpanExporter`
   - Define `_TRACER_NAME = "pyagent.backend"`
   - Define `setup_tracing(exporter=None) -> trace.Tracer`
   - Create module-level `tracer = setup_tracing()`

3. **Update `backend/app.py`**
   - Add `from .tracing import tracer` (import triggers setup on startup)
   - No additional call needed

4. **Create `tests/test_tracing.py`** with 5 tests:
   - `test_setup_tracing_returns_tracer`
   - `test_span_name_recorded`
   - `test_tracer_instrumentation_scope`
   - `test_tracing_module_singleton_exists`
   - `test_tracer_name_constant`

## Validation
```
pytest tests/test_tracing.py -v
```
All 5 tests must pass.

## Commits
1. `@1project: prj0000070-opentelemetry-tracing — project artifacts`
2. `@6code: prj0000070 — add OTel tracing module + app integration`
3. `@5test: prj0000070 — tracing tests`
4. `@9git: prj0000070 — push and open PR`
