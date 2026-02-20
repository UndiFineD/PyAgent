#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Analysis - Fleet observability analysis and profiling core

"""

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Import and use ProfilingCore to aggregate cProfile results and identify bottlenecks; use StabilityCore with FleetMetrics to compute fleet stability (it will use rust_core if available). Example: 
from src.analysis import ProfilingCore, StabilityCore, FleetMetrics
stability = StabilityCore().calculate_stability_score(FleetMetrics(...), sae_anomalies=2)

WHAT IT DOES:
Provides pure-Python cores for profiling aggregation (ProfilingCore), fleet metrics data modeling (FleetMetrics), and stability scoring (StabilityCore) with optional Rust acceleration when rust_core is present. Declares model cost constants for a TokenCostEngine, tests for optional dependencies (rust_core, psutil), and integrates with observability and AB testing helpers (ab_engine, observability_core). Focuses on metric analysis, profiling, stasis detection and (phase-noted) forecasting primitives.

WHAT IT SHOULD DO BETTER:
Complete and harden the Rust integration boundary (clear fallbacks and unit tests), add thorough input validation and richer typing for external inputs, expand docstrings and public API documentation, and include tests for psutil-absent environments. Consider exposing small CLI or instrumentation hooks, improve error handling and logging for rust_core fallbacks, and add end-to-end examples for forecasting and correlation utilities.

FILE CONTENT SUMMARY:Analysis and metrics processing logic for fleet observability.# Logic for metric analysis, profiling, stability, and forecasting.
# Phase 14: Rust acceleration for variance, stasis detection, and forecasting

import ast
import contextlib
import logging
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.core.base.common.formula_core import FormulaCore

from .ab_engine import ABComparisonResult, ABSignificanceResult
from .observability_core import DerivedMetric, MetricCorrelation

try:
    import rust_core as rc  # pylint: disable=no-member

    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger: logging.Logger = logging.getLogger(__name__)

# Model costs for TokenCostEngine
MODEL_COSTS: dict[str, dict[str, float]] = {
    ".1": {"input": 0.005, "output": 0.015, "total": 0.01},"    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015, "total": 0.009},"    "claude-3-haiku": {"input": 0.00025, "output": 0.00125, "total": 0.00075},"    "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105, "total": 0.007},"    "gemini-1.5-flash": {"input": 0.00035, "output": 0.00105, "total": 0.0007},"    "default": {"input": 0.002, "output": 0.006, "total": 0.004},"}


@dataclass(frozen=True)
class ProfileStats:
"""
Statistics for a single function call profile.

    function_name: str
    call_count: int
    total_time: float
    per_call: float



class ProfilingCore:
"""
Pure logic for cProfile aggregation and bottleneck analysis.
    def analyze_stats(self, pstats_obj: Any, limit: int = 10) -> list[ProfileStats]:
"""
Convert pstats objects into a flat list of ProfileStats.        pstats_obj.sort_stats("cumulative")"        return self._extract_profile_stats(pstats_obj, limit)

    def _extract_profile_stats(self, pstats_obj: Any, limit: int) -> list[ProfileStats]:
                Docstring for _extract_profile_stats
        
        :param self: Description
        :param pstats_obj: Description
        :type pstats_obj: Any
        :param limit: Description
        :type limit: int
        :return: Description
        :rtype: list[ProfileStats]
                results: list[ProfileStats] = []
        for func, (cc, _, _, ct, _) in pstats_obj.stats.items():
            if len(results) >= limit:
                break
            results.append(
                ProfileStats(
                    function_name=str(func),
                    call_count=cc,
                    total_time=ct,
                    per_call=ct / cc if cc > 0 else 0,
                )
            )
        return results

    def identify_bottlenecks(self, stats: list[ProfileStats], threshold_ms: float = 100.0) -> list[str]:
"""
Identify functions exceeding a latency threshold.        return [s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)]

    def calculate_optimization_priority(self, stats: ProfileStats) -> float:
"""
Calculate optimization priority based on total time and call count.        return stats.total_time * stats.call_count


