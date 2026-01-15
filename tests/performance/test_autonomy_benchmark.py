
import timeit
import statistics
from src.core.base.core.AutonomyCore import AutonomyCore




def benchmark_autonomy():
    core = AutonomyCore("bench_agent")

    # 1. Benchmark blind spots
    def run_blind_spots():
        core.identify_blind_spots(0.65, 0.25)

    times_spots = timeit.repeat(run_blind_spots, repeat=5, number=100000)
    avg_spots = statistics.mean(times_spots) / 100000 * 1e6










    print(f"identify_blind_spots: {avg_spots:.4f} μs per call")

    # 2. Benchmark sleep interval
    def run_sleep():



        core.calculate_daemon_sleep_interval(0.85)

    times_sleep = timeit.repeat(run_sleep, repeat=5, number=100000)
    avg_sleep = statistics.mean(times_sleep) / 100000 * 1e6
    print(f"calculate_daemon_sleep_interval: {avg_sleep:.4f} μs per call")

    # 3. Benchmark plan generation
    spots = ["General_Error", "Rigidity"]
    def run_plan():
        core.generate_self_improvement_plan(spots)


    times_plan = timeit.repeat(run_plan, repeat=5, number=100000)
    avg_plan = statistics.mean(times_plan) / 100000 * 1e6
    print(f"generate_self_improvement_plan: {avg_plan:.4f} μs per call")





if __name__ == "__main__":
    benchmark_autonomy()
