#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Logic for metric analysis, profiling, stability, and forecasting.

from __future__ import annotations
import ast
import logging
import math
import operator
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from .metrics import (
    DerivedMetric,
    MetricCorrelation,
    ABComparisonResult,
    ABSignificanceResult,
)

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger = logging.getLogger(__name__)

# Mock for matplotlib if not present
has_matplotlib = False
try:
    import matplotlib.pyplot as plt
    has_matplotlib = True
except ImportError:
    plt = None  # type: ignore[assignment]

# Model costs for TokenCostEngine
MODEL_COSTS = {
    "gpt-4o": {"input": 0.005, "output": 0.015, "total": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006, "total": 0.0004},
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015, "total": 0.009},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125, "total": 0.00075},
    "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105, "total": 0.007},
    "gemini-1.5-flash": {"input": 0.00035, "output": 0.00105, "total": 0.0007},
    "default": {"input": 0.002, "output": 0.006, "total": 0.004}
}


@dataclass(frozen=True)
class ProfileStats:




    function_name: str
    call_count: int
    total_time: float
    per_call: float



class ProfilingCore:
    """Pure logic for cProfile aggregation and bottleneck analysis."""
    def analyze_stats(self, pstats_obj:
        Any, limit: int = 10) -> list[ProfileStats]:










        results: list[Any] = []


        pstats_obj.sort_stats('cumulative')
        for func, (cc, nc, tt, ct, callers) in pstats_obj.stats.items():

            if len(results) >= limit:
                break
            results.append(ProfileStats(
                function_name=str(func),
                call_count=cc,




                total_time=ct,
                per_call=ct / cc if cc > 0 else 0
            ))

        return results

    def identify_bottlenecks(self, stats:




        list[ProfileStats], threshold_ms: float = 100.0) -> list[str]:
        return [s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)]

    def calculate_optimization_priority(self, stats:






        ProfileStats) -> float:
        return stats.total_time * stats.call_count






@dataclass(frozen=True)
class FleetMetrics:
    avg_error_rate: float
    total_token_out: int
    active_agent_count: int
    latency_p95: float







class StabilityCore:
    """Pure logic for calculating fleet stability and reasoning coherence."""
    def calculate_stability_score(self, metrics:
        FleetMetrics, sae_anomalies: int) -> float:
        score = 1.0




        score -= (metrics.avg_error_rate * 5.0)
        score -= (sae_anomalies * 0.05)
        latency_penalty = max(0.0, (metrics.latency_p95 - 2000) / 10000)










        score -= latency_penalty
        return min(max(score, 0.0), 1.0)

    def is_in_stasis(self, score_history:
        list[float]) -> bool:
        if len(score_history) < 10:








            return False
        avg = sum(score_history)/len(score_history)
        variance = sum((x - avg)**2 for x in score_history) / len(score_history)
        return variance < 0.0001

    def get_healing_threshold(self, stability_score:
        float) -> float:
        if stability_score < 0.3:
            return 0.9
        return 0.5

class TracingCore:
    """distributed tracing and latency breakdown logic."""
    def create_span_context(self, trace_id:
        str, span_id: str) -> dict[str, str]:
        return {"trace_id": trace_id, "span_id": span_id, "version": "OTel-1.1"}

    def calculate_latency_breakdown(self, total_time:
        float, network_time: float) -> dict[str, float]:

        thinking_time = total_time - network_time
        return {
            "total_latency_ms": total_time * 1000,
            "network_latency_ms": network_time * 1000,
            "agent_thinking_ms": thinking_time * 1000,









            "think_ratio": thinking_time / total_time if total_time > 0 else 0
        }

    def format_otel_log(self, name:




        str, attributes: dict[str, Any]) -> dict[str, Any]:
        return {"timestamp": time.time_ns(), "name": name, "attributes": attributes, "kind": "INTERNAL"}




