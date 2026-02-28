# Auto-synced test for infrastructure/engine/tokenization/utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "get_tokenizer"), "get_tokenizer missing"
    assert hasattr(mod, "create_tokenizer"), "create_tokenizer missing"
    assert hasattr(mod, "estimate_token_count"), "estimate_token_count missing"
    assert hasattr(mod, "detect_tokenizer_backend"), "detect_tokenizer_backend missing"

