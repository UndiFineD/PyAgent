import timeit
import statistics
from src.observability.stats.core.tracing_core import TracingCore


def benchmark_tracing():
    core = TracingCore()

    # 1. Benchmark span context creation

    def run_span():
        core.create_span_context("trace-12345", "span-67890")

    times_span = timeit.repeat(run_span, repeat=5, number=100000)
    avg_span = statistics.mean(times_span) / 100000 * 1e6

    print(f"create_span_context: {avg_span:.4f} μs per call")

    # 2. Benchmark latency breakdown
    def run_latency():
        core.calculate_latency_breakdown(1.5, 0.3)

    times_lat = timeit.repeat(run_latency, repeat=5, number=100000)
    avg_lat = statistics.mean(times_lat) / 100000 * 1e6
    print(f"calculate_latency_breakdown: {avg_lat:.4f} μs per call")


if __name__ == "__main__":
    benchmark_tracing()
