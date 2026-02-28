# Auto-synced test for infrastructure/engine/attention/backend/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AttentionBackendEnum"), "AttentionBackendEnum missing"
    assert hasattr(mod, "AttentionType"), "AttentionType missing"
    assert hasattr(mod, "AttentionCapabilities"), "AttentionCapabilities missing"
    assert hasattr(mod, "AttentionMetadata"), "AttentionMetadata missing"

