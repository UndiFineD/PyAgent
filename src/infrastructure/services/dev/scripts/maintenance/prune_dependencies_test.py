# Auto-synced test for infrastructure/services/dev/scripts/maintenance/prune_dependencies.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "prune_dependencies.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "prune_requirements"), "prune_requirements missing"

