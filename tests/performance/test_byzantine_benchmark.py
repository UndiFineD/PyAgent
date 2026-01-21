import timeit
import random
from src.logic.agents.security.core.byzantine_core import ByzantineCore


def benchmark_byzantine():
    core = ByzantineCore()

    # Setup
    votes_small = [
        {"weight": random.random(), "hash": random.choice(["a", "b", "c"])}
        for _ in range(10)
    ]
    votes_large = [
        {"weight": random.random(), "hash": random.choice(["a", "b", "c"])}
        for _ in range(1000)
    ]

    agents_reliability = {f"agent_{i}": random.random() for i in range(100)}

    t_score_small = timeit.timeit(
        lambda: core.calculate_agreement_score(votes_small), number=10000
    )
    t_score_large = timeit.timeit(
        lambda: core.calculate_agreement_score(votes_large), number=1000
    )

    t_comm = timeit.timeit(
        lambda: core.select_committee(agents_reliability), number=1000
    )

    print(f"Agreement Score (Small 10): {t_score_small / 10000 * 1e6:.2f} us")
    print(f"Agreement Score (Large 1000): {t_score_large / 1000 * 1e6:.2f} us")
    print(f"Select Committee (100 agents): {t_comm / 1000 * 1e6:.2f} us")


if __name__ == "__main__":
    benchmark_byzantine()
