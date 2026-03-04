#!/usr/bin/env python3
from __future__ import annotations
"""
OpenTelemetry Tracing Module - Phase 20: Production Infrastructure
===================================================================

Distributed tracing with OpenTelemetry integration.
Inspired by vLLM's tracing.py pattern.

Features:
- SpanAttributes: Standard attribute names for LLM operations
- Trace context extraction and propagation
- OTLP exporter support (gRPC and HTTP)
- Graceful fallback when OpenTelemetry is not installed
- Span context managers and decorators
- Custom span processors

Author: PyAgent Phase 20
"""


import functools
import logging
import os
import time
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    ParamSpec,
    TypeVar,
)

logger = logging.getLogger(__name__)

# Standard trace headers
TRACE_HEADERS = ["traceparent", "tracestate"]

# Track if OpenTelemetry is available
OTEL_IMPORT_ERROR_TRACEBACK: str | None = None

if TYPE_CHECKING:
    from opentelemetry.context.context import Context
    from opentelemetry.trace import SpanKind, Tracer, Span, get_current_span

# Type stubs for when otel is not available (runtime)
if not TYPE_CHECKING:
    Context = Any
    Tracer = Any
    Span = Any
    SpanKind = Any
    get_current_span = None

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        SimpleSpanProcessor,
        SpanExporter,
    )
    from opentelemetry.trace import (
        SpanKind,
        Status,
        StatusCode,
        get_current_span,
        get_tracer_provider,
        set_tracer_provider,
    )
    if not TYPE_CHECKING:
        from opentelemetry.context.context import Context
        from opentelemetry.trace import Tracer, Span

    _IS_OTEL_IMPORTED = True
except ImportError:
    import traceback
    OTEL_IMPORT_ERROR_TRACEBACK = traceback.format_exc()
    Status = None
    StatusCode = None
    TracerProvider = None  # type: ignore[assignment]
    BatchSpanProcessor = None  # type: ignore[assignment]
    SimpleSpanProcessor = None  # type: ignore[assignment]
    SpanExporter = None  # type: ignore[assignment]
    set_tracer_provider = None  # type: ignore[assignment]
    get_tracer_provider = None  # type: ignore[assignment]
    get_current_span = None  # type: ignore[assignment]
    _IS_OTEL_IMPORTED = False


P = ParamSpec("P")
T = TypeVar("T")


# ============================================================================
# Span Attributes (Standard names for LLM operations)
# ============================================================================


class SpanAttributes:
    """
    Standard span attribute names for LLM and AI operations.
    
    Based on OpenTelemetry semantic conventions for GenAI.
    """

    # Usage metrics
    GEN_AI_USAGE_COMPLETION_TOKENS = "gen_ai.usage.completion_tokens"
    GEN_AI_USAGE_PROMPT_TOKENS = "gen_ai.usage.prompt_tokens"
    GEN_AI_USAGE_TOTAL_TOKENS = "gen_ai.usage.total_tokens"
    GEN_AI_USAGE_NUM_SEQUENCES = "gen_ai.usage.num_sequences"

    # Request parameters
    GEN_AI_REQUEST_MAX_TOKENS = "gen_ai.request.max_tokens"
    GEN_AI_REQUEST_TOP_P = "gen_ai.request.top_p"
    GEN_AI_REQUEST_TEMPERATURE = "gen_ai.request.temperature"
    GEN_AI_REQUEST_ID = "gen_ai.request.id"
    GEN_AI_REQUEST_N = "gen_ai.request.n"
    GEN_AI_REQUEST_MODEL = "gen_ai.request.model"
    GEN_AI_REQUEST_STREAM = "gen_ai.request.stream"

    # Response info
    GEN_AI_RESPONSE_MODEL = "gen_ai.response.model"
    GEN_AI_RESPONSE_FINISH_REASON = "gen_ai.response.finish_reason"
    GEN_AI_RESPONSE_ID = "gen_ai.response.id"

    # Latency metrics
    GEN_AI_LATENCY_TIME_IN_QUEUE = "gen_ai.latency.time_in_queue"
    GEN_AI_LATENCY_TIME_TO_FIRST_TOKEN = "gen_ai.latency.time_to_first_token"
    GEN_AI_LATENCY_E2E = "gen_ai.latency.e2e"
    GEN_AI_LATENCY_TIME_IN_SCHEDULER = "gen_ai.latency.time_in_scheduler"
    GEN_AI_LATENCY_TIME_IN_MODEL_FORWARD = "gen_ai.latency.time_in_model_forward"
    GEN_AI_LATENCY_TIME_IN_MODEL_EXECUTE = "gen_ai.latency.time_in_model_execute"
    GEN_AI_LATENCY_TIME_IN_MODEL_PREFILL = "gen_ai.latency.time_in_model_prefill"
    GEN_AI_LATENCY_TIME_IN_MODEL_DECODE = "gen_ai.latency.time_in_model_decode"

    # Agent/orchestration
    AGENT_NAME = "agent.name"
    AGENT_TYPE = "agent.type"
    AGENT_VERSION = "agent.version"
    ORCHESTRATOR_NAME = "orchestrator.name"
    TASK_TYPE = "task.type"
    TASK_ID = "task.id"

    # Error tracking
    ERROR_TYPE = "error.type"
    ERROR_MESSAGE = "error.message"


