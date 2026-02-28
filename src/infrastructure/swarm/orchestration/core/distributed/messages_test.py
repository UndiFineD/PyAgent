# Auto-synced test for infrastructure/swarm/orchestration/core/distributed/messages.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "messages.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CoordinatorMessage"), "CoordinatorMessage missing"
    assert hasattr(mod, "RequestMessage"), "RequestMessage missing"
    assert hasattr(mod, "ResponseMessage"), "ResponseMessage missing"
    assert hasattr(mod, "ControlMessage"), "ControlMessage missing"
    assert hasattr(mod, "MetricsMessage"), "MetricsMessage missing"

