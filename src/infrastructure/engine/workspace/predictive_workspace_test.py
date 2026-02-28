# Auto-synced test for infrastructure/engine/workspace/predictive_workspace.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "predictive_workspace.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "PredictiveWorkspace"), "PredictiveWorkspace missing"