# ============================================================================
# Core Functions
# ============================================================================


def is_otel_available() -> bool:
    """Check if OpenTelemetry is available."""
    return _IS_OTEL_IMPORTED


def init_tracer(
    instrumenting_module_name: str,
    otlp_traces_endpoint: str | None = None,
    *,
    use_batch_processor: bool = True,
) -> Tracer | None:
    """
    Initialize an OpenTelemetry tracer.
    
    Args:
        instrumenting_module_name: Name of the module being instrumented.
        otlp_traces_endpoint: OTLP endpoint URL for trace export.
        use_batch_processor: If True, use batch span processor (recommended).

    Returns:
        Tracer instance or None if OpenTelemetry is not available.

    Raises:
        ValueError: If OpenTelemetry is not available.
    """
    if not is_otel_available():
        raise ValueError(
            "OpenTelemetry is not available. Unable to initialize a tracer. "
            "Ensure OpenTelemetry packages are installed. "
            f"Original error:\n{OTEL_IMPORT_ERROR_TRACEBACK}"
        )

    trace_provider = TracerProvider()

    if otlp_traces_endpoint:
        span_exporter = get_span_exporter(otlp_traces_endpoint)
        if use_batch_processor:
            trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        else:
            trace_provider.add_span_processor(SimpleSpanProcessor(span_exporter))

    set_tracer_provider(trace_provider)
    return trace_provider.get_tracer(instrumenting_module_name)


def get_span_exporter(endpoint: str) -> SpanExporter:
    """
    Get a span exporter based on the configured protocol.
    
    Supports both gRPC and HTTP protocols.
    """
    if not is_otel_available():
        raise RuntimeError("OpenTelemetry is not available")

    protocol = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_PROTOCOL", "grpc")

    if protocol == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
    elif protocol == "http/protobuf":
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
    else:
        raise ValueError(f"Unsupported OTLP protocol '{protocol}' is configured")

    return OTLPSpanExporter(endpoint=endpoint)


def get_tracer(name: str = __name__) -> Tracer | None:
    """
    Get a tracer from the current provider.

    Returns None if OpenTelemetry is not available.
    """
    if not is_otel_available():
        return None
    return get_tracer_provider().get_tracer(name)


# ============================================================================
# Trace Context Propagation
# ============================================================================
def extract_trace_context(headers: Mapping[str, str] | None) -> Context | None:
    """
    Extract trace context from HTTP headers.

    Args:
        headers: HTTP headers containing trace context.

    Returns:
        OpenTelemetry context or None.
    """
    if not is_otel_available():
        return None

    from opentelemetry.propagators.textmap import TraceContextTextMapPropagator

    headers = headers or {}
    return TraceContextTextMapPropagator().extract(headers)


def inject_trace_context(headers: dict[str, str]) -> dict[str, str]:
    """
    Inject current trace context into headers.

    Args:
        headers: Dictionary to inject trace context into.

    Returns:
        Headers with trace context added.
    """
    if not is_otel_available():
        return headers

    from opentelemetry.propagators.textmap import TraceContextTextMapPropagator

    TraceContextTextMapPropagator().inject(headers)
    return headers


