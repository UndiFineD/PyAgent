#!/usr/bin/env python3

"""Engine for tracking agent performance, latency, and resource metrics."""

import json
import time
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from src.classes.fleet.ResilientStubs import resilient_import
from src.classes.stats.ObservabilityCore import ObservabilityCore, AgentMetric

# Resiliently load dependencies
TokenCostEngine = resilient_import("src.classes.stats.TokenCostEngine", "TokenCostEngine")
PrometheusExporter = resilient_import("src.classes.stats.PrometheusExporter", "PrometheusExporter")
OTelManager = resilient_import("src.classes.stats.OTelManager", "OTelManager")
MetricsExporter = resilient_import("src.classes.stats.MetricsExporter", "MetricsExporter")

class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.telemetry_file = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.metrics: List[AgentMetric] = []
        self._start_times: Dict[str, float] = {}
        self._otel_spans: Dict[str, str] = {} # Map trace_id -> tel_span_id
        self.cost_engine = TokenCostEngine()
        self.prometheus = PrometheusExporter()
        self.otel = OTelManager()
        self.metrics_exporter = MetricsExporter()
        self.log_buffer: List[Dict[str, Any]] = []
        self.load()

    def log_event(self, agent_id: str, event_type: str, data: Any, level: str = "INFO") -> None:
        """Logs a system event in a structured format for ELK.
        
        Args:
            agent_id: The ID of the agent generating the event.
            event_type: The category of event (e.g., 'task_complete', 'error').
            data: Payload of the event.
            level: Severity level (INFO, WARNING, ERROR, CRITICAL).
        """
        # Noise Reduction: Only store significant events in the persistent log buffer.
        # Metrics are still recorded for everything.
        important_types = ["agent_failure", "security_alert", "workflow_error", "system_crash"]
        important_levels = ["ERROR", "WARNING", "CRITICAL"]
        
        should_log = level in important_levels or event_type in important_types

        if should_log:
            event = {
                "timestamp": time.time(),
                "agent_id": agent_id,
                "event_type": event_type,
                "level": level,
                "data": data
            }
            self.log_buffer.append(event)
            
        # Always record metrics regardless of log storage
        self.prometheus.record_metric("agent_events_total", 1.0, {"agent": agent_id, "type": event_type})
        self.metrics_exporter.record_agent_call(agent_id, 0.0, True)

    def export_to_elk(self) -> str:
        """Simulates exporting log buffer to ELK stack."""
        count = len(self.log_buffer)
        # In real scenario: push to Elasticsearch/Logstash
        log_batch = json.dumps(self.log_buffer)
        self.log_buffer = [] 
        self.metrics_exporter.export_to_grafana()
        return f"Exported {count} events to ELK/Logstash."

    def get_metrics(self) -> str:
        """Returns Prometheus scrape response."""
        return self.metrics_exporter.get_prometheus_payload()

    def start_trace(self, trace_id: str) -> None:
        """Start timing an operation."""
        self._start_times[trace_id] = time.time()
        # Also start OTel span and store its UUID
        span_id = self.otel.start_span(trace_id)
        self._otel_spans[trace_id] = span_id

    def end_trace(self, trace_id: str, agent_name: str, operation: str, status: str = "success", 
                  input_tokens: int = 0, output_tokens: int = 0, model: str = "unknown",
                  metadata: Optional[Dict[str, Any]] = None) -> None:
        """End timing and record metric with cost estimation."""
        if trace_id not in self._start_times:
            logging.warning(f"No start trace found for {trace_id}")
            return
            
        duration = (time.time() - self._start_times.pop(trace_id)) * 1000
        
        # End OTel span using the stored span_id
        otel_span_id = self._otel_spans.pop(trace_id, None)
        if ot_span_id:
            self.otel.end_span(otel_span_id, status=status, attributes=metadata)
        
        # Calculate cost
        cost = TokenCostEngine.calculate_cost(model, input_tokens, output_tokens)
        
        metric = AgentMetric(
            agent_name=agent_name,
            operation=operation,
            duration_ms=round(duration, 2),
            status=status,
            token_count=input_tokens + output_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=cost,
            model=model,
            metadata=metadata or {}
        )
        self.metrics.append(metric)
        self.core.process_metric(metric)
        self.metrics_exporter.record_agent_call(agent_name, duration, status == "success")
        self.prometheus.record_metric("agent_latency_ms", metric.duration_ms, {"agent": agent_name})
        self.prometheus.record_metric("agent_cost_usd", metric.estimated_cost, {"agent": agent_name})
        self.save()

    def trace_workflow(self, workflow_name: str, duration: float) -> None:
        """Records a workflow trace for OpenTelemetry visualization."""
        self.prometheus.record_metric(
            "workflow_duration_seconds",
            duration,
            {"workflow": workflow_name}
        )
        self.log_event("system", "workflow_trace", {"workflow": workflow_name, "duration": duration})

    def get_summary(self) -> Dict[str, Any]:
        """Returns a summary of performance and cost metrics."""
        if not self.metrics:
            return {"status": "No data"}
            
        summary = {
            "total_calls": len(self.metrics),
            "avg_latency_ms": round(sum(m.duration_ms for m in self.metrics) / len(self.metrics), 2),
            "success_rate": round(len([m for m in self.metrics if m.status == "success"]) / len(self.metrics) * 100, 2),
            "total_tokens": sum(m.token_count for m in self.metrics),
            "total_cost_usd": round(sum(m.estimated_cost for m in self.metrics), 6),
            "agents": {}
        }
        
        for m in self.metrics:
            if m.agent_name not in summary["agents"]:
                summary["agents"][m.agent_name] = {"calls": 0, "latency": [], "cost": 0.0}
            summary["agents"][m.agent_name]["calls"] += 1
            summary["agents"][m.agent_name]["latency"].append(m.duration_ms)
            summary["agents"][m.agent_name]["cost"] += m.estimated_cost
            
        for agent in summary["agents"]:
            lats = summary["agents"][agent]["latency"]
            summary["agents"][agent]["avg_latency"] = round(sum(lats) / len(lats), 2)
            summary["agents"][agent]["total_cost"] = round(summary["agents"][agent]["cost"], 6)
            del summary["agents"][agent]["latency"]
            del summary["agents"][agent]["cost"]
            
        return summary

    def save(self) -> None:
        """Persist telemetry to disk."""
        try:
            data = [asdict(m) for m in self.metrics]
            self.telemetry_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logging.error(f"Failed to save telemetry: {e}")

    def load(self) -> None:
        """Load telemetry from disk."""
        if self.telemetry_file.exists():
            try:
                data = json.loads(self.telemetry_file.read_text())
                self.metrics = [AgentMetric(**m) for m in data]
            except Exception as e:
                logging.error(f"Failed to load telemetry: {e}")
                self.metrics = []
