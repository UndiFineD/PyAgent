# Auto-synced test for inference/execution/model_runner/runner.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "runner.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AsyncModelRunner"), "AsyncModelRunner missing"

