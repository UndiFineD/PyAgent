from __future__ import annotations
from typing import Any
import time

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]


class TracingCore:
    """
    TracingCore handles the logic for distributed tracing and latency breakdown.
    It prepares trace data for OpenTelemetry (OTel) exporters.
    """

    def create_span_context(self, trace_id: str, span_id: str) -> dict[str, str]:
        """Creates a standardized context for distributed tracing."""
        if rc:
            try:
                return rc.create_span_context(trace_id, span_id)  # type: ignore[attr-defined]
            except Exception:
                pass
        return {"trace_id": trace_id, "span_id": span_id, "version": "OTel-1.1"}

    def calculate_latency_breakdown(
        self, total_time: float, network_time: float
    ) -> dict[str, float]:
        """
        Calculates agent thinking time vs network latency.
        """
        if rc:
            try:
                return rc.calculate_latency_breakdown(total_time, network_time)  # type: ignore[attr-defined]
            except Exception:
                pass
        thinking_time = total_time - network_time
        return {
            "total_latency_ms": total_time * 1000,
            "network_latency_ms": network_time * 1000,
            "agent_thinking_ms": thinking_time * 1000,
            "think_ratio": thinking_time / total_time if total_time > 0 else 0,
        }

    def format_otel_log(self, name: str, attributes: dict[str, Any]) -> dict[str, Any]:
        """Formats a single telemetry event for OTel ingestion."""
        return {
            "timestamp": time.time_ns(),
            "name": name,
            "attributes": attributes,
            "kind": "INTERNAL",
        }
