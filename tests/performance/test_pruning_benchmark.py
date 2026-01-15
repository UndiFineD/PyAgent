import timeit
from src.core.base.core.PruningCore import PruningCore, SynapticWeight
import time




def benchmark_pruning():
    core = PruningCore()

    # Measure calculate_decay
    def run_decay():
        core.calculate_decay(0.8, 3600.0, 3600.0)











    t_decay = timeit.timeit(run_decay, number=100000)
    print(f"calculate_decay: {t_decay/100000 * 1_000_000:.4f} μs per call")






    # Measure is_in_refractory
    weight = SynapticWeight("agent", 0.5, 0.0, refractory_until=time.time() + 100)
    def run_refractory():
        core.is_in_refractory(weight)






    t_ref = timeit.timeit(run_refractory, number=100000)
    print(f"is_in_refractory: {t_ref/100000 * 1_000_000:.4f} μs per call")

    # Measure update_weight_on_fire
    def run_update():





        core.update_weight_on_fire(0.5, True)

    t_update = timeit.timeit(run_update, number=100000)
    print(f"update_weight_on_fire: {t_update/100000 * 1_000_000:.4f} μs per call")






if __name__ == "__main__":
    benchmark_pruning()