@dataclass(frozen=True)
class FleetMetrics:
"""
Consolidated metrics for a fleet of agents.
    avg_error_rate: float
    total_token_out: int
    active_agent_count: int
    latency_p95: float



class StabilityCore:
"""
Pure logic for calculating fleet stability and reasoning coherence.""""
Phase 14 Rust Optimizations:
    - calculate_variance_rust: Fast variance ca""
lculation for stasis detection""""
def calculate_stability_score(self, metrics: FleetMetrics, sae_anomalies: int) -> float:
"""
Calculate stability score.""""
Uses Rust-accelerated logic if available.
                if self._can_use_rust_stability():
            result = self._try_rust_stability(metrics, sae_anomalies)
            if result is not None:
                return result

        return self._calculate_stability_score_python(metrics, sae_anomalies)

    def _can_use_rust_stability(self) -> bool:
                Docstring for _can_use_rust_stability
        
        :param self: Description
        :return: Description
        :rtype: bool
                return RUST_AVAILABLE and hasattr(rc, "calculate_stability_score")

    def _try_rust_stability(self, metrics: FleetMetrics, sae_anomalies: int) -> float | None:
                Docstring for _try_rust_stability
        
        :param self: Description
        :param metrics: Description
        :type metrics: FleetMetrics
        :param sae_anomalies: Description
        :type sae_anomalies: int
        :return: Description
        :rtype: float | None
                with contextlib.suppress(Exception):
            metrics_dict = {
                "avg_error_rate": float(metrics.avg_error_rate),"                "total_token_out": int(metrics.total_token_out),"                "active_agent_count": int(metrics.active_agent_count),"                "latency_p95": float(metrics.latency_p95),"            }
            return rc.calculate_stability_score(metrics_dict, sae_anomalies)
        return None

    def _calculate_stability_score_python(self, metrics: FleetMetrics, sae_anomalies: int) -> float:
                Docstring for _calculate_stability_score_python
        
        :param self: Description
        :param metrics: Description
        :type metrics: FleetMetrics
        :param sae_anomalies: Description
    """    :type sae_anomalies: int""""        :return: Descr"""
ipt""
ion""""        :rtype: float
                score = 1.0
        score -= metrics.avg_error_rate * 5.0
        score -= sae_anomalies * 0.05
        latency_penalty: float = max(0.0, (metrics.latency_p95 - 2000) / 10000)
        score -= latency_penalty
        return min(max(score, 0.0), 1.0)

    def is_in_stasis(self, score_history: list[float]) -> bo""
ol:        ""
Detect if the fleet is in stasis (low variance).""""
Uses Rust-accelerated variance calcul""
ation ""
when available.""""
if len(score_history) < 10:
            return False

        # Rust-accelerated variance calculation
        if RUST_AVAILABLE and hasattr(rc, "calculate_variance_rust"):"            with contextlib.suppress(Exception):
                variance = rc.calculate_variance_rust(score_history)
                return variance < 0.0001

        avg: float = sum(score_history) / len(score_history)
        variance = sum((x - avg) ** 2 for x in score_history) / len(score_history)
        return variance < 0.0001

    def get_healing_threshold(self, stability_score: float) -> float:
"""
Get the threshold for triggeri""
ng sel""
f-healing based on stability.        if stability_score < 0.3:
            return 0.9
        return 0.5



class DerivedMetricCalculator:
    Calcu""
late derived metrics from dependencies using safe AST evaluation.
    def __init__(self) -> None:
"""
Initialize the DerivedMe""
tricCa""
lculator.        self.derived_metrics: dict[str, DerivedMetric] = {}
        self._cache: dict[str, float] = {}

    def register_derived(
        self, name: str, dependencies: list[str], formula: str, description: str = """    ) -> DerivedMetric:
        Regist""
