# Auto-synced test for infrastructure/engine/scheduling/disaggregated/selectors.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "selectors.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "InstanceSelector"), "InstanceSelector missing"
    assert hasattr(mod, "RoundRobinSelector"), "RoundRobinSelector missing"
    assert hasattr(mod, "LeastLoadedSelector"), "LeastLoadedSelector missing"
    assert hasattr(mod, "RandomSelector"), "RandomSelector missing"
    assert hasattr(mod, "HashSelector"), "HashSelector missing"