def extract_trace_headers(headers: Mapping[str, str]) -> dict[str, str]:
    """
    Extract only trace-related headers from a headers mapping.
    """
    return {h: headers[h] for h in TRACE_HEADERS if h in headers}


def contains_trace_headers(headers: Mapping[str, str]) -> bool:
    """Check if headers contain trace context."""
    return any(h in headers for h in TRACE_HEADERS)


# ============================================================================
# Span Context Managers
# ============================================================================
@contextmanager
def create_span(
    name: str,
    tracer: Tracer | None = None,
    *,
    kind: SpanKind | None = None,
    attributes: dict[str, Any] | None = None,
    context: Context | None = None,
    should_record_exception: bool = True,
    set_status_on_exception: bool = True,
) -> Generator[Span | None, None, None]:
    """
    Context manager for creating a span.

    Args:
        name: Span name.
        tracer: Tracer to use (uses global if not provided).
        kind: Span kind (CLIENT, SERVER, PRODUCER, CONSUMER, INTERNAL).
        attributes: Initial span attributes.
        context: Parent context.
        should_record_exception: If True, record exceptions on the span.
        set_status_on_exception: If True, set error status on exception.

    Yields:
        Span instance or None if tracing is not available.

    Example:
        >>> with create_span("process_request", attributes={"user_id": 123}) as span:
        ...     if span:
        ...         span.set_attribute("status", "processing")
        ...     result = do_work()
    """
    if not is_otel_available():
        yield None
        return

    if tracer is None:
        tracer = get_tracer()

    if tracer is None:
        yield None
        return

    # Default to INTERNAL kind
    if kind is None:
        kind = SpanKind.INTERNAL

    with tracer.start_as_current_span(
        name,
        kind=kind,
        attributes=attributes,
        context=context,
        record_exception=should_record_exception,
        set_status_on_exception=set_status_on_exception,
    ) as span:
        yield span


