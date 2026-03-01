# Description: src/observability/tracing/open_telemetry_tracer.py

Module overview:
- Implements OpenTelemetry integration and fallback behavior when OTEL packages are not installed.
- Defines standardized `SpanAttributes` names for GenAI operations and various helpers to create, inject, extract, and manage spans.
- Provides context managers (`create_span`), decorators (`traced`), tracer initialization (`init_tracer`), and utilities for exporters.

Primary classes and APIs:
- `SpanAttributes` (class): constant names for span attributes.
- `is_otel_available()`, `init_tracer()`, `get_span_exporter()`, `create_span()`, `traced()` and propagation helpers.

Behavioral notes:
- Attempts to import OpenTelemetry at module import and records traceback if unavailable.
- Gracefully yields None spans or no-op behaviors when OTEL is not installed.
