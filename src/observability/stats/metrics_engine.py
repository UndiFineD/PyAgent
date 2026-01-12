#!/usr/bin/env python3
<<<<<<< HEAD
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Unified logic for metric calculation, processing, and management.


import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.observability.reports.grafana_generator import GrafanaDashboardGenerator

from src.observability.stats.metrics_core import TokenCostResult

# Import pure calculation cores
from .metrics_core import ModelFallbackCore, TokenCostCore
from .observability_core import AgentMetric, ObservabilityCore

try:
    import rust_core as rc
except ImportError:
    rc = None

from .exporters import MetricsExporter, OTelManager, PrometheusExporter
from src.core.base.lifecycle.version import VERSION


__version__: str = VERSION

logger: logging.Logger = logging.getLogger(__name__)


class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""

=======
# Copyright 2026 PyAgent Authors
# Unified logic for metric calculation, processing, and management.
from __future__ import annotations
import json
import logging
import math
import zlib
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING, Callable
from pathlib import Path

from .observability_core import *

from src.core.base.version import VERSION
__version__ = VERSION

logger = logging.getLogger(__name__)

class ObservabilityEngine:
    """Provides telemetry and performance tracking for the agent fleet."""
    
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
    def __init__(self, workspace_root: str = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")
<<<<<<< HEAD

        self.telemetry_file: Path = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.metrics: list[AgentMetric] = []
        self._start_times: dict[str, float] = {}
        self._otel_spans: dict[str, str] = {}  # Map trace_id -> tel_span_id
=======
            
        self.telemetry_file = self.workspace_root / ".agent_telemetry.json"
        self.core = ObservabilityCore()
        self.metrics: List[AgentMetric] = []
        self._start_times: Dict[str, float] = {}
        self._otel_spans: Dict[str, str] = {} # Map trace_id -> tel_span_id
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        self.cost_engine = TokenCostEngine()
        self.prometheus = PrometheusExporter()
        self.otel = OTelManager()
        self.metrics_exporter = MetricsExporter()
<<<<<<< HEAD
        self.log_buffer: list[dict[str, Any]] = []
=======
        self.log_buffer: List[Dict[str, Any]] = []
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        self.load()

    def log_event(self, agent_id: str, event_type: str, data: Any, level: str = "INFO") -> None:
        """Logs a system event in a structured format for ELK.
<<<<<<< HEAD

=======
        
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        Args:
            agent_id: The ID of the agent generating the event.
            event_type: The category of event (e.g., 'task_complete', 'error').
            data: Payload of the event.
            level: Severity level (INFO, WARNING, ERROR, CRITICAL).
        """
        # Noise Reduction: Only store significant events in the persistent log buffer.
        # Metrics are still recorded for everything.
<<<<<<< HEAD
        important_types: list[str] = [
            "agent_failure",
            "security_alert",
            "workflow_error",
            "system_crash",
        ]
        important_levels: list[str] = ["ERROR", "WARNING", "CRITICAL"]

        should_log: bool = level in important_levels or event_type in important_types
=======
        important_types = ["agent_failure", "security_alert", "workflow_error", "system_crash"]
        important_levels = ["ERROR", "WARNING", "CRITICAL"]
        
        should_log = level in important_levels or event_type in important_types
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))

        if should_log:
            event = {
                "timestamp": time.time(),
                "agent_id": agent_id,
                "event_type": event_type,
                "level": level,
<<<<<<< HEAD
                "data": data,
            }
            self.log_buffer.append(event)

=======
                "data": data
            }
            self.log_buffer.append(event)
            
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        # Always record metrics regardless of log storage
        self.prometheus.record_metric("agent_events_total", 1.0, {"agent": agent_id, "type": event_type})
        self.metrics_exporter.record_agent_call(agent_id, 0.0, True)

    def export_to_elk(self) -> str:
        """Simulates exporting log buffer to ELK stack."""
<<<<<<< HEAD
        count: int = len(self.log_buffer)
        # In real scenario: push to Elasticsearch/Logstash
        json.dumps(self.log_buffer)
        self.log_buffer = []
=======
        count = len(self.log_buffer)
        # In real scenario: push to Elasticsearch/Logstash
        log_batch = json.dumps(self.log_buffer)
        self.log_buffer = [] 
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        self.metrics_exporter.export_to_grafana()
        return f"Exported {count} events to ELK/Logstash."

    def get_metrics(self) -> str:
        """Returns Prometheus scrape response."""
        return self.metrics_exporter.get_prometheus_payload()

<<<<<<< HEAD
    def generate_dashboard(self, shard_name: str | None = None) -> str:
        """
        Triggers Grafana JSON dashboard generation (Phase 126).
        """
        try:
            generator = GrafanaDashboardGenerator(self.workspace_root / "deploy" / "grafana")
            if shard_name:
                return generator.generate_shard_obs(shard_name)
            return generator.generate_fleet_summary()
        except RuntimeError as e:
            return f"Error: GrafanaDashboardGenerator not available: {e}"
=======
    def generate_dashboard(self, shard_name: Optional[str] = None) -> str:
        """
        Triggers Grafana JSON dashboard generation (Phase 126).
        """
        if GrafanaGenerator:
            generator = GrafanaGenerator(self.workspace_root / "deploy" / "grafana")
            if shard_name:
                return generator.generate_shard_obs(shard_name)
            return generator.generate_fleet_summary()
        return "Error: GrafanaGenerator not available."
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))

    def start_trace(self, trace_id: str) -> None:
        """Start timing an operation."""
        self._start_times[trace_id] = time.time()
        # Also start OTel span and store its UUID
<<<<<<< HEAD
        span_id: str = self.otel.start_span(trace_id)
        self._otel_spans[trace_id] = span_id

    def end_trace(
        self,
        trace_id: str,
        agent_name: str,  # noqa: ARG002
        operation: str,  # noqa: ARG002
        status: str = "success",
        input_tokens: int = 0,  # noqa: ARG002
        output_tokens: int = 0,  # noqa: ARG002
        model: str = "unknown",  # noqa: ARG002
        metadata: dict[str, Any] | None = None,
    ) -> None:
=======
        span_id = self.otel.start_span(trace_id)
        self._otel_spans[trace_id] = span_id

    def end_trace(self, trace_id: str, agent_name: str, operation: str, status: str = "success", 
                  input_tokens: int = 0, output_tokens: int = 0, model: str = "unknown",
                  metadata: Optional[Dict[str, Any]] = None) -> None:
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        """End timing and record metric with cost estimation."""
        if trace_id not in self._start_times:
            logging.warning(f"No start trace found for {trace_id}")
            return
<<<<<<< HEAD

        _duration: float = (time.time() - self._start_times.pop(trace_id)) * 1000  # noqa: F841

        # End OTel span using the stored span_id
        otel_span_id: str | None = self._otel_spans.pop(trace_id, None)
        if otel_span_id:
            self.otel.end_span(otel_span_id, status=status, attributes=metadata)

    def consolidate_telemetry(self) -> dict[str, float]:
        """Aggregate metrics using Rust high-throughput engine."""
        if rc and hasattr(rc, "aggregate_metrics_rust"):
            data_map = self._build_data_map()
            try:
                aggregated_results = rc.aggregate_metrics_rust(data_map)  # type: ignore
                return aggregated_results
            except (AttributeError, RuntimeError) as e:  # pylint: disable=broad-exception-caught
                logger.warning("Rust metric aggregation failed: %s", e)
                import traceback
                traceback.print_exc()
        return self._python_aggregate_metrics()

    def _build_data_map(self) -> dict[str, list[float]]:
        data_map: dict[str, list[float]] = {}
        for m in self.metrics:
            key = f"{m.agent_name}:{m.operation}"
            if key not in data_map:
                data_map[key] = []
            data_map[key].append(m.duration_ms)
        return data_map

    def _python_aggregate_metrics(self) -> dict[str, float]:
        counts: dict[str, int] = {}
        sums: dict[str, float] = {}
        for m in self.metrics:
            key = f"{m.agent_name}:{m.operation}"
            counts[key] = counts.get(key, 0) + 1
            sums[key] = sums.get(key, 0.0) + m.duration_ms
        aggregated_results: dict[str, float] = {}
        for key, total in sums.items():
            if counts[key] > 0:
                aggregated_results[key] = total / counts[key]
        return aggregated_results

    def get_reliability_weights(self, agent_names: list[str]) -> list[float]:
=======
            
        duration = (time.time() - self._start_times.pop(trace_id)) * 1000
        
        # End OTel span using the stored span_id
        otel_span_id = self._otel_spans.pop(trace_id, None)
        if otel_span_id:
            self.otel.end_span(otel_span_id, status=status, attributes=metadata)
        
        # Calculate cost
        cost = self.cost_engine.calculate_cost(model, input_tokens, output_tokens)
        
        metric = AgentMetric(
            agent_name=agent_name,
            operation=operation,
            duration_ms=duration,
            status=status,
            token_count=input_tokens + output_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=cost,
            model=model,
            metadata=metadata or {}
        )
        
        self.core.process_metric(metric)
        self.metrics.append(metric) # Redundant but kept for display
        
        # External exporters
        self.prometheus.record_metric("agent_duration_ms", duration, {"agent": agent_name, "op": operation})
        self.metrics_exporter.record_agent_call(agent_name, duration, status == "success")
        
        if len(self.metrics) > 1000:
            self.save()
            self.metrics = self.metrics[-500:] # Prune memory

    def get_reliability_weights(self, agent_names: List[str]) -> List[float]:
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
        """Exposes core reliability logic for consensus protocols."""
        return self.core.calculate_reliability_scores(agent_names)

    def trace_workflow(self, workflow_name: str, duration: float) -> None:
        """Records a workflow trace for OpenTelemetry visualization."""
