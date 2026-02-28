# Auto-synced test for core/base/common/utils/lazy_loader.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lazy_loader.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LazyModule"), "LazyModule missing"
    assert hasattr(mod, "LazyImport"), "LazyImport missing"
    assert hasattr(mod, "DeferredImport"), "DeferredImport missing"
    assert hasattr(mod, "lazy_import"), "lazy_import missing"
    assert hasattr(mod, "optional_import"), "optional_import missing"
    assert hasattr(mod, "require_import"), "require_import missing"

