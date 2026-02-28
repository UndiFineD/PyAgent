# Auto-synced test for observability/tracing/open_telemetry_tracer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "open_telemetry_tracer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SpanAttributes"), "SpanAttributes missing"
    assert hasattr(mod, "is_otel_available"), "is_otel_available missing"
    assert hasattr(mod, "init_tracer"), "init_tracer missing"
    assert hasattr(mod, "get_span_exporter"), "get_span_exporter missing"
    assert hasattr(mod, "get_tracer"), "get_tracer missing"
    assert hasattr(mod, "extract_trace_context"), "extract_trace_context missing"
    assert hasattr(mod, "inject_trace_context"), "inject_trace_context missing"
    assert hasattr(mod, "extract_trace_headers"), "extract_trace_headers missing"
    assert hasattr(mod, "contains_trace_headers"), "contains_trace_headers missing"
    assert hasattr(mod, "create_span"), "create_span missing"
    assert hasattr(mod, "traced"), "traced missing"
    assert hasattr(mod, "get_current_span_safe"), "get_current_span_safe missing"
    assert hasattr(mod, "add_span_attributes"), "add_span_attributes missing"
    assert hasattr(mod, "add_span_event"), "add_span_event missing"
    assert hasattr(mod, "record_exception"), "record_exception missing"
    assert hasattr(mod, "log_tracing_disabled_warning"), "log_tracing_disabled_warning missing"
    assert hasattr(mod, "SpanTiming"), "SpanTiming missing"
    assert hasattr(mod, "timed_span"), "timed_span missing"
    assert hasattr(mod, "NullSpan"), "NullSpan missing"
    assert hasattr(mod, "NullTracer"), "NullTracer missing"
    assert hasattr(mod, "get_null_tracer"), "get_null_tracer missing"

