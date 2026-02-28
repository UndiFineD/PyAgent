# Auto-synced test for infrastructure/swarm/distributed/tensor_parallel_group.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "tensor_parallel_group.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ParallelConfig"), "ParallelConfig missing"
    assert hasattr(mod, "RankInfo"), "RankInfo missing"
    assert hasattr(mod, "ParallelMode"), "ParallelMode missing"
    assert hasattr(mod, "GroupCoordinator"), "GroupCoordinator missing"
    assert hasattr(mod, "TensorParallelGroup"), "TensorParallelGroup missing"
    assert hasattr(mod, "init_distributed"), "init_distributed missing"
    assert hasattr(mod, "get_tp_group"), "get_tp_group missing"
    assert hasattr(mod, "get_tp_size"), "get_tp_size missing"
    assert hasattr(mod, "get_tp_rank"), "get_tp_rank missing"