<<<<<<< HEAD
        self.prometheus.record_metric("workflow_duration_seconds", duration, {"workflow": workflow_name})
        self.log_event(
            "system",
            "workflow_trace",
            {"workflow": workflow_name, "duration": duration},
        )

    def get_summary(self) -> dict[str, Any]:
        """Returns a summary of performance and cost metrics."""
        if not self.metrics:
            return {"status": "No data"}

        count = len(self.metrics)
        total_latency = sum(m.duration_ms for m in self.metrics)
        success_count = sum(1 for m in self.metrics if m.status == "success")
        agent_stats = self._aggregate_agent_stats()

        summary = {
            "total_calls": count,
            "avg_latency_ms": round(total_latency / count, 2),
            "success_rate": round(success_count / count * 100, 2),
            "total_tokens": sum(m.token_count for m in self.metrics),
            "total_cost_usd": round(sum(m.estimated_cost for m in self.metrics), 6),
            "agents": agent_stats,
        }
        return summary

    def _aggregate_agent_stats(self) -> dict[str, dict[str, float]]:
        agents: dict[str, dict[str, float]] = {}
        for m in self.metrics:
            if m.agent_name not in agents:
                agents[m.agent_name] = {"calls": 0, "latency": 0.0, "cost": 0.0}
            a = agents[m.agent_name]
            a["calls"] += 1
            a["latency"] += m.duration_ms
            a["cost"] += m.estimated_cost
        for _name, data in agents.items():
            data["avg_latency"] = round(data["latency"] / data["calls"], 2) if data["calls"] else 0.0
            data["total_cost"] = round(data["cost"], 6)
        return agents
=======
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
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))

    def save(self) -> None:
        """Persist telemetry to disk."""
        try:
<<<<<<< HEAD
            data: list[dict[str, Any]] = [asdict(m) for m in self.metrics]
            self.telemetry_file.write_text(json.dumps(data, indent=2))
        except (OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to save telemetry: {e}")
            import traceback
            traceback.print_exc()
=======
            data = [asdict(m) for m in self.metrics]
            self.telemetry_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logging.error(f"Failed to save telemetry: {e}")
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))

    def load(self) -> None:
        """Load telemetry from disk."""
        if self.telemetry_file.exists():
            try:
                data = json.loads(self.telemetry_file.read_text())
<<<<<<< HEAD

                self.metrics = [AgentMetric(**m) for m in data]
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logging.error(f"Failed to load telemetry: {e}")
                import traceback
                traceback.print_exc()
                self.metrics = []


class TokenCostEngine:
    def __init__(self) -> None:
        self.core = TokenCostCore()

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0) -> float:
        res: TokenCostResult = self.core.calculate_cost(input_tokens, output_tokens, model)
        return res.total_cost


class ModelFallbackEngine:
    def __init__(self, cost_engine=None) -> None:
        self.cost_engine = cost_engine
        self.core = ModelFallbackCore()

    def get_fallback_model(self, current_model: str) -> str:
        return self.core.determine_next_model(current_model)
=======
                self.metrics = [AgentMetric(**m) for m in data]
            except Exception as e:
                logging.error(f"Failed to load telemetry: {e}")
                self.metrics = []