class DerivedMetricCalculator:
    """Calculate derived metrics from dependencies using safe AST evaluation."""
    def __init__(self) -> None:










        self.derived_metrics: dict[str, DerivedMetric] = {}
        self._cache: dict[str, float] = {}
        self.operators = {
            ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,






            ast.Div: operator.truediv, ast.Pow: operator.pow, ast.BitXor: operator.xor,
            ast.USub: operator.neg, ast.UAdd: operator.pos
        }











    def _eval_node(self, node:
        ast.AST) -> float:
        if isinstance(node, ast.Constant):
            return float(node.value)
        elif hasattr(ast, "Num") and isinstance(node, ast.Num):







            return float(node.n)
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))



        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                args = [self._eval_node(a) for a in node.args]




                if func_name == "abs":
                    return abs(args[0])
                if func_name == "max":
                    return max(args)
                if func_name == "min":
                    return min(args)
                if func_name == "sqrt":

                    return math.sqrt(args[0])
                if func_name == "pow":
                    return math.pow(args[0], args[1])
            raise TypeError(f"Unsupported function: {node.func}")



        raise TypeError(f"Unsupported operation: {type(node)}")


    def register_derived(self, name:
        str, dependencies: list[str], formula: str, description: str = "") -> DerivedMetric:

        derived = DerivedMetric(name=name, dependencies=dependencies, formula=formula, description=description)
        self.derived_metrics[name] = derived
        return derived



    def calculate(self, name:
        str, metric_values: dict[str, float]) -> float | None:
        derived = self.derived_metrics.get(name)
        if not derived:
            return None
        for dep in derived.dependencies:










            if dep not in metric_values:
                return None
        formula = derived.formula


        for dep in derived.dependencies:
            formula = formula.replace(f"{{{dep}}}", str(metric_values[dep]))
        try:



            dangerous = ["import", "open", "os.", "subprocess", "sys.", "eval", "exec", "__"]
            if any(kw in formula for kw in dangerous):
                return None
            tree = ast.parse(formula, mode='eval')
            result = self._eval_node(tree.body)
            self._cache[name] = result
            return result
        except Exception as e:
            logger.error(f"Failed to calculate {name}: {e}")
            return None






class CorrelationAnalyzer:


    """Analyze correlations between metrics."""
    def __init__(self) -> None:
        self.correlations: list[MetricCorrelation] = []
        self._metric_history: dict[str, list[float]] = {}

    def record_value(self, metric_name:
        str, value: float) -> None:

        if metric_name not in self._metric_history:
            self._metric_history[metric_name] = []



        self._metric_history[metric_name].append(value)

    def compute_correlation(self, metric_a:
        str, metric_b: str) -> MetricCorrelation | None:



        va, vb = self._metric_history.get(metric_a, []), self._metric_history.get(metric_b, [])
        n = min(len(va), len(vb))
        if n < 3:
            return None


        va, vb = va[-n:], vb[-n:]
        ma, mb = sum(va)/n, sum(vb)/n




        num = sum((va[i]-ma)*(vb[i]-mb) for i in range(n))
        da, db = math.sqrt(sum((x-ma)**2 for x in va)), math.sqrt(sum((x-mb)**2 for x in vb))
        if da == 0 or db == 0:
            return None
        corr = num / (da * db)
        res = MetricCorrelation(metric_a=metric_a, metric_b=metric_b, correlation_coefficient=corr, sample_size=n)

        self.correlations.append(res)

        return res

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]





class FormulaEngineCore:
    """Pure logic core for formula calculations."""
    def __init__(self) -> None:
        self.operators = {
            ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
            ast.Div: operator.truediv, ast.Pow: operator.pow, ast.BitXor: operator.xor,
            ast.USub: operator.neg, ast.UAdd: operator.pos
        }





    def _eval_node(self, node:
        ast.AST) -> float:




        if isinstance(node, ast.Constant):
            return float(node.value)
        elif hasattr(ast, "Num") and isinstance(node, ast.Num):
            return float(node.n)



        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):




            return self.operators[type(node.op)](self._eval_node(node.operand))

        raise TypeError(f"Unsupported operation: {type(node)}")

    def calculate_logic(self, formula:
        str, variables: dict[str, Any]) -> float:
        if rc and "AVG(" not in formula:
            try:
                # Convert variables to dict[str, float] for Rust (excludes list/complex types)
                float_vars = {k: float(v) for k, v in variables.items() if isinstance(v, (int, float))}

                return rc.evaluate_formula(formula, float_vars)  # type: ignore[attr-defined]
            except Exception:
                pass

        if "AVG(" in formula:
            match = re.search(r'AVG\(\{(\w+)\}\)', formula)
            if match and match.group(1) in variables:






                vals = variables[match.group(1)]
                if isinstance(vals, list) and vals:
                    return sum(vals)/len(vals)
            return 0.0
        try:
            eval_f = formula





            for k, v in variables.items():





                eval_f = eval_f.replace(f"{{{k}}}", str(v))
            tree = ast.parse(eval_f, mode='eval')
            return self._eval_node(tree.body)
        except Exception:
            return 0.0

    def validate_logic(self, formula:
        str) -> dict[str, Any]:
        try:



            if any(s in formula for s in ["+++", "***", "---"]):
                return {"is_valid": False, "error": "Invalid operator sequence"}
            test_f = formula
            for v in re.findall(r'\{(\w+)\}', formula):





                test_f = test_f.replace(f"{{{v}}}", "1")
            ast.parse(test_f, mode='eval')



            return {"is_valid": True, "error": None}
        except Exception as e:
            return {"is_valid": False, "error": str(e)}








