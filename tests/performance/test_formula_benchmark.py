"""Benchmark FormulaEngineCore Python implementation.

This establishes the baseline before Rust conversion.
"""

import time
from src.observability.stats.metrics_engine import FormulaEngineCore


def benchmark_simple_operation(iterations: int = 10000) -> float:
    """Benchmark simple arithmetic formula."""
    core = FormulaEngineCore()
    formula = "{x} + {y}"
    variables = {"x": 10.0, "y": 20.0}
    
    start = time.perf_counter()
    for _ in range(iterations):
        core.calculate_logic(formula, variables)
    elapsed = time.perf_counter() - start
    
    return elapsed


def benchmark_complex_operation(iterations: int = 10000) -> float:
    """Benchmark complex formula with multiple operations."""
    core = FormulaEngineCore()
    formula = "({x} * {y}) + ({z} / {w})"
    variables = {"x": 10.0, "y": 20.0, "z": 100.0, "w": 5.0}
    
    start = time.perf_counter()
    for _ in range(iterations):
        core.calculate_logic(formula, variables)
    elapsed = time.perf_counter() - start
    
    return elapsed


def benchmark_validation(iterations: int = 10000) -> float:
    """Benchmark formula validation."""
    core = FormulaEngineCore()
    formula = "{x} + {y} * {z}"
    
    start = time.perf_counter()
    for _ in range(iterations):
        core.validate_logic(formula)
    elapsed = time.perf_counter() - start
    
    return elapsed


if __name__ == "__main__":
    print("FormulaEngineCore Python Benchmark")
    print("=" * 50)
    
    # Warmup
    benchmark_simple_operation(100)
    
    # Simple operation benchmark
    iterations = 10000
    elapsed = benchmark_simple_operation(iterations)
    per_call = (elapsed * 1_000_000) / iterations
    print(f"Simple operation ({iterations} iterations): {elapsed:.4f}s")
    print(f"  → {per_call:.2f} microseconds per call")
    
    # Complex operation benchmark
    elapsed = benchmark_complex_operation(iterations)
    per_call = (elapsed * 1_000_000) / iterations
    print(f"\nComplex operation ({iterations} iterations): {elapsed:.4f}s")
    print(f"  → {per_call:.2f} microseconds per call")
    
    # Validation benchmark
    elapsed = benchmark_validation(iterations)
    per_call = (elapsed * 1_000_000) / iterations
    print(f"\nValidation ({iterations} iterations): {elapsed:.4f}s")
    print(f"  → {per_call:.2f} microseconds per call")
    
    print("\n" + "=" * 50)
    print("Note: Rust version should be 10-50x faster")
    print("Expected Rust performance:")
    print("  Simple: 0.01-0.5 microseconds per call")
    print("  Complex: 0.02-0.5 microseconds per call")