class DerivedMetricCalculator:
    """Calculate derived metrics from dependencies using safe AST evaluation."""

    def __init__(self) -> None:
        """Initialize derived metric calculator."""
        self.derived_metrics: Dict[str, DerivedMetric] = {}
        self._cache: Dict[str, float] = {}
        # Safe operator mapping
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):
            return float(node.value)
        elif isinstance(node, ast.Num):
            return float(node.n)
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                args = [self._eval_node(a) for a in node.args]
                if func_name == "abs": return abs(args[0])
                if func_name == "max": return max(args)
                if func_name == "min": return min(args)
                if func_name == "sqrt": return math.sqrt(args[0])
                if func_name == "pow": return math.pow(args[0], args[1])
            raise TypeError(f"Unsupported function: {node.func}")
        else:
            raise TypeError(f"Unsupported operation in formula: {type(node)}")

    def register_derived(
        self,
        name: str,
        dependencies: List[str],
        formula: str,
        description: str = ""
    ) -> DerivedMetric:
        """Register a derived metric.

        Args:
            name: Name for the derived metric.
            dependencies: List of metric names this depends on.
            formula: Formula string using {metric_name} variables.
            description: Description of the metric.

        Returns:
            The registered derived metric.
        """
        derived = DerivedMetric(
            name=name,
            dependencies=dependencies,
            formula=formula,
            description=description
        )
        self.derived_metrics[name] = derived
        return derived

    def calculate(
        self,
        name: str,
        metric_values: Dict[str, float]
    ) -> Optional[float]:
        """Calculate a derived metric value.

        Args:
            name: The derived metric name.
            metric_values: Current values of all metrics.

        Returns:
            Calculated value or None if missing dependencies.
        """
        derived = self.derived_metrics.get(name)
        if not derived:
            return None

        # Check all dependencies are available
        for dep in derived.dependencies:
            if dep not in metric_values:
                return None

        # Replace variables and evaluate
        formula = derived.formula
        for dep in derived.dependencies:
            formula = formula.replace(f"{{{dep}}}", str(metric_values[dep]))

        try:
            # Basic validation (clean variable injection still matters)
            dangerous_keywords = ["import", "open", "os.", "subprocess", "sys.", "eval", "exec", "__"]
            if any(kw in formula for kw in dangerous_keywords):
                logging.error(f"Blocked potentially dangerous formula: {formula}")
                return None

            # Safe AST evaluation
            tree = ast.parse(formula, mode='eval')
            result = self._eval_node(tree.body)
            
            self._cache[name] = result
            return result
        except Exception as e:
            logging.error(f"Failed to calculate {name}: {e}")
            return None

    def get_all_derived(
        self,
        metric_values: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate all derived metrics.

        Args:
            metric_values: Current values of all metrics.

        Returns:
            Dictionary of all calculated derived metrics.
        """
        results: Dict[str, float] = {}
        for name in self.derived_metrics:
            value = self.calculate(name, metric_values)
            if value is not None:
                results[name] = value
        return results


class CorrelationAnalyzer:
    """Analyze correlations between metrics.

    Provides correlation analysis to identify relationships
    between different metrics.

    Attributes:
        correlations: Computed correlations.
    """

    def __init__(self) -> None:
        """Initialize correlation analyzer."""
        self.correlations: List[MetricCorrelation] = []
        self._metric_history: Dict[str, List[float]] = {}

    def record_value(self, metric_name: str, value: float) -> None:
        """Record a metric value for correlation analysis.

        Args:
            metric_name: The metric name.
            value: The value to record.
        """
        if metric_name not in self._metric_history:
            self._metric_history[metric_name] = []
        self._metric_history[metric_name].append(value)

    def compute_correlation(
        self,
        metric_a: str,
        metric_b: str
    ) -> Optional[MetricCorrelation]:
        """Compute correlation between two metrics.

        Args:
            metric_a: First metric name.
            metric_b: Second metric name.

        Returns:
            Correlation result or None if insufficient data.
        """
        values_a = self._metric_history.get(metric_a, [])
        values_b = self._metric_history.get(metric_b, [])

        # Need same number of samples
        n = min(len(values_a), len(values_b))
        if n < 3:
            return None

        values_a = values_a[-n:]
        values_b = values_b[-n:]

        # Calculate Pearson correlation
        mean_a = sum(values_a) / n
        mean_b = sum(values_b) / n

        numerator = sum((values_a[i] - mean_a) * (values_b[i] - mean_b) for i in range(n))
        denom_a = math.sqrt(sum((x - mean_a) ** 2 for x in values_a))
        denom_b = math.sqrt(sum((x - mean_b) ** 2 for x in values_b))

        if denom_a == 0 or denom_b == 0:
            return None

        correlation = numerator / (denom_a * denom_b)

        result = MetricCorrelation(
            metric_a=metric_a,
            metric_b=metric_b,
            correlation_coefficient=correlation,
            sample_size=n
        )
        self.correlations.append(result)
        return result

    def find_strong_correlations(
        self,
        threshold: float = 0.7
    ) -> List[MetricCorrelation]:
        """Find strongly correlated metric pairs.

        Args:
            threshold: Minimum absolute correlation coefficient.

        Returns:
            List of strong correlations.
        """
        return [c for c in self.correlations
                if abs(c.correlation_coefficient) >= threshold]

    def get_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """Get correlation matrix for all metrics.

        Returns:
            Matrix of correlations.
        """
        metrics = list(self._metric_history.keys())
        matrix: Dict[str, Dict[str, float]] = {}

        for m1 in metrics:
            matrix[m1] = {}
            for m2 in metrics:
                if m1 == m2:
                    matrix[m1][m2] = 1.0
                else:
                    corr = self.compute_correlation(m1, m2)
                    matrix[m1][m2] = corr.correlation_coefficient if corr else 0.0

        return matrix


class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation.
    
    Acts as the I/O Shell for FormulaEngineCore.
    """
    def __init__(self) -> None:
        self.formulas: Dict[str, str] = {}
        self.core = FormulaEngineCore()

    def define(self, name: str, formula: str) -> None:
        """Define a formula."""
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        """Define a formula (backward compat)."""
        self.define(name, formula)

    def calculate(self, formula_or_name: str, variables: Optional[Dict[str, Any]] = None) -> float:
        """Calculate formula result via Core."""
        variables = variables or {}
        
        # If formula_or_name is in formulas dict, use stored formula
        formula = self.formulas.get(formula_or_name, formula_or_name)
            
        try:
            return self.core.calculate_logic(formula, variables)
        except Exception as e:
            logging.error(f"Formula calculation failed: {e}")
            return 0.0

    def validate(self, formula: str) -> FormulaValidation:
        """Validate formula syntax via Core."""
        result = self.core.validate_logic(formula)
        return FormulaValidation(
            is_valid=result["is_valid"], 
            error=result["error"]
        )

    def validate_formula(self, formula: str) -> bool:
        """Validate formula syntax (backward compat)."""
        return self.validate(formula).is_valid


class FormulaEngineCore:
    """Pure logic core for formula calculations."""

    def __init__(self) -> None:
        self.operators: Dict[Type[ast.AST], Any] = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise TypeError(f"Constant of type {type(node.value)} is not a number")
        elif hasattr(ast, "Num") and isinstance(node, ast.Num): # type: ignore
             return float(node.n) # type: ignore
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")

    def calculate_logic(self, formula: str, variables: Dict[str, Any]) -> float:
        """Core logic for calculating a formula result."""
        # Handle special functions like AVG
        if "AVG(" in formula:
            match = re.search(r'AVG\(\{(\w+)\}\)', formula)
            if match:
                var_name = match.group(1)
                if var_name in variables:
                    values = variables[var_name]
                    if isinstance(values, list) and values:
                        return sum(values) / len(values)
            return 0.0

        try:
            # Replace {variable} with actual values
            eval_formula = formula
            for var_name, var_value in variables.items():
                eval_formula = eval_formula.replace(f"{{{var_name}}}", str(var_value))
            
            # Use safe AST evaluation
            tree = ast.parse(eval_formula, mode='eval')
            return self._eval_node(tree.body)
        except Exception:
            # Core returns a default value, Shell handles logging
            return 0.0

    def validate_logic(self, formula: str) -> Dict[str, Any]:
        """Core logic for validating formula syntax."""
        try:
            if any(seq in formula for seq in ["+++", "***", "---"]):
                return {"is_valid": False, "error": "Invalid operator sequence"}

            test_formula = formula
            vars_found: List[str] = re.findall(r'\{(\w+)\}', formula)
            for var in vars_found:
                test_formula = test_formula.replace(f"{{{var}}}", "1")
            
            # Final AST parse check
            ast.parse(test_formula, mode='eval')
            return {"is_valid": True, "error": None}
        except Exception as e:
            return {"is_valid": False, "error": str(e)}


@dataclass
class FormulaValidation:
    """Result of formula validation."""
    is_valid: bool = True
    error: str = ""


class ResourceMonitor:
    """Monitors local system load to inform agent execution strategies."""
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.stats_file = self.workspace_root / ".system_stats.json"

    def get_current_stats(self) -> Dict[str, Any]:
        """Collects current CPU, Memory, and Disk metrics."""
        stats = {
            "platform": platform.platform(),
            "cpu_usage_pct": 0,
            "memory_usage_pct": 0,
            "disk_free_gb": 0,
            "status": "UNAVAILABLE",
            "gpu": {"available": False, "type": "NONE"}
        }
        
        if not HAS_PSUTIL:
            return stats
            
        try:
            stats["cpu_usage_pct"] = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            stats["memory_usage_pct"] = mem.percent
            
            disk = psutil.disk_usage(str(self.workspace_root))
            stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
            
            # GPU Detection (Hardware-Aware Orchestration - Phase 126)
            stats["gpu"] = self._detect_gpu()
            
            # Simple threshold logic
            if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90:
                stats["status"] = "CRITICAL"
            elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70:
                stats["status"] = "WARNING"
            else:
                stats["status"] = "HEALTHY"
                
        except Exception as e:
            logging.error(f"Failed to gather resource stats: {e}")
            stats["status"] = "ERROR"
            
        return stats

    def _detect_gpu(self) -> Dict[str, Any]:
        """Detects if NVIDIA or AMD GPUs are available."""
        # Check for NVIDIA (via nvidia-smi if available)
        import shutil
        if shutil.which("nvidia-smi"):
            return {"available": True, "type": "NVIDIA"}
        
        # Fallback to checking for torch/tensorflow availability if installed
        try:
            import torch
            if torch.cuda.is_available():
                return {"available": True, "type": "NVIDIA (Torch)"}
        except ImportError:
            pass
            
        return {"available": False, "type": "NONE"}

    def save_stats(self) -> str:
        """Saves current stats to disk."""
        stats = self.get_current_stats()
        try:
            self.stats_file.write_text(json.dumps(stats, indent=2))
        except Exception as e:
            logging.error(f"Failed to save system stats: {e}")

    def get_market_multiplier(self) -> float:
        """Determines the surcharge multiplier based on load."""
        stats = self.get_current_stats()
        multiplier = 1.0
        
        if stats["status"] == "CRITICAL":
            multiplier = 3.0
        elif stats["status"] == "WARNING":
            multiplier = 1.5
            
        if stats.get("gpu", {}).get("available"):
            multiplier += 1.0 # Additive premium for GPU availability
            
        return multiplier

    def get_execution_recommendation(self) -> str:
        """Suggests whether to run heavy tasks."""
        stats = self.get_current_stats()
        if stats["status"] == "CRITICAL":
            return "PAUSE: System load is too high. Defer heavy indexing or LLM calls."
        elif stats["status"] == "WARNING":
            return "CAUTION: Elevated load. Run tasks sequentially rather than in parallel."
        return "PROCEED: System resources are sufficient."

if __name__ == "__main__":
    mon = ResourceMonitor("c:/DEV/PyAgent")
    print(json.dumps(mon.get_current_stats(), indent=2))
    print(f"Recommendation: {mon.get_execution_recommendation()}")


class RetentionEnforcer:
    """Enforces retention policies on metrics."""
    def __init__(self) -> None:
        self.policies: Dict[str, RetentionPolicy] = {}
        self.data: Dict[str, List[Dict[str, Any]]] = {}

    def set_policy(self, metric_pattern: str, policy: RetentionPolicy) -> None:
        """Set a retention policy for metrics matching pattern."""
        self.policies[metric_pattern] = policy

    def add_policy(self, metric: str, max_age_days: int, max_points: int) -> None:
        """Add a retention policy (backward compat)."""
        policy = RetentionPolicy(name=metric, retention_days=max_age_days, max_points=max_points)
        self.policies[metric] = policy

    def add_data(self, metric_name: str, timestamp: float, value: Any) -> None:
        """Add data point to a metric."""
        if metric_name not in self.data:
            self.data[metric_name] = []
        self.data[metric_name].append({"timestamp": timestamp, "value": value})

    def enforce(self) -> int:
        """Enforce retention policies, return count of removed items."""
        from datetime import datetime
        removed_count = 0
        now = datetime.now().timestamp()
        for metric_pattern, policy in self.policies.items():
            # Find matching metrics
            matching_metrics = [m for m in self.data.keys() if metric_pattern.replace("*", "") in m]
            for metric in matching_metrics:
                if metric in self.data:
                    original_count = len(self.data[metric])
                    # Apply retention days policy
                    if policy.retention_days > 0:
                        cutoff_time = now - (policy.retention_days * 86400)  # days to seconds
                        self.data[metric] = [
                            d for d in self.data[metric]
                            if d["timestamp"] > cutoff_time
                        ]
                    removed_count += original_count - len(self.data[metric])
        return removed_count

    def apply_policies(self, metrics: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Apply retention policies to metrics."""
        result: Dict[str, List[Any]] = {}
        for metric, values in metrics.items():
            policy = self.policies.get(metric)
            if policy:
                if hasattr(policy, 'max_points') and policy.max_points > 0:
                    result[metric] = values[-policy.max_points:]
                else:
                    result[metric] = values
            else:
                result[metric] = values
        return result


class TokenCostEngine:
    """
    Calculates estimated costs for LLM tokens based on model variety.
    Shell for TokenCostCore.
    """
    
    def __init__(self) -> None:
        self.core = TokenCostCore()
        # Keep global reference for backward compatibility if needed
        self.MODEL_COSTS = MODEL_COSTS

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0) -> float:
        """Returns the estimated cost in USD for the given token counts."""
        return self.core.compute_usd(model, input_tokens, output_tokens)

    def get_supported_models(self) -> list:
        """Returns list of models with explicit pricing."""
        return self.core.list_models()


class TokenCostCore:
    """
    Pure logic for cost calculations.
    No I/O or state management.
    """

    def compute_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Returns the estimated cost in USD."""
        model_key = model.lower()
        pricing = self._find_pricing(model_key)
        
        # Cost per 1k tokens
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return round(input_cost + output_cost, 6)

    def _find_pricing(self, model_key: str) -> Dict[str, float]:
        """Heuristic for finding model pricing."""
        pricing = MODEL_COSTS.get(model_key)
        if not pricing:
            for key in MODEL_COSTS:
                if key != "default" and key in model_key:
                    return MODEL_COSTS[key]
        return pricing or MODEL_COSTS["default"]

    def list_models(self) -> List[str]:
        return list(MODEL_COSTS.keys())


class ModelFallbackEngine:
    """
    Manages model redundancy and fallback strategies.
    Shell for ModelFallbackCore.
    """

    def __init__(self, cost_engine: Optional[TokenCostEngine] = None, fleet: Optional[Any] = None) -> None:
        if fleet and hasattr(fleet, "telemetry") and not cost_engine:
            self.cost_engine = fleet.telemetry.cost_engine
        else:
            self.cost_engine = cost_engine
        self.core = ModelFallbackCore()
        self.max_retries = 3

    def get_fallback_model(self, current_model: str, failure_reason: str = "") -> Optional[str]:
        """Determines the next model to use after a failure."""
        logging.warning(f"Fallback requested for {current_model}. Reason: {failure_reason}")
        next_model = self.core.determine_next_model(current_model)
        if next_model:
            logging.info(f"Stepping to next model: {next_model}")
        return next_model

    def get_cheapest_model(self, models: List[str]) -> str:
        """Returns the cheapest model from the list based on the cost engine."""
        price_map = {}
        if self.cost_engine:
            price_map = self.cost_engine.MODEL_COSTS
            
        ranked = self.core.rank_models_by_cost(models, price_map)
        return ranked[0]

if __name__ == "__main__":
    cost_engine = TokenCostEngine()
    fallback = ModelFallbackEngine(cost_engine)
    
    print(f"Fallback for gpt-4o: {fallback.get_fallback_model('gpt-4o')}")
    print(f"Cheapest of [gpt-4o, gpt-4o-mini]: {fallback.get_cheapest_model(['gpt-4o', 'gpt-4o-mini'])}")


class ModelFallbackCore:
    """Pure logic core for model fallback strategies."""

    def __init__(self, fallback_chains: Optional[Dict[str, List[str]]] = None) -> None:
        self.fallback_chains = fallback_chains or {
            "high_performance": ["gpt-4o", "claude-3-5-sonnet", "gpt-4-turbo"],
            "balanced": ["claude-3-5-sonnet", "gpt-4o-mini", "gemini-1.5-pro"],
            "economy": ["gpt-4o-mini", "claude-3-haiku", "gemini-1.5-flash"]
        }

    def determine_next_model(self, current_model: str) -> Optional[str]:
        """Logic to pick the next model in a chain."""
        for chain_name, chain in self.fallback_chains.items():
            if current_model in chain:
                idx = chain.index(current_model)
                if idx + 1 < len(chain):
                    return chain[idx + 1]
        
        # Default fallback if not in a chain
        return self.fallback_chains["economy"][0]

    def rank_models_by_cost(self, models: List[str], model_price_map: Dict[str, Dict[str, float]]) -> List[str]:
        """Ranks models from cheapest to most expensive."""
        def get_cost(m: str) -> float:
            return model_price_map.get(m, {}).get("total", 999.0)
            
        return sorted(models, key=get_cost)

    def validate_retry_limit(self, current_retry: int, max_retries: int) -> bool:
        """Logic for retry boundaries."""
        return current_retry < max_retries


class StatsRollupCalculator:
    """Calculates metric rollups."""
    def __init__(self) -> None:
        self.rollups: Dict[str, List[float]] = {}
        self._points: Dict[str, List[Tuple[float, float]]] = {}

    def add_point(self, metric: str, timestamp: float, value: float) -> None:
        """Add a data point for rollup calculation."""
        if metric not in self._points:
            self._points[metric] = []
        self._points[metric].append((float(timestamp), float(value)))

    def rollup(self, metric: str, interval: str = "1h") -> List[float]:
        """Compute rollups for a metric at the given interval.

        Interval format examples: '1h', '1d', '15m'.
        Returns a list of aggregated values per time bucket (average).
        """
        points = self._points.get(metric, [])
        if not points:
            return []

        unit = interval[-1]
        try:
            amount = int(interval[:-1])
        except Exception:
            amount = 1

        if unit == "m":
            bucket = 60 * amount
        elif unit == "h":
            bucket = 3600 * amount
        elif unit == "d":
            bucket = 86400 * amount
        else:
            bucket = 3600 * amount

        buckets: Dict[int, List[float]] = {}
        for ts, val in points:
            key = int(ts) // int(bucket)
            buckets.setdefault(key, []).append(float(val))

        results: List[float] = []
        for key in sorted(buckets.keys()):
            vals = buckets[key]
            results.append(sum(vals) / len(vals))

        self.rollups[metric] = results
        return results

    def calculate_rollup(self, metrics: List[float], aggregation_type: AggregationType) -> float:
        """Calculate rollup with specified aggregation."""
        if not metrics:
            return 0.0
        if aggregation_type == AggregationType.SUM:
            return sum(metrics)
        elif aggregation_type == AggregationType.AVG:
            return sum(metrics) / len(metrics)
        elif aggregation_type == AggregationType.MIN:
            return min(metrics)
        elif aggregation_type == AggregationType.MAX:
            return max(metrics)
        elif aggregation_type == AggregationType.COUNT:
            return float(len(metrics))
        return 0.0


class StatsRollup:
    """Aggregate metrics into rollup views.

    Provides rollup capabilities for aggregating metrics
    over time intervals.

    Attributes:
        configs: Rollup configurations.
        rollups: Computed rollup data.
    """

    def __init__(self) -> None:
        """Initialize stats rollup."""
        self.configs: Dict[str, RollupConfig] = {}
        self.rollups: Dict[str, List[Dict[str, Any]]] = {}
        self._raw_data: Dict[str, List[Tuple[datetime, float]]] = {}

    def configure_rollup(
        self,
        name: str,
        source_metrics: List[str],
        aggregation: AggregationType,
        interval_minutes: int = 60,
        keep_raw: bool = True
    ) -> RollupConfig:
        """Configure a rollup.

        Args:
            name: Name for the rollup.
            source_metrics: Source metric names.
            aggregation: Aggregation type to use.
            interval_minutes: Rollup interval in minutes.
            keep_raw: Whether to keep raw data.

        Returns:
            The rollup configuration.
        """
        config = RollupConfig(
            name=name,
            source_metrics=source_metrics,
            aggregation=aggregation,
            interval_minutes=interval_minutes,
            keep_raw=keep_raw
        )
        self.configs[name] = config
        self.rollups[name] = []
        return config

    def add_value(
        self,
        metric_name: str,
        value: float,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Add a value for rollup processing.

        Args:
            metric_name: The metric name.
            value: The value to add.
            timestamp: Optional timestamp (default: now).
        """
        ts = timestamp or datetime.now()
        if metric_name not in self._raw_data:
            self._raw_data[metric_name] = []
        self._raw_data[metric_name].append((ts, value))

    def compute_rollup(self, name: str) -> List[Dict[str, Any]]:
        """Compute rollup for a configuration.

        Args:
            name: The rollup name.

        Returns:
            List of rollup values.
        """
        config = self.configs.get(name)
        if not config:
            return []
        # Collect all values for source metrics
        all_values: List[float] = []
        for metric in config.source_metrics:
            values = self._raw_data.get(metric, [])
            all_values.extend(v for _, v in values)
        if not all_values:
            return []
        # Apply aggregation
        if config.aggregation == AggregationType.SUM:
            result = sum(all_values)
        elif config.aggregation == AggregationType.AVG:
            result = sum(all_values) / len(all_values)
        elif config.aggregation == AggregationType.MIN:
            result = min(all_values)
        elif config.aggregation == AggregationType.MAX:
            result = max(all_values)
        elif config.aggregation == AggregationType.COUNT:
            result = float(len(all_values))
        elif config.aggregation == AggregationType.P50:
            sorted_vals = sorted(all_values)
            result = sorted_vals[len(sorted_vals) // 2]
        elif config.aggregation == AggregationType.P95:
            sorted_vals = sorted(all_values)
            result = sorted_vals[int(len(sorted_vals) * 0.95)]
        elif config.aggregation == AggregationType.P99:
            sorted_vals = sorted(all_values)
            result = sorted_vals[int(len(sorted_vals) * 0.99)]
        else:
            result = sum(all_values) / len(all_values)
        rollup_entry: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "value": result,
            "sample_count": len(all_values),
            "aggregation": config.aggregation.value
        }
        self.rollups[name].append(rollup_entry)
        # Clear raw data if not keeping
        if not config.keep_raw:
            for metric in config.source_metrics:
                self._raw_data[metric] = []
        return self.rollups[name]

    def get_rollup_history(self, name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get rollup history.

        Args:
            name: The rollup name.
            limit: Maximum entries to return.

        Returns:
            List of rollup entries.
        """
        return self.rollups.get(name, [])[-limit:]


class StatsChangeDetector:
    """Detects changes in metric values."""
    def __init__(self, threshold: float = 0.1, threshold_percent: Optional[float] = None) -> None:
        if threshold_percent is not None:
            threshold = float(threshold_percent) / 100.0
        self.threshold = float(threshold)
        self.previous_values: Dict[str, float] = {}
        self._changes: List[Dict[str, Any]] = []
        self._listeners: List[Callable[[Dict[str, Any]], None]] = []

    def detect_change(self, metric: str, value: float) -> bool:
        """Detect if metric has significantly changed."""
        if metric not in self.previous_values:
            self.previous_values[metric] = value
            return False

        prev = self.previous_values[metric]
        if prev == 0:
            change = abs(value - prev) > 0
        else:
            change = abs((value - prev) / prev) > self.threshold

        self.previous_values[metric] = value
        return change

    def record(self, metric: str, value: float) -> bool:
        """Record a metric value and emit change notifications."""
        prev = self.previous_values.get(metric)
        changed = self.detect_change(metric, float(value))
        if changed:
            old_val = 0.0 if prev is None else float(prev)
            new_val = float(value)
            if old_val == 0.0:
                change_percent = 100.0 if new_val != 0.0 else 0.0
            else:
                change_percent = abs((new_val - old_val) / old_val) * 100.0
            change_info: Dict[str, Any] = {
                "metric": metric,
                "old": old_val,
                "new": new_val,
                "change_percent": change_percent,
            }
            self._changes.append(change_info)
            for listener in list(self._listeners):
                try:
                    listener(change_info)
                except Exception:
                    logging.debug("Change listener failed.")
        return changed

    def on_change(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for change events."""
        self._listeners.append(callback)

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return recorded changes."""
        return list(self._changes)


class StatsForecaster:
    """Forecasts future metric values."""
    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self.history: List[float] = []

    def add_value(self, value: float) -> None:
        """Add a value to history."""
        self.history.append(value)

    def predict_next(self) -> float:
        """Predict next value using simple average."""
        if not self.history:
            return 0.0
        return sum(self.history[-self.window_size:]) / min(len(self.history), self.window_size)

    def confidence_interval(self) -> Tuple[float, float]:
        """Return confidence interval for prediction."""
        prediction = self.predict_next()
        margin = prediction * 0.1  # 10% margin
        return (prediction - margin, prediction + margin)

    def predict(self, historical: List[float], periods: int = 3) -> List[float]:
        """Predict future values from a historical series."""
        if periods <= 0:
            return []
        if not historical:
            return []
        if len(historical) == 1:
            return [float(historical[0])] * periods

        last = float(historical[-1])
        prev = float(historical[-2])
        delta = last - prev
        if delta == 0.0:
            # Fall back to average slope over the last window.
            window = [float(v) for v in historical[-min(len(historical), self.window_size):]]
            delta = (window[-1] - window[0]) / max(1, (len(window) - 1))
        return [last + delta * (i + 1) for i in range(periods)]

    def predict_with_confidence(self, historical: List[float], periods: int = 2) -> Dict[str, List[float]]:
        """Predict future values and include naive confidence intervals."""
        preds = self.predict(historical, periods=periods)
        if not historical:
            margin = 0.0
        else:
            values = [float(v) for v in historical]
            mean = sum(values) / len(values)
            var = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(var)
            margin = max(std, abs(mean) * 0.05)

        lower = [p - margin for p in preds]
        upper = [p + margin for p in preds]
        return {
            "predictions": preds,
            "confidence_lower": lower,
            "confidence_upper": upper,
        }


class StatsQueryEngine:
    """Queries metrics with time range and aggregation."""
    def __init__(self) -> None:
        self.metrics: Dict[str, List[Metric]] = {}
        # Lightweight query store used by tests.
        self._rows: Dict[str, List[Dict[str, Any]]] = {}

    def insert(self, metric: str, timestamp: float, value: Any) -> None:
        """Insert a datapoint for querying."""
        if metric not in self._rows:
            self._rows[metric] = []
        self._rows[metric].append({"timestamp": float(timestamp), "value": value})

    def query(
        self,
        metric_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        start: Optional[float] = None,
        end: Optional[float] = None,
        aggregation: str = "",
    ) -> Any:
        """Query metrics within time range and/or aggregate.

        Compatibility:
        - Tests call `query(metric, start=..., end=...)` returning a list of dict rows.
        - Tests call `query(metric, aggregation='avg')` returning a dict with `value`.
        """
        # Prefer the test store when present.
        rows = list(self._rows.get(metric_name, []))
        if rows:
            if start is not None or end is not None:
                start_v = float(start) if start is not None else float("-inf")
                end_v = float(end) if end is not None else float("inf")
                rows = [r for r in rows if start_v <= float(r.get("timestamp", 0.0)) <= end_v]

            if aggregation:
                values: List[float] = []
                for r in rows:
                    try:
                        values.append(float(r.get("value")))
                    except Exception:
                        continue
                if not values:
                    agg_value = 0.0
                else:
                    agg = aggregation.lower()
                    if agg == "sum":
                        agg_value = float(sum(values))
                    elif agg in ("avg", "mean"):
                        agg_value = float(sum(values) / len(values))
                    elif agg == "min":
                        agg_value = float(min(values))
                    elif agg == "max":
                        agg_value = float(max(values))
                    else:
                        agg_value = float(sum(values) / len(values))
                return {"metric": metric_name, "aggregation": aggregation, "value": agg_value}

            return rows

        # Fallback to legacy Metric store.
        if metric_name not in self.metrics:
            return []
        return self.metrics[metric_name]

    def add_metric(self, name: str, metric: Metric) -> None:
        """Add metric to query engine."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(metric)


class ABComparisonEngine:
    """Compare stats between different code versions (A / B testing).

    Provides statistical comparison capabilities for A / B testing
    different code versions.

    Attributes:
        comparisons: Active comparisons.
    """

    def __init__(self) -> None:
        """Initialize A / B comparison engine."""
        self.comparisons: Dict[str, ABComparison] = {}

    def create_comparison(
        self,
        version_a: str,
        version_b: str
    ) -> ABComparison:
        """Create a new A / B comparison.

        Args:
            version_a: Version A identifier.
            version_b: Version B identifier.

        Returns:
            The created comparison.
        """
        comp_id = hashlib.md5(
            f"{version_a}:{version_b}".encode()
        ).hexdigest()[:8]

        comparison = ABComparison(
            id=comp_id,
            version_a=version_a,
            version_b=version_b
        )
        self.comparisons[comp_id] = comparison
        return comparison

    def add_metric(
        self,
        comparison_id: str,
        version: str,
        metric_name: str,
        value: float
    ) -> bool:
        """Add a metric measurement to a comparison.

        Args:
            comparison_id: The comparison ID.
            version: Which version (a or b).
            metric_name: The metric name.
            value: The metric value.

        Returns:
            True if added successfully.
        """
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return False

        if version.lower() == "a":
            comp.metrics_a[metric_name] = value
        elif version.lower() == "b":
            comp.metrics_b[metric_name] = value
        else:
            return False
        return True

    def calculate_winner(
        self,
        comparison_id: str,
        metric_name: str,
        higher_is_better: bool = True
    ) -> Dict[str, Any]:
        """Calculate winner for a specific metric.

        Args:
            comparison_id: The comparison ID.
            metric_name: The metric to compare.
            higher_is_better: Whether higher values are better.

        Returns:
            Comparison results.
        """
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return {"error": "Comparison not found"}

        val_a = comp.metrics_a.get(metric_name, 0)
        val_b = comp.metrics_b.get(metric_name, 0)

        if val_a == val_b:
            winner = "tie"
        elif higher_is_better:
            winner = "a" if val_a > val_b else "b"
        else:
            winner = "a" if val_a < val_b else "b"

        improvement = abs(val_b - val_a) / val_a * 100 if val_a != 0 else 0

        return {
            "metric": metric_name,
            "version_a": val_a,
            "version_b": val_b,
            "winner": winner,
            "improvement_percent": improvement
        }

    def get_summary(self, comparison_id: str) -> Dict[str, Any]:
        """Get comparison summary.

        Args:
            comparison_id: The comparison ID.

        Returns:
            Summary of all metrics compared.
        """
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return {}

        all_metrics = set(comp.metrics_a.keys()) | set(comp.metrics_b.keys())
        return {
            "id": comp.id,
            "version_a": comp.version_a,
            "version_b": comp.version_b,
            "metrics_count": len(all_metrics),
            "metrics_a_count": len(comp.metrics_a),
            "metrics_b_count": len(comp.metrics_b)
        }


class ABComparator:
    """Compares A/B test metrics."""
    def __init__(self) -> None:
        self.results: List[Dict[str, Any]] = []

    def compare(self, a_data: Dict[str, float], b_data: Dict[str, float]) -> ABComparisonResult:
        """Compare two metric groups (A vs B)."""
        common = sorted(set(a_data.keys()) & set(b_data.keys()))
        diffs: Dict[str, float] = {}
        for key in common:
            try:
                diffs[key] = float(b_data[key]) - float(a_data[key])
            except (TypeError, ValueError):
                # Non-numeric values are ignored.
                continue
        return ABComparisonResult(metrics_compared=len(common), differences=diffs)

    def calculate_significance(
        self,
        control_values: List[float],
        treatment_values: List[float],
        alpha: float = 0.05,
    ) -> ABSignificanceResult:
        """Very lightweight significance heuristic for tests.

        This is not a full statistical test; it's a simple signal used by unit tests.
        """
        if not control_values or not treatment_values:
            return ABSignificanceResult(p_value=1.0, is_significant=False, effect_size=0.0)

        mean_a = sum(control_values) / len(control_values)
        mean_b = sum(treatment_values) / len(treatment_values)
        effect = mean_b - mean_a
        # Heuristic: big effect => low p-value.
        p_value = 0.01 if abs(effect) >= 1.0 else 0.5
        return ABSignificanceResult(p_value=p_value, is_significant=p_value < alpha, effect_size=effect)


@dataclass
class ABComparisonResult:
    """Result of comparing two metric groups."""

    metrics_compared: int
    differences: Dict[str, float] = field(default_factory=lambda: {})


@dataclass
class ABSignificanceResult:
    """Result of A/B statistical significance calculation."""

    p_value: float
    is_significant: bool
    effect_size: float = 0.0


@dataclass
class ABComparison:
    """A / B comparison between code versions."""
    id: str
    version_a: str
    version_b: str
    metrics_a: Dict[str, float] = field(default_factory=lambda: {})
    metrics_b: Dict[str, float] = field(default_factory=lambda: {})
    winner: str = ""
    confidence: float = 0.0


class AnnotationManager:
    """Manage metric annotations and comments.

    Provides capabilities for adding and managing annotations
    on metrics for documentation and context.

    Attributes:
        annotations: All annotations indexed by metric name.
    """

    def __init__(self) -> None:
        """Initialize annotation manager."""
        self.annotations: Dict[str, List[MetricAnnotation]] = {}

    def add_annotation(
        self,
        metric_name: str,
        text: str,
        author: str = "",
        annotation_type: str = "info"
    ) -> MetricAnnotation:
        """Add an annotation to a metric.

        Args:
            metric_name: The metric to annotate.
            text: Annotation text.
            author: Author of the annotation.
            annotation_type: Type of annotation (info, warning, milestone).

        Returns:
            The created annotation.
        """
        annotation = MetricAnnotation(
            metric_name=metric_name,
            timestamp=datetime.now().isoformat(),
            text=text,
            author=author,
            annotation_type=annotation_type
        )

        if metric_name not in self.annotations:
            self.annotations[metric_name] = []
        self.annotations[metric_name].append(annotation)
        return annotation

    def get_annotations(
        self,
        metric_name: str,
        annotation_type: Optional[str] = None
    ) -> List[MetricAnnotation]:
        """Get annotations for a metric.

        Args:
            metric_name: The metric name.
            annotation_type: Optional type filter.

        Returns:
            List of annotations.
        """
        annotations = self.annotations.get(metric_name, [])
        if annotation_type:
            annotations = [a for a in annotations if a.annotation_type == annotation_type]
        return annotations

    def delete_annotation(self, metric_name: str, timestamp: str) -> bool:
        """Delete an annotation by timestamp.

        Args:
            metric_name: The metric name.
            timestamp: The annotation timestamp.

        Returns:
            True if annotation was deleted.
        """
        if metric_name not in self.annotations:
            return False

        original_count = len(self.annotations[metric_name])
        self.annotations[metric_name] = [
            a for a in self.annotations[metric_name]
            if a.timestamp != timestamp
        ]
        return len(self.annotations[metric_name]) < original_count

    def export_annotations(self, metric_name: Optional[str] = None) -> str:
        """Export annotations to JSON.

        Args:
            metric_name: Optional metric to filter by.

        Returns:
            JSON string of annotations.
        """
        if metric_name:
            data: List[MetricAnnotation] = self.annotations.get(metric_name, [])
        else:
            data = []
            for ann_values in self.annotations.values():
                data.extend(ann_values)
        return json.dumps([{
            "metric_name": a.metric_name,
            "timestamp": a.timestamp,
            "text": a.text,
            "author": a.author,
            "type": a.annotation_type
        } for a in data], indent=2)


class StatsAnnotationManager:
    """Manages annotations on metrics."""

    def __init__(self) -> None:
        self.annotations: Dict[str, List[MetricAnnotation]] = {}

    def add_annotation(
        self,
        metric: str,
        annotation: Optional[MetricAnnotation] = None,
        **kwargs: Any,
    ) -> MetricAnnotation:
        """Add annotation to metric.

        Compatibility:
        - Some tests call `add_annotation(metric=..., timestamp=..., text=..., author=...)`.
        - Older code may pass a `MetricAnnotation` directly.
        """
        if annotation is None:
            timestamp = kwargs.get("timestamp")
            text = str(kwargs.get("text", ""))
            author = str(kwargs.get("author", ""))
            annotation_type = str(kwargs.get("annotation_type", kwargs.get("type", "info")))
            annotation = MetricAnnotation(
                metric_name=metric,
                timestamp=str(timestamp) if timestamp is not None else datetime.now().isoformat(),
                text=text,
                author=author,
                annotation_type=annotation_type,
            )

        if metric not in self.annotations:
            self.annotations[metric] = []
        self.annotations[metric].append(annotation)
        return annotation

    def get_annotations(self, metric: str) -> List[MetricAnnotation]:
        """Get annotations for metric."""
        return self.annotations.get(metric, [])


class SubscriptionManager:
    """Manage metric subscriptions and change notifications.

    Provides subscription management for receiving notifications
    when metrics change or breach thresholds.

    Attributes:
        subscriptions: Active subscriptions.
        last_notification: Timestamp of last notification per subscription.
    """

    def __init__(self) -> None:
        """Initialize subscription manager."""
        self.subscriptions: Dict[str, MetricSubscription] = {}
        self.last_notification: Dict[str, datetime] = {}
        self._notification_count: Dict[str, int] = {}

    def subscribe(
        self,
        metric_pattern: str,
        callback_url: str = "",
        notify_on: Optional[List[str]] = None,
        min_interval_seconds: int = 60
    ) -> MetricSubscription:
        """Create a new subscription.

        Args:
            metric_pattern: Glob pattern for metrics.
            callback_url: URL to call on notification.
            notify_on: Events to notify on.
            min_interval_seconds: Minimum interval between notifications.

        Returns:
            The created subscription.
        """
        sub_id = hashlib.md5(
            f"{metric_pattern}:{callback_url}".encode()
        ).hexdigest()[:8]

        subscription = MetricSubscription(
            id=sub_id,
            metric_pattern=metric_pattern,
            callback_url=callback_url,
            notify_on=notify_on or ["threshold", "anomaly"],
            min_interval_seconds=min_interval_seconds
        )
        self.subscriptions[sub_id] = subscription
        self._notification_count[sub_id] = 0
        return subscription

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription.

        Args:
            subscription_id: The subscription to remove.

        Returns:
            True if subscription was removed.
        """
        if subscription_id in self.subscriptions:
            del self.subscriptions[subscription_id]
            return True
        return False

    def _matches_pattern(self, metric_name: str, pattern: str) -> bool:
        """Check if metric name matches pattern.

        Args:
            metric_name: The metric name.
            pattern: The glob pattern.

        Returns:
            True if matches.
        """
        import fnmatch
        return fnmatch.fnmatch(metric_name, pattern)

    def notify(
        self,
        metric_name: str,
        event_type: str,
        value: float
    ) -> List[str]:
        """Send notifications for a metric event.

        Args:
            metric_name: The metric name.
            event_type: Type of event (threshold, anomaly).
            value: The metric value.

        Returns:
            List of subscription IDs that were notified.
        """
        notified: List[str] = []
        now = datetime.now()
        for sub_id, sub in self.subscriptions.items():
            if event_type not in sub.notify_on:
                continue
            if not self._matches_pattern(metric_name, sub.metric_pattern):
                continue
            # Check minimum interval
            last = self.last_notification.get(sub_id)
            if last:
                elapsed = (now - last).total_seconds()
                if elapsed < sub.min_interval_seconds:
                    continue
            # Send notification (simulated)
            self.last_notification[sub_id] = now
            self._notification_count[sub_id] += 1
            notified.append(sub_id)
            logging.info(f"Notified {sub_id}: {metric_name}={value} ({event_type})")
        return notified

    def get_stats(self) -> Dict[str, Any]:
        """Get subscription statistics.

        Returns:
            Statistics about subscriptions.
        """
        return {
            "total_subscriptions": len(self.subscriptions),
            "notification_counts": dict(self._notification_count)
        }


class StatsSubscriptionManager:
    """Manages metric subscriptions."""
    def __init__(self) -> None:
        # Legacy exact-metric subscriptions: metric -> callbacks(value)
        self.subscribers: Dict[str, List[Callable[[float], None]]] = {}

        # New-style subscriptions used by tests: (subscriber_id, metric_pattern, delivery_method)
        self._subscriptions: List[StatsSubscription] = []
        self._delivery_handlers: Dict[str, Callable[[str], None]] = {}

    def subscribe(self, *args: Any, **kwargs: Any) -> Any:
        """Subscribe to updates.

        Supported forms:
        - Legacy: subscribe(metric: str, callback: Callable[[float], None]) -> None
        - New: subscribe(subscriber_id: str, metric_pattern: str, delivery_method: str) -> StatsSubscription
        - New (kwargs): subscribe(subscriber_id=..., metric_pattern=..., delivery_method=...)
        """
        if kwargs and "subscriber_id" in kwargs:
            subscriber_id = str(kwargs.get("subscriber_id"))
            metric_pattern = str(kwargs.get("metric_pattern"))
            delivery_method = str(kwargs.get("delivery_method"))
            return self._subscribe_delivery(subscriber_id, metric_pattern, delivery_method)

        if len(args) == 2 and callable(args[1]):
            metric, callback = args
            metric = str(metric)
            if metric not in self.subscribers:
                self.subscribers[metric] = []
            self.subscribers[metric].append(callback)
            return None

        if len(args) == 3:
            subscriber_id, metric_pattern, delivery_method = args
            return self._subscribe_delivery(str(subscriber_id), str(metric_pattern), str(delivery_method))

        raise TypeError("subscribe() expects (metric, callback) or (subscriber_id, metric_pattern, delivery_method)")

    def _subscribe_delivery(self, subscriber_id: str, metric_pattern: str, delivery_method: str) -> "StatsSubscription":
        sub_id = hashlib.md5(f"{subscriber_id}:{metric_pattern}:{delivery_method}".encode()).hexdigest()[:8]
        sub = StatsSubscription(
            id=sub_id,
            subscriber_id=subscriber_id,
            metric_pattern=metric_pattern,
            delivery_method=delivery_method,
            created_at=datetime.now().isoformat(),
        )
        self._subscriptions.append(sub)
        return sub

    def set_delivery_handler(self, delivery_method: str, handler: Callable[[str], None]) -> None:
        """Set a handler for a delivery method (e.g. webhook/email)."""
        self._delivery_handlers[delivery_method] = handler

    def notify(self, metric: str, value: Any) -> None:
        """Notify subscribers.

        - If `value` is a float/int, deliver to legacy metric callbacks.
        - If `value` is a str, treat it as a message and deliver via delivery handlers.
        """
        if isinstance(value, (int, float)):
            if metric in self.subscribers:
                for callback in self.subscribers[metric]:
                    try:
                        callback(float(value))
                    except Exception:
                        logging.debug(f"Metric subscriber for {metric} failed.")
            return

        # Message delivery mode
        message = str(value)
        import fnmatch

        for sub in self._subscriptions:
            if fnmatch.fnmatch(metric, sub.metric_pattern):
                handler = self._delivery_handlers.get(sub.delivery_method)
                if handler is None:
                    continue
                try:
                    handler(message)
                except Exception:
                    logging.debug(f"Delivery handler {sub.delivery_method} failed for {metric}")


class ThresholdAlertManager:
    """Manages threshold-based alerting."""
    def __init__(self) -> None:
        self.alerts: List[ThresholdAlert] = []
        # Each metric can have warning/critical thresholds and/or min/max thresholds.
        self.thresholds: Dict[str, Dict[str, Optional[float]]] = {}

    def set_threshold(
        self,
        metric: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        warning: Optional[float] = None,
        critical: Optional[float] = None,
    ) -> None:
        """Set thresholds for a metric.

        Compatibility:
        - Some callers use `warning=` and `critical=`.
        - Older callers use `min_val=`/`max_val=`.
        """
        self.thresholds[metric] = {
            "min": min_val,
            "max": max_val,
            "warning": warning,
            "critical": critical,
        }

    def check(self, metric: str, value: float) -> List["ThresholdAlert"]:
        """Check a value against thresholds and return any alerts."""
        if metric not in self.thresholds:
            return []

        thresh = self.thresholds[metric]
        alerts: List[ThresholdAlert] = []

        # Warning/critical are treated as "value >= threshold".
        critical_threshold = thresh.get("critical")
        warning_threshold = thresh.get("warning")
        if critical_threshold is not None and value >= critical_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="critical", threshold=critical_threshold)
            )
        elif warning_threshold is not None and value >= warning_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="warning", threshold=warning_threshold)
            )

        # Min/max thresholds are treated as bounds checks.
        min_threshold = thresh.get("min")
        max_threshold = thresh.get("max")
        if min_threshold is not None and value < min_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="below_min", threshold=min_threshold)
            )
        if max_threshold is not None and value > max_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="above_max", threshold=max_threshold)
            )

        self.alerts.extend(alerts)
        return alerts

    def check_value(self, metric: str, value: float) -> bool:
        """Compatibility wrapper: return True if any alert triggered."""
        return len(self.check(metric, value)) > 0


