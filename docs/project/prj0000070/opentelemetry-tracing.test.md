# opentelemetry-tracing — Test Plan

## Tests in `tests/test_tracing.py`

```python
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from backend.tracing import setup_tracing, _TRACER_NAME


def test_setup_tracing_returns_tracer():
    exporter = InMemorySpanExporter()
    t = setup_tracing(exporter)
    assert t is not None


def test_span_name_recorded():
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    t = provider.get_tracer(_TRACER_NAME)
    with t.start_as_current_span("my-span"):
        pass
    spans = exporter.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].name == "my-span"


def test_tracer_instrumentation_scope():
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    t = provider.get_tracer(_TRACER_NAME)
    with t.start_as_current_span("scope-check"):
        pass
    spans = exporter.get_finished_spans()
    assert spans[0].instrumentation_scope.name == _TRACER_NAME


def test_tracing_module_singleton_exists():
    from backend import tracing
    assert hasattr(tracing, "tracer")
    assert hasattr(tracing, "setup_tracing")
    assert hasattr(tracing, "_TRACER_NAME")


def test_tracer_name_constant():
    assert _TRACER_NAME == "pyagent.backend"
```

## Notes
- Use `SimpleSpanProcessor` (synchronous) not `BatchSpanProcessor` to avoid async flush timing
- Create isolated `TracerProvider` instances per test — avoid touching global state
- `test_setup_tracing_returns_tracer` can call `setup_tracing(exporter)` with an exporter to suppress BatchSpanProcessor global pollution
