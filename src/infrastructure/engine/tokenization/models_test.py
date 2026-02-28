# Auto-synced test for infrastructure/engine/tokenization/models.py
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
    assert hasattr(mod, "TokenizerBackend"), "TokenizerBackend missing"
    assert hasattr(mod, "SpecialTokenHandling"), "SpecialTokenHandling missing"
    assert hasattr(mod, "TruncationStrategy"), "TruncationStrategy missing"
    assert hasattr(mod, "PaddingStrategy"), "PaddingStrategy missing"
    assert hasattr(mod, "TokenizerConfig"), "TokenizerConfig missing"
    assert hasattr(mod, "TokenizerInfo"), "TokenizerInfo missing"
    assert hasattr(mod, "TokenizeResult"), "TokenizeResult missing"
    assert hasattr(mod, "BatchTokenizeResult"), "BatchTokenizeResult missing"