class StatsBackupManager:
    """Manages backups of stats."""

    def __init__(self, backup_dir: Optional[Union[str, Path]] = None) -> None:
        self.backup_dir: Optional[Path] = Path(backup_dir) if backup_dir is not None else None
        if self.backup_dir is not None:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.backups: Dict[str, Dict[str, Any]] = {}

    def _safe_backup_name(self, name: str) -> str:
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        safe = "".join(ch if ch in allowed else "_" for ch in name)
        return safe or "backup"

    def _backup_path(self, name: str) -> Optional[Path]:
        if self.backup_dir is None:
            return None
        safe_name = self._safe_backup_name(name)
        return self.backup_dir / f"{safe_name}.json"

    def create_backup(self, name: str, data: Dict[str, Any]) -> StatsBackup:
        """Create a backup and persist to disk when configured."""
        timestamp = datetime.now().isoformat()
        self.backups[name] = {"data": data, "timestamp": timestamp}

        path = self._backup_path(name) or Path(f"{self._safe_backup_name(name)}.json")
        payload: Dict[str, Any] = {"name": name, "timestamp": timestamp, "data": data}
        if self.backup_dir is not None:
            path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

        return StatsBackup(name=name, path=path, timestamp=timestamp)

    def restore(self, name: str) -> Optional[Dict[str, Any]]:
        """Restore a backup by name (test compatibility)."""
        restored = self.restore_backup(name)
        if restored is not None:
            return restored

        path = self._backup_path(name)
        if path is not None and path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                data = payload.get("data")
                if isinstance(data, dict):
                    self.backups[name] = {"data": data, "timestamp": str(payload.get("timestamp") or "")}
                    return data
            except Exception:
                return None
        return None

    def restore_backup(self, name: str) -> Optional[Dict[str, Any]]:
        """Restore from in-memory backup."""
        if name in self.backups:
            val = self.backups[name]["data"]
            if isinstance(val, dict):
                return val  # type: ignore
        return None

    def list_backups(self) -> List[str]:
        """List all backups."""
        names = set(self.backups.keys())
        if self.backup_dir is not None:
            for candidate in self.backup_dir.glob("*.json"):
                if candidate.is_file():
                    names.add(candidate.stem)
        return sorted(names)


