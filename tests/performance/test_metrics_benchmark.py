"""Benchmark MetricsCore Python implementation.

This establishes the baseline before Rust conversion.
"""

import time
import random
from src.observability.stats.MetricsCore import (
    TokenCostCore,
    ModelFallbackCore,
    StatsRollupCore,
)


def benchmark_token_cost(iterations: int = 100_000) -> float:
    """Benchmark token cost calculation."""
    core = TokenCostCore()

    input_tokens = 1000

    output_tokens = 500
    model = "gpt-4"

    start = time.perf_counter()

    for _ in range(iterations):
        core.calculate_cost(input_tokens, output_tokens, model)
    elapsed = time.perf_counter() - start

    return elapsed


def benchmark_model_fallback(iterations: int = 100_000) -> float:
    """Benchmark model selection."""
    core = ModelFallbackCore()
    constraints = {"max_cost": 0.5, "required_speed": 0.5, "required_quality": 0.5}

    start = time.perf_counter()
    for _ in range(iterations):
        core.select_best_model(constraints)
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_stats_rollup(iterations: int = 100_000) -> float:
    """Benchmark stats rollup (p95)."""
    core = StatsRollupCore()
    # Ensure stable data for benchmarking
    values = [random.random() * 100 for _ in range(100)]

    start = time.perf_counter()
    for _ in range(iterations):
        core.rollup_p95(values)
    elapsed = time.perf_counter() - start
    return elapsed


if __name__ == "__main__":
    iters = 100_000
    print(f"Running benchmarks ({iters} iterations)...")

    t_cost = benchmark_token_cost(iters)
    print(f"TokenCost: {t_cost:.4f}s ({t_cost / iters * 1e6:.3f} µs/call)")

    t_fallback = benchmark_model_fallback(iters)
    print(f"ModelFallback: {t_fallback:.4f}s ({t_fallback / iters * 1e6:.3f} µs/call)")

    t_stats = benchmark_stats_rollup(iters)
    print(f"StatsRollup (p95): {t_stats:.4f}s ({t_stats / iters * 1e6:.3f} µs/call)")