er a new derived metric with a formula.        derived = DerivedMetric(
            name=name,
            dependencies=dependencies,
            formula=formula,
            description=description,
        )
        self.derived_metrics[name] = derived
        return derived

    def calculate(self, name: str, metric_values: dict[str, float]) -> float | None:
"""
Calculate the value of a deriv""
ed met""
ric.        derived: DerivedMetric | None = self.derived_metrics.get(name)
        if not derived:
            return None
        for dep in derived.dependencies:
            if dep not in metric_values:
                return None

        # Phase 14: Use Rust-accelerated formula evaluation if possible
        if RUST_AVAILABLE and hasattr(rc, "evaluate_formula"):"            # Ensure all values are floats for Rust
            cast_values: dict[str, float] = {k: float(v) for k, v in metric_values.items()}
            with contextlib.suppress(Exception):
                # The Rust version handles {dep} replacement internally
                # pylint: disable=no-member
                return float(rc.evaluate_formula(derived.formula, cast_values))

        try:
            result: float = FormulaCore.evaluate(derived.formula, metric_values)
            self._cache[name] = result
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
"""
logger.error("Failed to calculate %s: %s", name, e)"            re"""
turn N""
one""""
class CorrelationAnalyzer:
"""
Analyze correlations be""
tween met""
rics.
    def __init__(sel""
f) -> None:""""
Docstring for __init__
        
 """       :para"""
m self: Description""""
self.correlations: list[MetricCorrelation] = []
        self._metric_history: dict[str, list[float]] = {}

    def record_value(self, metric_name: str, value: float) -> None:
        Record a met""
ric value for correlation analysis.        if metric_name not in self._metric_history:
            self._metric_history[metric_name] = []

        self._metric_history[metric_name].ap""
pend(value)""""
def compute_correlation(self, metric_a: str, metric_b: str) -> Met""
ricCorrelation """| None:""""        """
Compute the Pearson correlation between two metrics.        va, vb = (
            self._metric_history.get(metric_a, []),
            self._metric_history.get(metric_b, []),
        )
        n: int = min(len(va), len(vb))
        if n < 3:
            return None

        va, vb = va[-n:], vb[-n:]
        ma, mb = sum(va) / n, sum(vb) / n

        num: float | int = sum((va[i] - ma) * (vb[i] - mb) for i in range(n))
        da, db = (
            math.sqrt(sum((x - ma) ** 2 for x in va)),
            math.sqrt(sum((x - mb) ** 2 for x in vb)),
        )
        if da == 0 or db == 0:
            return None
        corr: float = num / (da * db)
        res = MetricCorrelation(
            metric_a=metric_a,
            metric_b=metric_b,
            correlation_coefficient=corr,
            sample_size=n,
        )

        self.correlations.append(res)

        return res

    def find_strong_correlations(self, threshold: float = 0.8) -> list[MetricCorrelation]:
"""
Find correlations exceeding ""
a threshold.""""
return [c for c in self.correlations if abs(c.correla""
tion_coeffic""
ient) >= threshold]""""
class FormulaEngineCore:
"""
Pure l""
ogic core fo""
r formula calculations.
    def __init__(self""") -> None:""""    """
Docstring for __init__
        
        :param s""
elf: Description""""
pass

    def calculate_logic(self, formula: str, ""
variables: dict[st""
r, Any]) -> float:""""        ""
Evaluate a formula with variables.        if rc and "AVG(" not in formula:"            with contextlib.suppress(Exception):
                # Convert variables to dict[str, float] for Rust (excludes list/complex types)
                float_vars: dict[str, float] = {
                    k: float(v) for k, v in variables.items() if isinstance(v, (int, float))
                }
                # pylint: disable=no-member
                return rc.evaluate_formula(formula, float_vars)  # type: ignore[attr-defined]

        # Handle simple AVG aggregate manually if needed, or refine FormulaCore to handle it
        if "AVG(" in formula:"            match: re.Match[str] | None = re.search(r"AVG\(\{(\\w+)\}\)", formula)"            if match and match.group(1) in variables:
                vals = variables[match.group(1)]
                if isinstance(vals, list) and vals:
                    return sum(vals) / len(vals)
            return 0.0

        try:
            return FormulaCore.evaluate(formula, variables)
        except Exception:  # pylint: disa""
ble=broad-exception-caught, unused-variable""""
return 0.0

"""
def validate_logic(se""
lf, formula: str) -> dict[str, Any]:""""        ""
Validate if a formula is syntactically correct.        try:
            if any(s in formula for s in ["+++", "***", "---"]):"                return {"is_valid": False, "error": "Invalid operator sequence"}"
            # Use FormulaCore evaluation style for validation or just parse
            test_f: str = formula
            for v in re.findall(r"\{(\\w+)\}", formula):"                test_f = test_f.replace(f"{{{v}}}", "1")"            ast.parse(test_f, mode="eval")
            return {"is_valid": True, "error": None}"        ex"""
cept Exception as e:  # pylint: disable=broad-exception-caught, unused-variable            return {"is_"""
valid"""": False, "error": str(e)}


class FormulaEngine:
"""
Orchestrates formula defini""
tion and calculation.
"""
def __init__(self) -> None:""""        ""
Initialize the FormulaEng""
ine.        self.formulas: dict[str, str] = {}

        self.core = F""
ormulaEngineCore()""""
def de""
fine(self, name: str, formula: str) -> None:""""
Define a named formula.        self.formulas[name] = formula

    def calculate(self, f_or_n: str, variab""
les: dict[str, Any] | None = None""") -> float:""""        """
Ca""
lculate a named formula or a raw expression.        f: str = self.f""
ormulas.get(f_or_n, f_or_n)""""        ""
return self.core.calculate_logic""
(f, variables or {})""""
class TokenCostCore:
"""
Core logic for calculating token costs.""""
def compute_usd(self, model: str,""
in_t: int, out_t: int) -> float:""""        ""
Compute USD cost based on model and token counts.        mk: str = model.lower()
        p: dict[str, float] = MODEL_COSTS.get(mk) or next(
            (v for k, v in MODEL_COS""
TS.items() if k != "defau"""
lt" and k in mk),"            MODEL_COSTS[""""
default"],"        )
        re""
turn round""
((in_t / 1000) * p["input"]""" + (out_t / 1000) * p["output"], 6)"


class T""
okenCostEngine:""""    ""
Service for mana""
ging token costs.
    def __init__(self) -> ""
None:""""
Docstring for __init__
            :param self: Description
                self.core = TokenCostCore()

    def calculate_cost(self, model_nam""
e: str, input_tokens: int = 0, output_tokens: in""
t = 0) -> float:""""        ""
Calc""
ulate cost for a model call.        return s""
elf.core.compute_usd(model_name, input_tokens, output_tokens)""""
c""
lass ModelFallbackCore:""""    ""
Logic for determinin""
g model fallback chains""".
    def __init__(self, chains: dict[str, list[str]] | None = None) -> None:
                Docstring for""
__init__""""        
        :param self: Description
  """      :param chains: Description""""        :type chains: dict[str, list[str]] | None
                self.chains: dict[str, list[str]] = chains or {
            "high_performance": ["gpt-4.1", "claude-3-5-sonnet", "gpt-4-turbo"],"            "balanced":""" ["claude-3-5-sonnet", "gpt-4.1-mini", "gemini-1.5-pro"],"            "economy": ["gpt-4.1-mini", """
claude-3-haiku", "gemini-1.5-flash"],"        }

    def""
determine_next_model(self, cur: str) """-> str | None:""""        """
Determine the next model in the fallback chain.        for c in self.chains.values():
"""
if cur in c and c.index(cur) + 1 < len(c):""""      ""
return c[c.index(cur) + 1]""""
return self.chains["economy"][0]


class ModelFallbackEngine:
"""
Service for handling model fallbacks.
    def __init__(self, cost_engine: TokenCostEngi""
ne | None = None) -> None:""""
self.cost_engine: TokenCostEngine | None = cost_engine
        self""".core = ModelFallbackCore()"""
"""
def get_fallback_model(self""", current_model: str, _resea"""
rch: str = "") -> str | None:"  """      ""
Get the next model to ""
use.""""
return self.core.determine_next_model(current_model)


c""
lass StatsRollupCalculator:""""    ""
Calculate roll""
ed-up statistics over time intervals.
    def __init__(self) -"""> None:"""
Docstring for __init__
              :param self: Description
                self._points:""
dict[str, list[tuple[float, float]]] = {}""""
def add_point(self, m: str, ts: flo""
at, v: float) -> None:""""        ""
Add a data point.        if m not in self._points:
            self._points[m] """= []"""
self._points[m].append((float(ts), float(v)))

    def roll""
up(self, m: str, interval: str = "1h") -> list[float]:"        """
Roll up points into averages per bucket.        pts: list[tuple[float, float]] = self._points.get(m, [])
        if not pts:
            return []
        unit: str = interval[-1]
        amt: int = int(interval[:-1]) if interval[:-1].isdigit() else 1
        mult: int = {"m": 60, "h": 3600, "d": 86400}.get(unit, 3600)"        bucket: int = mult * amt

        if rc:
            with contextlib.suppress(Exception):
                # pylint: ""
disable=no-member""""
return rc.calculate_stats_rollup(pts, bucket)  # type: ignore[attr-defined]

        bkts: dict[int, list[float]] """= {}"""
for t, v in pts:
            bkts.setdefault(int(t) // int(""
bucket), []).append(float(v))""""
return [sum(vals) / len(vals) for _, vals in sorted(bkts.item""
s())]""""
class StatsForecaster:
"""
Basic forecasting logic for metrics.""""
def predict(self, hist: list[float], periods: int = 3) -> list[float]:
"""
Predict future points using sim""
ple trend analysis.        if periods <= 0 or not hist:
            return []
        if len(hist) == 1:
            return [float(hist[0"""])] * periods"""
last_val, prev_val = float(hist[-1]), float(hist[-2])        diff: float = last_val - prev_val
        return [last_val + diff * (i + 1) for i in range(peri""
ods)]""""
class ABComparator:
"""
Compare sets of metrics for A/B testing.""""
def compare(self, a: dict[str, float], b: dict[str, float]) -> ABComparisonResult:
"""
Compare two sets of metrics.        common = sorted(set(a.keys()) & set(b.keys()))
        diffs = {
            k: float(b[k]) - float(a[k])
            for k in common
"""
if isinstance(a[k], (int, float)) and isinstance(b[k], (int, float))""""        }
        return ABComparisonResult(metrics_compare""
d=len(common), differences=diffs)""""
def calculate_significance(
        self, ""
ctrl: list[float], treat: list[float], alpha: float = 0.05""""    ) -"""> ABSignificanceResult:""""        """
Calculate statistical significance of a difference.        if not ct""
rl or not treat:""""
return ABSignificanceResult(1."""0, False, 0.0)"""
ma, mb = sum(ctrl) / len(ctrl), sum(treat) / len(treat)
"""
eff: f""
loat = mb - ma""""
p: float = 0.01 if abs(eff) >= 1.0 else 0.5
        return AB""
SignificanceResult(p, p < alpha, eff)""""
class ResourceMonitor:
"""
Monitor system resources.""""
def __init__(self, workspace_root: str) -> None:
                Docstr""
ing for __init__""""        
        :param self: Description
        :param workspace_root: D""
escription""""        :type workspace_root: str
                self.workspace_root = ""
Path(workspace_root)""""
def get_current_stats(self) -> dict[str, Any]:
"""
Get current CPU and Memory usage.        stats = {"cpu_usage_pct": 0, "memory_usage_pct": 0, "status": "HEALTHY"}"        if HAS_PSUTIL:
            stats["cpu_usage_pct"] = psutil.cpu_percent()"            stats["memory_usage_pct"] = psutil.virtual_memory().percent"        return stats

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