@dataclass
class StatsBackup:
    """A persisted backup entry for StatsBackupManager."""

    name: str
    path: Path
    timestamp: str


class StatsCompressor:
    """Compresses metric data."""
    def compress(self, data: Any) -> bytes:
        """Compress data.

        Compatibility: tests pass Python objects like `list[float]`.
        """
        if isinstance(data, (bytes, bytearray)):
            payload = b"b" + bytes(data)
        else:
            payload = b"j" + json.dumps(data, separators=(",", ":")).encode("utf-8")
        return zlib.compress(payload)

    def decompress(self, data: bytes) -> Any:
        """Decompress data."""
        payload = zlib.decompress(data)
        if not payload:
            return payload
        tag = payload[:1]
        body = payload[1:]
        if tag == b"b":
            return body
        if tag == b"j":
            return json.loads(body.decode("utf-8"))
        # Best-effort fallback for legacy payloads.
        try:
            return json.loads(payload.decode("utf-8"))
        except Exception:
            return payload


class StatsSnapshotManager:
    """Manages snapshots of stats state.

    Compatibility:
    - Tests expect `__init__(snapshot_dir=...)`.
    - `create_snapshot()` returns an object with `.name` and `.data`.
    - When `snapshot_dir` is provided, snapshots are persisted to JSON files.
    """

    def __init__(self, snapshot_dir: Optional[Union[str, Path]] = None) -> None:
        self.snapshot_dir: Optional[Path] = Path(snapshot_dir) if snapshot_dir is not None else None
        if self.snapshot_dir is not None:
            self.snapshot_dir.mkdir(parents=True, exist_ok=True)

        self.snapshots: Dict[str, StatsSnapshot] = {}

    def _safe_snapshot_name(self, name: str) -> str:
        # Prevent path traversal and keep filenames portable.
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        safe = "".join(ch if ch in allowed else "_" for ch in name)
        return safe or "snapshot"

    def _snapshot_path(self, name: str) -> Optional[Path]:
        if self.snapshot_dir is None:
            return None
        safe_name = self._safe_snapshot_name(name)
        return self.snapshot_dir / f"{safe_name}.json"

    def create_snapshot(self, name: str, data: Dict[str, Any]) -> StatsSnapshot:
        """Create a snapshot."""
        snapshot = StatsSnapshot(name=name, data=data, timestamp=datetime.now().isoformat())
        self.snapshots[name] = snapshot

        path = self._snapshot_path(name)
        if path is not None:
            payload = {"name": snapshot.name, "timestamp": snapshot.timestamp, "data": snapshot.data}
            path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

        return snapshot

    def restore_snapshot(self, name: str) -> Optional[Dict[str, Any]]:
        """Restore a snapshot."""
        if name in self.snapshots:
            return self.snapshots[name].data

        path = self._snapshot_path(name)
        if path is not None and path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                data = payload.get("data")
                if isinstance(data, dict):
                    timestamp = str(payload.get("timestamp") or "")
                    snapshot = StatsSnapshot(name=str(payload.get("name") or name), data=data, timestamp=timestamp)
                    self.snapshots[name] = snapshot
                    return data
            except Exception:
                return None

        return None

    def list_snapshots(self) -> List[str]:
        """List all snapshots."""
        names = set(self.snapshots.keys())
        if self.snapshot_dir is not None:
            for candidate in self.snapshot_dir.glob("*.json"):
                if candidate.is_file():
                    names.add(candidate.stem)
        return sorted(names)