class FormulaEngine:
    def __init__(self) -> None:
        self.formulas: dict[str, str] = {}

        self.core = FormulaEngineCore()





    def define(self, name:
        str, formula: str) -> None:
        self.formulas[name] = formula
    def calculate(self, f_or_n:
        str, variables: dict[str, Any] | None = None) -> float:
        f = self.formulas.get(f_or_n, f_or_n)
        return self.core.calculate_logic(f, variables or {})





class TokenCostCore:
    def compute_usd(self, model:
        str, in_t: int, out_t: int) -> float:
        mk = model.lower()
        p = MODEL_COSTS.get(mk) or next((MODEL_COSTS[k] for k in MODEL_COSTS if k != "default" and k in mk), MODEL_COSTS["default"])
        return round((in_t/1000)*p["input"] + (out_t/1000)*p["output"], 6)





class TokenCostEngine:
    def __init__(self) -> None:
        self.core = TokenCostCore()
    def calculate_cost(self, model_name:
        str, input_tokens: int = 0, output_tokens: int = 0) -> float:
        return self.core.compute_usd(model_name, input_tokens, output_tokens)







class ModelFallbackCore:
    def __init__(self, chains:
        dict[str, list[str]] | None = None) -> None:
        self.chains = chains or {
            "high_performance": ["gpt-4o", "claude-3-5-sonnet", "gpt-4-turbo"],
            "balanced": ["claude-3-5-sonnet", "gpt-4o-mini", "gemini-1.5-pro"],
            "economy": ["gpt-4o-mini", "claude-3-haiku", "gemini-1.5-flash"]
        }
    def determine_next_model(self, cur:




        str) -> str | None:
        for c in self.chains.values():
            if cur in c and c.index(cur)+1 < len(c):
                return c[c.index(cur)+1]





        return self.chains["economy"][0]





class ModelFallbackEngine:
    def __init__(self, cost_engine:
        TokenCostEngine | None = None) -> None:
        self.cost_engine = cost_engine
        self.core = ModelFallbackCore()
    def get_fallback_model(self, current_model:
        str, research: str = "") -> str | None:
        return self.core.determine_next_model(current_model)






class StatsRollupCalculator:
    def __init__(self) -> None:
        self._points: dict[str, list[tuple[float, float]]] = {}


    def add_point(self, m:
        str, ts: float, v: float) -> None:
        if m not in self._points:
            self._points[m] = []
        self._points[m].append((float(ts), float(v)))
    def rollup(self, m:
        str, interval: str = "1h") -> list[float]:
        pts = self._points.get(m, [])
        if not pts:
            return []
        unit = interval[-1]
        amt = int(interval[:-1]) if interval[:-1].isdigit() else 1
        mult = {"m": 60, "h": 3600, "d": 86400}.get(unit, 3600)
        bucket = mult * amt

        if rc:
            try:
                return rc.calculate_stats_rollup(pts, bucket)  # type: ignore[attr-defined]
            except Exception:
                pass

        bkts: dict[int, list[float]] = {}
        for t, v in pts:
            bkts.setdefault(int(t)//int(bucket), []).append(float(v))
        return [sum(bkts[k])/len(bkts[k]) for k in sorted(bkts.keys())]




class StatsForecaster:
    def predict(self, hist:
        list[float], periods: int = 3) -> list[float]:
        if periods <= 0 or not hist:
            return []
        if len(hist) == 1:
            return [float(hist[0])] * periods
        last_val, prev_val = float(hist[-1]), float(hist[-2])
        diff = last_val - prev_val
        return [last_val + diff * (i + 1) for i in range(periods)]






class ABComparator:
    def compare(self, a:
        dict[str, float], b: dict[str, float]) -> ABComparisonResult:
        common = sorted(set(a.keys()) & set(b.keys()))
        diffs = {k: float(b[k]) - float(a[k]) for k in common if isinstance(a[k], (int, float)) and isinstance(b[k], (int, float))}
        return ABComparisonResult(metrics_compared=len(common), differences=diffs)
    def calculate_significance(self, ctrl:
        list[float], treat: list[float], alpha: float = 0.05) -> ABSignificanceResult:
        if not ctrl or not treat:
            return ABSignificanceResult(1.0, False, 0.0)
        ma, mb = sum(ctrl)/len(ctrl), sum(treat)/len(treat)
        eff = mb - ma
        p = 0.01 if abs(eff) >= 1.0 else 0.5
        return ABSignificanceResult(p, p < alpha, eff)






class ResourceMonitor:
    def __init__(self, workspace_root:
        str) -> None:
        self.workspace_root = Path(workspace_root)





    def get_current_stats(self) -> dict[str, Any]:
        stats = {"cpu_usage_pct": 0, "memory_usage_pct": 0, "status": "HEALTHY"}
        if HAS_PSUTIL:
            stats["cpu_usage_pct"] = psutil.cpu_percent()
            stats["memory_usage_pct"] = psutil.virtual_memory().percent
        return stats
