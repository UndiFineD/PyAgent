# Auto-synced test for infrastructure/swarm/parallel/data_parallel_coordinator.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "data_parallel_coordinator.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DPRole"), "DPRole missing"
    assert hasattr(mod, "WorkerHealth"), "WorkerHealth missing"
    assert hasattr(mod, "LoadBalanceStrategy"), "LoadBalanceStrategy missing"
    assert hasattr(mod, "DPConfig"), "DPConfig missing"
    assert hasattr(mod, "WorkerState"), "WorkerState missing"
    assert hasattr(mod, "StepState"), "StepState missing"
    assert hasattr(mod, "WaveState"), "WaveState missing"
    assert hasattr(mod, "P2CLoadBalancer"), "P2CLoadBalancer missing"
    assert hasattr(mod, "DPEngineCoreProc"), "DPEngineCoreProc missing"
    assert hasattr(mod, "HierarchicalDPCoordinator"), "HierarchicalDPCoordinator missing"
    assert hasattr(mod, "dp_collective_all_reduce"), "dp_collective_all_reduce missing"