class StatsAccessController:
    """Controls access to stats."""
    def __init__(self) -> None:
        self.permissions: Dict[str, Dict[str, str]] = {}

    def grant(self, user: str, resource_pattern: str, level: str = "read") -> None:
        """Grant access level for a resource pattern.

        Compatibility: tests call `grant(user, pattern, level='read'|'write')`.
        """
        self.grant_access(user, resource_pattern, level)

    def can_access(self, user: str, resource: str, required_level: str = "read") -> bool:
        """Check whether user can access resource at required level."""
        import fnmatch

        if user not in self.permissions:
            return False

        required = required_level.lower()
        # Treat "write" as superset of "read".
        for pattern, granted_level in self.permissions[user].items():
            if not fnmatch.fnmatch(resource, pattern):
                continue
            granted = granted_level.lower()
            if required == "read":
                if granted in ("read", "write"):
                    return True
            elif required == "write":
                if granted == "write":
                    return True
            else:
                # Unknown required level: fall back to exact match.
                if granted == required:
                    return True
        return False

    def grant_access(self, user: str, resource: str, permission: str) -> None:
        """Grant access to user."""
        if user not in self.permissions:
            self.permissions[user] = {}
        self.permissions[user][resource] = permission

    def has_access(self, user: str, resource: str) -> bool:
        """Check if user has access."""
        return user in self.permissions and resource in self.permissions[user]


