
import timeit
from src.core.base.core.ConvergenceCore import ConvergenceCore




def benchmark_convergence():
    core = ConvergenceCore("/tmp")
    # Setup data
    small_fleet = {f"Agent_{i}": True for i in range(10)}
    mixed_fleet = {f"Agent_{i}": i % 2 == 0 for i in range(100)}


    large_fleet = {f"Agent_{i}": True for i in range(1000)}

    t_small = timeit.timeit(lambda: core.verify_fleet_health(small_fleet), number=10000)
    t_mixed = timeit.timeit(lambda: core.verify_fleet_health(mixed_fleet), number=10000)
    t_large = timeit.timeit(lambda: core.verify_fleet_health(large_fleet), number=1000)


    print(f"Verify Health (Small 10): {t_small/10000 * 1e6:.2f} us")
    print(f"Verify Health (Mixed 100): {t_mixed/10000 * 1e6:.2f} us")
    print(f"Verify Health (Large 1000): {t_large/1000 * 1e6:.2f} us")


if __name__ == "__main__":
    benchmark_convergence()
