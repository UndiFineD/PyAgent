# Auto-synced test for infrastructure/services/executor/multiproc/types.py
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
    assert hasattr(mod, "ExecutorBackend"), "ExecutorBackend missing"
    assert hasattr(mod, "WorkerState"), "WorkerState missing"
    assert hasattr(mod, "WorkerInfo"), "WorkerInfo missing"
    assert hasattr(mod, "TaskMessage"), "TaskMessage missing"
    assert hasattr(mod, "ResultMessage"), "ResultMessage missing"