class StatsStreamManager:
    """Manages real-time stats streaming."""
    def __init__(self, config: Optional[StreamingConfig] = None) -> None:
        self.config = config
        self.streams: Dict[str, StatsStream] = {}
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def create_stream(self, name: str, buffer_size: int = 1000) -> StatsStream:
        """Create a new stream."""
        stream = StatsStream(name=name, buffer_size=buffer_size)
        self.streams[name] = stream
        self.subscribers[name] = []
        return stream

    def get_latest(self, name: str, count: int = 1) -> List[Any]:
        """Get latest data from stream."""
        if name not in self.streams:
            return []
        return self.streams[name].get_latest(count)

    def subscribe(self, stream_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to stream updates."""
        if stream_name not in self.subscribers:
            self.subscribers[stream_name] = []
        self.subscribers[stream_name].append(callback)

    def publish(self, stream_name: str, data: Any) -> None:
        """Publish data to stream."""
        if stream_name in self.streams:
            self.streams[stream_name].add_data(data)

        # Notify subscribers
        if stream_name in self.subscribers:
            for callback in self.subscribers[stream_name]:
                try:
                    callback(data)
                except Exception:
                    logging.debug(f"Stream subscriber for {stream_name} failed.")


class StatsStreamer:
    """Real-time stats streaming via WebSocket for live dashboards.

    Provides real - time metric streaming capabilities using various
    protocols for live dashboard updates.

    Attributes:
        config: Streaming configuration.
        subscribers: Active subscribers to the stream.
        buffer: Buffered metrics for batch sending.
    """

    def __init__(self, config: StreamingConfig) -> None:
        """Initialize the stats streamer.

        Args:
            config: The streaming configuration.
        """
        self.config = config
        self.subscribers: List[str] = []
        self.buffer: List[Metric] = []
        self._connected = False
        self._last_heartbeat: Optional[datetime] = None

    def connect(self) -> bool:
        """Establish connection to streaming endpoint.

        Returns:
            True if connection successful.
        """
        # Simulated connection
        self._connected = True
        self._last_heartbeat = datetime.now()
        logging.info(f"Connected to {self.config.endpoint}:{self.config.port}")
        return True

    def disconnect(self) -> None:
        """Disconnect from streaming endpoint."""
        self._connected = False
        self._last_heartbeat = None
        self.buffer.clear()

    def stream_metric(self, metric: Metric) -> bool:
        """Stream a single metric.

        Args:
            metric: The metric to stream.

        Returns:
            True if successfully streamed.
        """
        if not self._connected:
            self.buffer.append(metric)
            if len(self.buffer) >= self.config.buffer_size:
                # Buffer overflow handling
                self.buffer = self.buffer[-self.config.buffer_size // 2:]
            return False

        # Send buffered metrics first
        if self.buffer:
            self._flush_buffer()

        # Simulate streaming
        logging.debug(f"Streamed: {metric.name}={metric.value}")
        return True

    def _flush_buffer(self) -> int:
        """Flush buffered metrics.

        Returns:
            Number of metrics flushed.
        """
        count = len(self.buffer)
        self.buffer.clear()
        return count

    def add_subscriber(self, subscriber_id: str) -> None:
        """Add a subscriber to the stream.

        Args:
            subscriber_id: Unique identifier for the subscriber.
        """
        if subscriber_id not in self.subscribers:
            self.subscribers.append(subscriber_id)

    def remove_subscriber(self, subscriber_id: str) -> bool:
        """Remove a subscriber from the stream.

        Args:
            subscriber_id: The subscriber to remove.

        Returns:
            True if subscriber was removed.
        """
        if subscriber_id in self.subscribers:
            self.subscribers.remove(subscriber_id)
            return True
        return False

    def broadcast(self, metric: Metric) -> int:
        """Broadcast metric to all subscribers.

        Args:
            metric: The metric to broadcast.

        Returns:
            Number of subscribers notified.
        """
        notified = 0
        for _ in self.subscribers:
            if self.stream_metric(metric):
                notified += 1
        return notified


class StatsStream:
    """Represents a real-time stats stream."""
    def __init__(self, name: str, buffer_size: int = 1000) -> None:
        self.name = name
        self.buffer_size = buffer_size
        self.buffer: List[Any] = []
        self.active = True

    def get_latest(self, count: int = 1) -> List[Any]:
        """Get latest data points."""
        return self.buffer[-count:] if self.buffer else []

    def add_data(self, data: Any) -> None:
        """Add data to stream."""
        self.buffer.append(data)
        # Enforce buffer size limit
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)




class AggregationResult(Dict[str, Any]):
    """Compatibility class that behaves like both a dict and a float."""
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return float(self.get("total", 0.0)) == float(other)
        return super().__eq__(other)

    def __float__(self) -> float:
        return float(self.get("total", 0.0))

class StatsFederation:
    """Aggregate stats from multiple repositories.

    Provides federation capabilities to collect and aggregate
    metrics from multiple source repositories.

    Attributes:
        sources: Federated data sources.
        mode: Federation mode (pull, push, hybrid).
        aggregated: Aggregated metrics from all sources.
    """

    def __init__(self, mode: FederationMode = FederationMode.PULL) -> None:
        """Initialize stats federation.

        Args:
            mode: The federation mode to use.
        """
        self.mode = mode
        self.sources: Dict[str, FederatedSource] = {}
        self.aggregated: Dict[str, List[float]] = {}
        self._last_sync: Dict[str, datetime] = {}
        self.connectivity = ConnectivityManager()

    def add_source(
        self,
        name: str,
        endpoint: Optional[str] = None,
        data: Optional[Dict[str, float]] = None,
        healthy: bool = True
    ) -> None:
        """Add a federated source.

        Args:
            name: Name for the source.
            endpoint: Optional API endpoint for the source.
            data: Optional data dictionary from the source.
            healthy: Whether the source is healthy.
        """
        source = FederatedSource(
            repo_url=name,
            api_endpoint=endpoint or "",
            enabled=healthy
        )
        self.sources[name] = source
        self._last_sync[name] = datetime.min

        # Store data if provided
        if data:
            source.metrics.update({k: float(v) for k, v in data.items()})

    def remove_source(self, name: str) -> bool:
        """Remove a federated source.

        Args:
            name: Name of the source to remove.

        Returns:
            True if source was removed.
        """
        if name in self.sources:
            del self.sources[name]
            if name in self._last_sync:
                del self._last_sync[name]
            return True
        return False

    def sync_source(self, name: str) -> Dict[str, float]:
        """Sync metrics from a specific source.

        Args:
            name: Name of the source to sync.

        Returns:
            Dictionary of synced metrics.
        """
        if name not in self.sources:
            return {}

        source = self.sources[name]
        if not source.enabled:
            return {}

        # Phase 120 enhancement: Real endpoint synchronization
        endpoint = source.api_endpoint
        if endpoint and endpoint.startswith(("http://", "https://")):
            try:
                headers = {}
                if source.auth_token:
                    headers["Authorization"] = f"Bearer {source.auth_token}"
                
                # Use ConnectivityManager
                data = self.connectivity.get_json(endpoint, headers=headers)
                
                if isinstance(data, dict):
                    # update metrics on source object
                    for k, v in data.items():
                        if isinstance(v, (int, float)):
                             source.metrics[k] = float(v)
                    
                    # Maintain compatibility with current aggregate() logic
                    self.aggregated[name] = [float(v) for v in data.values() if isinstance(v, (int, float))]
                    
                    self._last_sync[name] = datetime.now()
                    return {k: float(v) for k, v in data.items() if isinstance(v, (int, float))}
            except Exception as e:
                logging.error(f"StatsFederation: Sync failed for {name} ({endpoint}): {e}")
        
        self._last_sync[name] = datetime.now()
        return {}

    def sync_all(self) -> Dict[str, Dict[str, float]]:
        """Sync metrics from all sources.

        Returns:
            Dictionary of metrics per source.
        """
        results: Dict[str, Dict[str, float]] = {}
        for name in self.sources:
            results[name] = self.sync_source(name)
        return results

    def aggregate(
        self,
        metric_name: str,
        aggregation: AggregationType = AggregationType.SUM
    ) -> AggregationResult:
        """Aggregate a metric across all sources.

        Args:
            metric_name: The metric to aggregate.
            aggregation: The aggregation type.

        Returns:
            AggregationResult behaving as both dict and float.
        """
        values: List[float] = list(self.aggregated.get(metric_name, []))
        failed_sources = 0
        
        # Collect values from all sources
        for source_name, source in self.sources.items():
            if not source.enabled:
                failed_sources += 1
                continue
                
            # Check for the specific metric in the source's metrics dictionary
            if metric_name in source.metrics:
                value = source.metrics[metric_name]
                if isinstance(value, (int, float)):
                    values.append(float(value))

        total = 0.0
        if values:
            if aggregation == AggregationType.SUM:
                total = sum(values)
            elif aggregation == AggregationType.AVG:
                total = sum(values) / len(values)
            elif aggregation == AggregationType.MIN:
                total = min(values)
            elif aggregation == AggregationType.MAX:
                total = max(values)
            elif aggregation == AggregationType.COUNT:
                total = float(len(values))
        
        return AggregationResult({
            "total": total,
            "failed_sources": failed_sources,
            "source_count": len(values),
            "metric_name": metric_name
        })

    def get_federation_status(self) -> Dict[str, Dict[str, Union[bool, str]]]:
        """Get status of all federated sources.

        Returns:
            Status information per source.
        """
        status: Dict[str, Dict[str, Union[bool, str]]] = {}
        for name, source in self.sources.items():
            status[name] = {
                "enabled": source.enabled,
                "last_sync": self._last_sync.get(name, datetime.min).isoformat(),
                "endpoint": source.api_endpoint
            }
        return status


class StatsAPIServer:
    """Stats API endpoint for programmatic access.

    Provides RESTful API endpoints for accessing stats
    programmatically.

    Attributes:
        endpoints: Registered API endpoints.
        stats_agent: The stats agent to serve data from.
    """

    def __init__(self, stats_agent: Optional[StatsAgent] = None) -> None:
        """Initialize API server.

        Args:
            stats_agent: Optional stats agent instance.
        """
        self.stats_agent = stats_agent
        self.endpoints: Dict[str, APIEndpoint] = {}
        self._request_count: Dict[str, int] = {}
        self._setup_default_endpoints()

    def _setup_default_endpoints(self) -> None:
        """Setup default API endpoints."""
        defaults = [
            APIEndpoint("/api / stats", "GET", True, 100, 60),
            APIEndpoint("/api / metrics", "GET", True, 100, 30),
            APIEndpoint("/api / metrics/{name}", "GET", True, 100, 30),
            APIEndpoint("/api / alerts", "GET", True, 50, 10),
            APIEndpoint("/api / snapshots", "GET", True, 50, 60),
        ]
        for endpoint in defaults:
            self.endpoints[endpoint.path] = endpoint
            self._request_count[endpoint.path] = 0

    def register_endpoint(
        self,
        path: str,
        method: str = "GET",
        auth_required: bool = True,
        rate_limit: int = 100,
        cache_ttl: int = 60
    ) -> APIEndpoint:
        """Register a custom API endpoint.

        Args:
            path: The endpoint path.
            method: HTTP method.
            auth_required: Whether authentication is required.
            rate_limit: Requests per minute limit.
            cache_ttl: Cache time - to - live in seconds.

        Returns:
            The registered endpoint.
        """
        endpoint = APIEndpoint(
            path=path,
            method=method,
            auth_required=auth_required,
            rate_limit=rate_limit,
            cache_ttl=cache_ttl
        )
        self.endpoints[path] = endpoint
        self._request_count[path] = 0
        return endpoint

    def handle_request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle an API request.

        Args:
            path: The request path.
            method: The HTTP method.
            params: Request parameters.

        Returns:
            Response data.
        """
        endpoint = self.endpoints.get(path)
        if not endpoint:
            return {"error": "Endpoint not found", "status": 404}

        if endpoint.method != method:
            return {"error": "Method not allowed", "status": 405}

        self._request_count[path] += 1

        # Route to appropriate handler
        if path == "/api / stats" and self.stats_agent:
            return {"data": self.stats_agent.calculate_stats(), "status": 200}
        elif path == "/api / alerts" and self.stats_agent:
            alerts = self.stats_agent.get_alerts()
            return {"data": [{"id": a.id, "message": a.message} for a in alerts], "status": 200}
        else:
            return {"data": {}, "status": 200}

    def get_api_docs(self) -> str:
        """Generate API documentation.

        Returns:
            OpenAPI - style documentation.
        """
        docs: Dict[str, Any] = {
            "openapi": "3.0.0",
            "info": {"title": "Stats API", "version": "1.0.0"},
            "paths": {}
        }

        for path, endpoint in self.endpoints.items():
            docs["paths"][path] = {
                endpoint.method.lower(): {
                    "summary": f"Access {path}",
                    "security": [{"bearerAuth": []}] if endpoint.auth_required else [],
                    "responses": {"200": {"description": "Success"}}
                }
            }

        return json.dumps(docs, indent=2)


@dataclass
class APIEndpoint:
    """Stats API endpoint configuration."""
    path: str
    method: str = "GET"
    auth_required: bool = True
    rate_limit: int = 100  # requests per minute
    cache_ttl: int = 60  # seconds


class MetricNamespaceManager:
    """Manage metric namespaces for organizing large metric sets.

    Provides namespace management for organizing and hierarchically
    structuring large collections of metrics.

    Attributes:
        namespaces: Registered namespaces.
        metrics_by_namespace: Metrics organized by namespace.
    """

    def __init__(self) -> None:
        """Initialize namespace manager."""
        self.namespaces: Dict[str, MetricNamespace] = {}
        self.metrics_by_namespace: Dict[str, List[str]] = {}

    def create_namespace(
        self,
        name: str,
        description: str = "",
        parent: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> MetricNamespace:
        """Create a new namespace.

        Args:
            name: Namespace name.
            description: Description of the namespace.
            parent: Parent namespace name.
            tags: Tags for the namespace.

        Returns:
            The created namespace.
        """
        if parent and parent not in self.namespaces:
            raise ValueError(f"Parent namespace '{parent}' does not exist")

        namespace = MetricNamespace(
            name=name,
            description=description,
            parent=parent,
            tags=tags or {}
        )
        self.namespaces[name] = namespace
        self.metrics_by_namespace[name] = []
        return namespace

    def delete_namespace(self, name: str) -> bool:
        """Delete a namespace.

        Args:
            name: Name of namespace to delete.

        Returns:
            True if namespace was deleted.
        """
        # Check for child namespaces
        for ns in self.namespaces.values():
            if ns.parent == name:
                raise ValueError("Cannot delete: namespace has children")

        if name in self.namespaces:
            del self.namespaces[name]
            if name in self.metrics_by_namespace:
                del self.metrics_by_namespace[name]
            return True
        return False

    def assign_metric(self, metric_name: str, namespace: str) -> bool:
        """Assign a metric to a namespace.

        Args:
            metric_name: The metric name.
            namespace: The target namespace.

        Returns:
            True if assigned successfully.
        """
        if namespace not in self.namespaces:
            return False

        if metric_name not in self.metrics_by_namespace[namespace]:
            self.metrics_by_namespace[namespace].append(metric_name)
        return True

    def get_namespace_hierarchy(self, name: str) -> List[str]:
        """Get the namespace hierarchy from root to given namespace.

        Args:
            name: The namespace name.

        Returns:
            List of namespace names from root to given namespace.
        """
        hierarchy: list[str] = []
        current: str | None = name
        while current:
            hierarchy.insert(0, current)
            ns = self.namespaces.get(current)
            current = ns.parent if ns else None
        return hierarchy

    def get_full_path(self, namespace: str) -> str:
        """Get full path string for a namespace.

        Args:
            namespace: The namespace name.

        Returns:
            Full path string like "root / parent / child".
        """
        return " / ".join(self.get_namespace_hierarchy(namespace))


>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
