# Auto-synced test for core/base/common/utils/helpers.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "helpers.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "VERSION"), "VERSION missing"
    assert hasattr(mod, "requests"), "requests missing"
    assert hasattr(mod, "HAS_REQUESTS"), "HAS_REQUESTS missing"
    assert hasattr(mod, "HAS_TQDM"), "HAS_TQDM missing"
    assert hasattr(mod, "tqdm"), "tqdm missing"

