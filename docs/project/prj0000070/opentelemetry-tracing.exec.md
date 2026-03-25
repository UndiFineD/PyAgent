# opentelemetry-tracing — Exec Notes

## Validation Commands

### Install dependencies
```
pip install opentelemetry-api>=1.20 opentelemetry-sdk>=1.20
```

### Run tests
```
pytest tests/test_tracing.py -v
```

### Verify import works
```
python -c "from backend.tracing import tracer, _TRACER_NAME; print(_TRACER_NAME)"
```

## Expected Test Output
```
tests/test_tracing.py::test_setup_tracing_returns_tracer PASSED
tests/test_tracing.py::test_span_name_recorded PASSED
tests/test_tracing.py::test_tracer_instrumentation_scope PASSED
tests/test_tracing.py::test_tracing_module_singleton_exists PASSED
tests/test_tracing.py::test_tracer_name_constant PASSED
5 passed
```