def traced(
    name: str | None = None,
    *,
    tracer: Tracer | None = None,
    kind: SpanKind | None = None,
    attributes: dict[str, Any] | None = None,
    should_record_exception: bool = True,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to trace a function.

    Args:
        name: Span name (defaults to function name).
        tracer: Tracer to use.
        kind: Span kind.
        attributes: Static span attributes.
        should_record_exception: If True, record exceptions.

    Example:
        >>> @traced("process_data", attributes={"service": "processor"})
        ... def process_data(data: str) -> str:
        ...     return data.upper()
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        span_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            with create_span(
                span_name,
                tracer=tracer,
                kind=kind,
                attributes=attributes,
                should_record_exception=should_record_exception,
            ) as span:
                return func(*args, **kwargs)

        return wrapper

    return decorator


# ============================================================================
# Span Helpers
# ============================================================================
def get_current_span_safe() -> Span | None:
    """Get the current span, or None if not available."""
    if not is_otel_available():
        return None
    return get_current_span()


def add_span_attributes(attributes: dict[str, Any]) -> None:
    """
    Add attributes to the current span.
    
    Safe to call even if tracing is not available.
    """
    if not is_otel_available():
        return

    span = get_current_span_safe()
    if span and span.is_recording():
        for key, value in attributes.items():
            span.set_attribute(key, value)


def add_span_event(
    name: str,
    attributes: dict[str, Any] | None = None,
) -> None:
    """
    Add an event to the current span.

    Safe to call even if tracing is not available.
    """
    if not is_otel_available():
        return

    span = get_current_span_safe()
    if span and span.is_recording():
        span.add_event(name, attributes=attributes or {})


def record_exception(exception: Exception, escaped: bool = True) -> None:
    """
    Record an exception on the current span.

    Safe to call even if tracing is not available.
    """
    if not is_otel_available():
        return

    span = get_current_span_safe()
    if span and span.is_recording():
        span.record_exception(exception, escaped=escaped)
        if Status is not None and StatusCode is not None:
            span.set_status(Status(StatusCode.ERROR, str(exception)))


# ============================================================================
# Logging Integration
# ============================================================================
class _LoggingState:
    """Tracks logging state to avoid repeated warnings."""
    disabled_warning_logged = False


def log_tracing_disabled_warning() -> None:
    """Log a warning that tracing is disabled (only once)."""
    if not _LoggingState.disabled_warning_logged:
        logger.warning("Received a request with trace context but tracing is disabled")
        _LoggingState.disabled_warning_logged = True


# ============================================================================
# Timing Utilities
# ============================================================================
@dataclass
class SpanTiming:
    """Helper for tracking timing within a span."""

    start_time: float = field(default_factory=time.perf_counter)
    checkpoints: dict[str, float] = field(default_factory=dict)

    def checkpoint(self, name: str) -> float:
        """Record a timing checkpoint."""
        elapsed = time.perf_counter() - self.start_time
        self.checkpoints[name] = elapsed
        return elapsed

    def elapsed(self) -> float:
        """Get total elapsed time."""
        return time.perf_counter() - self.start_time

    def to_attributes(self, prefix: str = "") -> dict[str, float]:
        """Convert checkpoints to span attributes."""
        result = {f"{prefix}total": self.elapsed()}
        for name, elapsed in self.checkpoints.items():
            result[f"{prefix}{name}"] = elapsed
        return result

    def apply_to_span(self, span: Span | None, prefix: str = "timing.") -> None:
        """Apply timing attributes to a span."""
        if span is None:
            return
        for key, value in self.to_attributes(prefix).items():
            span.set_attribute(key, value)


@contextmanager
def timed_span(
    name: str,
    tracer: Tracer | None = None,
    **kwargs: Any
) -> Generator[tuple[Span | None, SpanTiming], None, None]:
    """
    Context manager for a span with timing.

    Yields:
        Tuple of (span, timing) where timing can be used to record checkpoints.
    """
    timing = SpanTiming()
    with create_span(name, tracer=tracer, **kwargs) as span:
        try:
            yield span, timing
        finally:
            if span and span.is_recording():
                timing.apply_to_span(span)


# ============================================================================
# Null Tracer (for testing)
# ============================================================================
class NullSpan:
    """A no-op span for testing or when tracing is disabled."""

    def set_attribute(self, key: str, value: Any) -> None:
        """No-op for setting an attribute."""
        pass

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        """No-op for adding an event."""
        pass

    def record_exception(self, exception: Exception, escaped: bool = True) -> None:
        """No-op for recording an exception."""
        pass

    def set_status(self, status: Any) -> None:
        """No-op for setting status."""
        pass

    def is_recording(self) -> bool:
        """Indicates if the span is recording (always False for NullSpan)."""
        return False

    def __enter__(self) -> "NullSpan":
        """No-op enter method."""
        return self

    def __exit__(self, *args: Any) -> None:
        """No-op exit method."""
        pass


class NullTracer:
    """A no-op tracer for testing or when tracing is disabled."""

    @contextmanager
    def start_as_current_span(
        self,
        name: str,
        **kwargs: Any
    ) -> Generator[NullSpan, None, None]:
        """Context manager that yields a NullSpan."""
        yield NullSpan()

    def start_span(self, name: str, **kwargs: Any) -> NullSpan:
        """Start a new NullSpan."""
        return NullSpan()


def get_null_tracer() -> NullTracer:
    """Get a null tracer for testing."""
    return NullTracer()


# ============================================================================
# Exports
# ============================================================================
__all__ = [
    # Constants
    "TRACE_HEADERS",
    "SpanAttributes",
    # Availability check
    "is_otel_available",
    "OTEL_IMPORT_ERROR_TRACEBACK",
    # Initialization
    "init_tracer",
    "get_span_exporter",
    "get_tracer",
    # Context propagation
    "extract_trace_context",
    "inject_trace_context",
    "extract_trace_headers",
    "contains_trace_headers",
    # Span creation
    "create_span",
    "traced",
    "timed_span",
    # Span helpers
    "get_current_span_safe",
    "add_span_attributes",
    "add_span_event",
    "record_exception",
    # Timing
    "SpanTiming",
    # Logging
    "log_tracing_disabled_warning",
    # Testing
    "NullSpan",
    "NullTracer",
    "get_null_tracer",
]
