import timeit
from src.core.base.core.ResilienceCore import ResilienceCore


def benchmark_resilience():
    # Measure calculate_backoff (full jitter)
    def run_backoff():
        ResilienceCore.calculate_backoff(
            failure_count=5,
            threshold=3,
            base_timeout=1.0,
            multiplier=2.0,
            max_timeout=60.0,
            jitter_mode="full",
        )

    t_backoff = timeit.timeit(run_backoff, number=100000)
    print(f"calculate_backoff: {t_backoff / 100000 * 1_000_000:.4f} μs per call")

    # Measure should_attempt_recovery
    def run_recovery():
        ResilienceCore.should_attempt_recovery(1000.0, 1061.0, 60.0)

    t_rec = timeit.timeit(run_recovery, number=100000)
    print(f"should_attempt_recovery: {t_rec / 100000 * 1_000_000:.4f} μs per call")

    # Measure evaluate_state_transition
    def run_transition():
        ResilienceCore.evaluate_state_transition("CLOSED", 0, 5, 4, 5)

    t_trans = timeit.timeit(run_transition, number=100000)
    print(f"evaluate_state_transition: {t_trans / 100000 * 1_000_000:.4f} μs per call")


if __name__ == "__main__":
    benchmark_resilience()
