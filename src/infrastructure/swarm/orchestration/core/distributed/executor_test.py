# Auto-synced test for infrastructure/swarm/orchestration/core/distributed/executor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "executor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DistributedExecutor"), "DistributedExecutor missing"
    assert hasattr(mod, "MultiProcessExecutor"), "MultiProcessExecutor missing"
    assert hasattr(mod, "create_distributed_executor"), "create_distributed_executor missing"
    assert hasattr(mod, "get_dp_rank"), "get_dp_rank missing"
    assert hasattr(mod, "get_dp_size"), "get_dp_size missing"
    assert hasattr(mod, "get_tp_rank"), "get_tp_rank missing"
    assert hasattr(mod, "get_tp_size"), "get_tp_size missing"

