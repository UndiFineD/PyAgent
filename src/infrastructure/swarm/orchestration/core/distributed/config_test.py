# Auto-synced test for infrastructure/swarm/orchestration/core/distributed/config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EngineState"), "EngineState missing"
    assert hasattr(mod, "WorkerState"), "WorkerState missing"
    assert hasattr(mod, "LoadBalancingStrategy"), "LoadBalancingStrategy missing"
    assert hasattr(mod, "ParallelConfig"), "ParallelConfig missing"
    assert hasattr(mod, "EngineIdentity"), "EngineIdentity missing"
    assert hasattr(mod, "WorkerIdentity"), "WorkerIdentity missing"

