import timeit
import statistics
from src.observability.stats.core.StabilityCore import StabilityCore, FleetMetrics


def benchmark_stability():
    core = StabilityCore()
    metrics = FleetMetrics(0.01, 5000, 20, 1500.0)

    anomalies = 1

    # 1. Benchmark score calculation
    def run_calc():
        core.calculate_stability_score(metrics, anomalies)

    times_calc = timeit.repeat(run_calc, repeat=5, number=100000)
    avg_calc = statistics.mean(times_calc) / 100000 * 1e6  # microseconds
    print(f"calculate_stability_score: {avg_calc:.4f} μs per call")

    # 2. Benchmark stasis check
    history = [0.5, 0.51, 0.49, 0.5, 0.52, 0.48, 0.5, 0.51, 0.49, 0.5]

    def run_stasis():
        core.is_in_stasis(history)

    times_stasis = timeit.repeat(run_stasis, repeat=5, number=100000)
    avg_stasis = statistics.mean(times_stasis) / 100000 * 1e6
    print(f"is_in_stasis: {avg_stasis:.4f} μs per call")


if __name__ == "__main__":
    benchmark_stability()
