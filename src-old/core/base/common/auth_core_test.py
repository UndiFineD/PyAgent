# Auto-synced test for core/base/common/auth_core.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically load the module under test to ensure it can be imported without errors."""
    p = pathlib.Path(__file__).parent / "auth_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise RuntimeError(f"Failed to create module spec for {p}")
    if spec.loader is None:
        raise RuntimeError(f"Failed to get loader for {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that auth_core.py can be imported and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "AuthProof"), "AuthProof missing"
    assert hasattr(mod, "AuthCore"), "AuthCore missing"
