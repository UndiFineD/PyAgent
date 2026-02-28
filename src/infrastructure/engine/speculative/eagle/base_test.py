# Auto-synced test for infrastructure/engine/speculative/eagle/base.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "InputBuffer"), "InputBuffer missing"
    assert hasattr(mod, "CpuGpuBuffer"), "CpuGpuBuffer missing"
    assert hasattr(mod, "AttentionMetadata"), "AttentionMetadata missing"
    assert hasattr(mod, "TreeAttentionMetadata"), "TreeAttentionMetadata missing"

