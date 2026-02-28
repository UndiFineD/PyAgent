# Auto-synced test for infrastructure/engine/engine_client/types.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "types.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ClientMode"), "ClientMode missing"
    assert hasattr(mod, "WorkerState"), "WorkerState missing"
    assert hasattr(mod, "EngineClientConfig"), "EngineClientConfig missing"
    assert hasattr(mod, "SchedulerOutput"), "SchedulerOutput missing"
    assert hasattr(mod, "EngineOutput"), "EngineOutput missing"
    assert hasattr(mod, "WorkerInfo"), "WorkerInfo missing"

