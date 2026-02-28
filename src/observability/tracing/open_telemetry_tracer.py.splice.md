# Splice: src/observability/tracing/open_telemetry_tracer.py

This module contains several logical groups and classes:

- `SpanAttributes` (class of constants): attribute name constants for GenAI operations.
- Tracer management: `is_otel_available`, `init_tracer`, `get_span_exporter`, `get_tracer`.
- Context/propagation helpers: `extract_trace_context`, `inject_trace_context`, `create_span`, `traced`.
- Internal helpers and small context managers around spans.

Suggested splices:
- `attributes.py`: keep `SpanAttributes` and related constants.
- `tracer.py`: tracer initialization and exporter selection.
- `propagation.py`: extract/inject helpers and header utilities.
- `decorators.py`: `traced` and other decorator/context manager helpers.
