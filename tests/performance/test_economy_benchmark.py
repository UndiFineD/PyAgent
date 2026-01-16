import time
import random
from src.infrastructure.fleet.core.EconomyCore import EconomyCore


def test_economy_benchmark():
    # Setup
    size = 1_000_000
    credits = [random.uniform(10, 1000) for _ in range(size)]
    importance = [random.random() for _ in range(size)]
    urgency = [random.random() for _ in range(size)]

    # Benchmark Priority Calculation loop
    start = time.perf_counter()

    priorities = []
    for c, i, u in zip(credits, importance, urgency):
        priorities.append(EconomyCore.calculate_bid_priority(c, i, u))
    duration_prio = (time.perf_counter() - start) * 1000

    print(f"Economy Prio Calc (N={size}): {duration_prio:.4f} ms")

    # Benchmark Surcharge
    vram = [random.uniform(4, 24) for _ in range(size)]

    util = [random.random() for _ in range(size)]

    start = time.perf_counter()
    surcharges = []
    for v, u in zip(vram, util):
        surcharges.append(EconomyCore.calculate_gpu_surcharge(v, u))
    duration_sur = (time.perf_counter() - start) * 1000

    print(f"Economy Surcharge Calc (N={size}): {duration_sur:.4f} ms")


if __name__ == "__main__":
    test_economy_benchmark()
