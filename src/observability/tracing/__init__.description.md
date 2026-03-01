# Description: src/observability/tracing/__init__.py

Module purpose:
- Provides a lazy-loading entry point for the `observability.tracing` subpackage.
- Exposes a registry of names that are loaded on-demand from `open_telemetry_tracer` through `ModuleLazyLoader`.

Behavioral notes:
- Uses `ModuleLazyLoader` to avoid importing heavy OpenTelemetry packages at import time.
- Defines `__getattr__` to forward attribute access to the lazy loader.

Public symbols (lazy):
- `NullSpan`, `NullTracer`, `SpanAttributes`, `SpanTiming`, `TRACE_HEADERS`, and many helper functions like `create_span`, `traced`, `init_tracer`, etc. (all lazily loaded)
