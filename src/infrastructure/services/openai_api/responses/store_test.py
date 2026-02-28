# Auto-synced test for infrastructure/services/openai_api/responses/store.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "store.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ResponseStore"), "ResponseStore missing"
    assert hasattr(mod, "InMemoryResponseStore"), "InMemoryResponseStore missing"

