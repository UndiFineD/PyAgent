#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""MetricsCore - Pure calculation logic for metrics processing.

This module contains all pure computational logic without I/O operations,
making it a candidate for Rust conversion. It handles:
- Token cost calculations
- Metric aggregation and rollup
- Formula evaluation and derived metrics
- Correlation analysis
- Statistical forecasting
- A/B comparison analysis

No I/O operations, no file access, no external calls.
"""

from __future__ import annotations

import contextlib
import logging
import math
from dataclasses import dataclass
from typing import Any, Tuple

from src.core.base.common.formula_core import FormulaCore

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class TokenCostResult:
    """Result of token cost calculation."""

    total_cost: float
    input_cost: float
    output_cost: float
    currency: str = "USD"


class TokenCostCore:
    """Pure token cost calculation (Rust-convertible).

    Calculates costs based on model pricing without I/O.
    """

    # Model pricing (cost per 1M tokens)
    MODEL_COSTS: dict[str, dict[str, float]] = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105},
        "llama-2-70b": {"input": 0.0008, "output": 0.001},
    }

    def __init__(self) -> None:
        """Initialize token cost calculator."""
        self.cache: dict[Tuple[int, int, str], TokenCostResult] = {}

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "gpt-3.5-turbo") -> TokenCostResult:
        """Calculate total cost for token usage (pure calculation).

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model name for pricing lookup

        Returns:
            TokenCostResult with cost breakdown
        """
        # optimized using Rust if available
        if rc:
            try:
                # pylint: disable=no-member
                # Returns (total_cost, input_cost, output_cost)
                total, i_cost, o_cost = rc.calculate_token_cost(input_tokens, output_tokens, model)
                return TokenCostResult(
                    total_cost=total,
                    input_cost=i_cost,
                    output_cost=o_cost,
                    currency="USD",
                )
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust calculate_token_cost failed: %s. Falling back to Python.", e)
                import traceback
                traceback.print_exc()

        # check cache
        cache_key: Tuple[int | str] = (input_tokens, output_tokens, model)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # get pricing
        pricing: dict[str, float] = self.MODEL_COSTS.get(model, self.MODEL_COSTS["gpt-3.5-turbo"])

        # calculate costs (convert from cost per 1M to per token)
        input_cost: float = (input_tokens * pricing["input"]) / 1_000_000
        output_cost: float = (output_tokens * pricing["output"]) / 1_000_000
        total_cost: float = input_cost + output_cost

        result = TokenCostResult(
            total_cost=total_cost,
            input_cost=input_cost,
            output_cost=output_cost,
            currency="USD",
        )

        # cache result
        self.cache[cache_key] = result
        return result

    def estimate_cost_per_token(self, model: str) -> dict[str, float]:
        """Estimate cost per single token (pure calculation).

        Args:
            model: Model name

        Returns:
            Dict with input and output cost per token
        """
        pricing: dict[str, float] = self.MODEL_COSTS.get(model, self.MODEL_COSTS["gpt-3.5-turbo"])
        return {
            "input": pricing["input"] / 1_000_000,
            "output": pricing["output"] / 1_000_000,
        }


class ModelFallbackCore:
    """Pure logic for model selection and fallback (Rust-convertible)."""

    def __init__(self) -> None:
        """Initialize model fallback engine."""
        self.model_capabilities: dict[str, dict[str, float]] = {
            "gpt-4": {"speed": 0.5, "quality": 1.0, "cost": 0.1},
            "gpt-4-turbo": {"speed": 0.7, "quality": 0.95, "cost": 0.3},
            "gpt-3.5-turbo": {"speed": 0.9, "quality": 0.7, "cost": 0.8},
            "claude-3-opus": {"speed": 0.6, "quality": 0.98, "cost": 0.15},
            "gemini-1.5-pro": {"speed": 0.8, "quality": 0.85, "cost": 0.4},
        }

    def select_best_model(self, constraints: dict[str, float]) -> str:
        """Select best model given constraints (pure logic).

        Args:
            constraints: Dict with max_cost, required_speed, required_quality

        Returns:
            Selected model name
        """
        if rc:
            try:
                # pylint: disable=no-member
                return rc.select_best_model(constraints)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust select_best_model failed: %s. Falling back to Python.", e)
                import traceback
                traceback.print_exc()

        max_cost: float = constraints.get("max_cost", 1.0)
        required_speed: float = constraints.get("required_speed", 0.0)
        required_quality: float = constraints.get("required_quality", 0.0)

        candidates = []
        for model, caps in self.model_capabilities.items():
            if caps["cost"] <= max_cost and caps["speed"] >= required_speed and caps["quality"] >= required_quality:
                score: float = (caps["speed"] * 0.3) + (caps["quality"] * 0.5) + ((1 - caps["cost"]) * 0.2)
                candidates.append((model, score))

        if not candidates:
            return "gpt-3.5-turbo"  # Fallback

        return max(candidates, key=lambda x: x[1])[0]

    def get_fallback_chain(self, primary: str) -> list[str]:
        """Get fallback model chain (pure logic).

        Args:
            primary: Primary model

        Returns:
            List of models in fallback order
        """
        if rc:
            try:
                # pylint: disable=no-member
                return rc.get_fallback_chain(primary)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust get_fallback_chain failed: %s. Falling back to Python.", e)
                import traceback
                traceback.print_exc()

        fallback_chains: dict[str, list[str]] = {
            "gpt-4": ["gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus"],
            "gpt-4-turbo": ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],
            "claude-3-opus": ["claude-3-sonnet", "gpt-4-turbo", "gemini-1.5-pro"],
            "gpt-3.5-turbo": ["claude-3-haiku", "gemini-1.5-pro"],
        }
        return fallback_chains.get(primary, list(self.model_capabilities.keys()))


class DerivedMetricCalculator:
    """Calculate derived metrics from dependencies (pure calculation)."""

    def __init__(self) -> None:
        """Initialize calculator."""

    def calculate(self, metric_name: str, context: dict[str, float]) -> float:
        """Calculate derived metric value."""
        if metric_name not in self.derived_metrics:
            raise KeyError(f"Derived metric {metric_name} not found")

        metric_def = self.derived_metrics[metric_name]
        formula: Any | str = getattr(metric_def, "formula", metric_def) if not isinstance(metric_def, str) else metric_def

        return self.evaluate_formula(formula, context)

    def get_all_derived(self, context: dict[str, float]) -> dict[str, float]:
        """Calculate all derived metrics."""
        results = {}
        for name in self.derived_metrics:
            with contextlib.suppress(Exception):
                results[name] = self.calculate(name, context)
        return results

    def register_derived(self, name: str, dependencies: list[str], formula: str) -> Any:
        """Register a derived metric definition."""
        # pylint: disable=import-outside-toplevel
        from src.observability.stats.observability_core import DerivedMetric

        metric = DerivedMetric(name=name, dependencies=dependencies, formula=formula)
        self.derived_metrics[name] = metric
        return metric

    def evaluate_formula(self, formula: str, values: dict[str, float]) -> float:
        """Evaluate a formula with given values (pure calculation)."""
        if rc:
            try:
                # pylint: disable=no-member
                return rc.evaluate_formula(formula, values)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust evaluate_formula failed: %s. Falling back to Python.", e)
                import traceback
                traceback.print_exc()

        return FormulaCore.evaluate(formula, values)


class StatsRollupCore:
    """Pure statistics rollup calculations (Rust-convertible)."""

    def __init__(self) -> None:
        """Initialize stats rollup."""

    def rollup_sum(self, values: list[float]) -> float:
        """Calculate sum of values (pure calculation)."""
        # Use high-precision summation to avoid catastrophic cancellation.
        # Prefer Python's math.fsum which provides better precision than sum().
        if values:
            try:
                return math.fsum(values)
            except Exception:
                return sum(values)
        return 0.0

    def rollup_avg(self, values: list[float]) -> float:
        """Calculate average (pure calculation)."""
        if not values:
            return 0.0
        # Use math.fsum for robust summation
        total = math.fsum(values)
        return total / len(values)

    def rollup_min(self, values: list[float]) -> float:
        """Calculate minimum (pure calculation)."""
        if rc:
            with contextlib.suppress(Exception):
                # pylint: disable=no-member
                return rc.calculate_min_rust(values)  # type: ignore[attr-defined]
        return min(values) if values else 0.0

    def rollup_max(self, values: list[float]) -> float:
        """Calculate maximum (pure calculation)."""
        if rc:
            with contextlib.suppress(Exception):
                # pylint: disable=no-member
                return rc.calculate_max_rust(values)  # type: ignore[attr-defined]
        return max(values) if values else 0.0

    def rollup_p50(self, values: list[float]) -> float:
        """Calculate 50th percentile (median) (pure calculation)."""
        if rc:
            with contextlib.suppress(Exception):
                # pylint: disable=no-member
                return rc.calculate_median_rust(values)  # type: ignore[attr-defined]
        if not values:
            return 0.0
        sorted_vals: list[float] = sorted(values)
        idx: int = len(sorted_vals) // 2
        return sorted_vals[idx] if len(sorted_vals) % 2 == 1 else (sorted_vals[idx - 1] + sorted_vals[idx]) / 2

    def rollup_p95(self, values: list[float]) -> float:
        """Calculate 95th percentile (pure calculation)."""
        if rc:
            try:
                # pylint: disable=no-member
                return rc.calculate_p95_rust(values)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust calculate_p95_rust failed: %s. Falling back to Python.", e)
                import traceback
                traceback.print_exc()

        if not values or len(values) < 20:
            return self.rollup_max(values)
        sorted_vals: list[float] = sorted(values)
        idx = int(len(sorted_vals) * 0.95)
        return sorted_vals[idx]

    def rollup_p99(self, values: list[float]) -> float:
        """Calculate 99th percentile (pure calculation)."""
        if not values or len(values) < 100:
            return self.rollup_max(values)
        sorted_vals: list[float] = sorted(values)
        idx = int(len(sorted_vals) * 0.99)
        return sorted_vals[idx]

    def rollup_stddev(self, values: list[float]) -> float:
        """Calculate standard deviation (pure calculation)."""
        if rc:
            with contextlib.suppress(Exception):
                # pylint: disable=no-member
                return rc.calculate_stddev_rust(values)  # type: ignore[attr-defined]
        if len(values) < 2:
            return 0.0
        mean: float = self.rollup_avg(values)
        variance: float = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)


class CorrelationCore:
    """Pure correlation analysis (Rust-convertible)."""

    def calculate_correlation(self, series1: list[float], series2: list[float]) -> float:
        """Calculate Pearson correlation coefficient (pure calculation).

        Args:
            series1: First data series
            series2: Second data series

        Returns:
            Correlation coefficient (-1.0 to 1.0)
        """
        if rc:
            with contextlib.suppress(Exception):
                # pylint: disable=no-member
                return rc.calculate_pearson_correlation_rust(series1, series2)  # type: ignore[attr-defined]

        if len(series1) != len(series2) or len(series1) < 2:
            return 0.0

        mean1: float = sum(series1) / len(series1)
        mean2: float = sum(series2) / len(series2)

        numerator: float | int = sum((x - mean1) * (y - mean2) for x, y in zip(series1, series2))
        denom1: float = math.sqrt(sum((x - mean1) ** 2 for x in series1))
        denom2: float = math.sqrt(sum((y - mean2) ** 2 for y in series2))

        if denom1 == 0 or denom2 == 0:
            return 0.0

        return numerator / (denom1 * denom2)


class ABTestCore:
    """Pure A/B testing calculations (Rust-convertible)."""

    def calculate_significance(self, control_values: list[float], treatment_values: list[float]) -> dict[str, float]:
        """Calculate statistical significance (pure calculation).

        Uses simplified t-test approach.

        Args:
            control_values: Control group values
            treatment_values: Treatment group values

        Returns:
            Dict with p_value, t_statistic, effect_size
        """
        if rc:
            try:
                # pylint: disable=no-member
                return rc.calculate_statistical_significance(
                    control_values, treatment_values
                )  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust calculate_statistical_significance failed: %s. Using Python fallback.", e)
                import traceback
                traceback.print_exc()

        if not control_values or not treatment_values:
            return {"p_value": 1.0, "t_statistic": 0.0, "effect_size": 0.0}

        control_mean: float = sum(control_values) / len(control_values)
        treatment_mean: float = sum(treatment_values) / len(treatment_values)

        control_var: float = sum((x - control_mean) ** 2 for x in control_values) / len(control_values)
        treatment_var: float = sum((x - treatment_mean) ** 2 for x in treatment_values) / len(treatment_values)

        pooled_se: float = math.sqrt((control_var / len(control_values)) + (treatment_var / len(treatment_values)))
        t_stat: float | int = (treatment_mean - control_mean) / pooled_se if pooled_se > 0 else 0

        effect_size: float | int = (
            (treatment_mean - control_mean) / math.sqrt(max(control_var, treatment_var))
            if max(control_var, treatment_var) > 0
            else 0
        )

        return {
            "p_value": 0.05 if abs(t_stat) > 2 else 0.95,  # Simplified
            "t_statistic": t_stat,
            "effect_size": effect_size,
        }

    def calculate_sample_size(self, effect_size: float, alpha: float = 0.05, power: float = 0.8) -> int:
        """Calculate required sample size (pure calculation).

        Args:
            effect_size: Expected effect size (Cohen's d)
            alpha: Type I error rate
            power: Statistical power (1 - beta)

        Returns:
            Required sample size per group
        """
        if rc:
            try:
                # pylint: disable=no-member
                return rc.calculate_sample_size(effect_size, alpha, power)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust calculate_sample_size failed: %s. Falling back to Python.", e)
                import traceback
                traceback.print_exc()

        # Simplified formula: n = 2 * (z_alpha + z_beta)^2 / effect_size^2
        z_alpha = 1.96  # For alpha=0.05
        z_beta = 0.84  # For power=0.8

        if effect_size == 0:
            return 1000000

        return int(2 * ((z_alpha + z_beta) ** 2) / (effect_size**2))
