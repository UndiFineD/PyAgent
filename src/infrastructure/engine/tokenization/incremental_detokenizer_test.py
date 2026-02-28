# Auto-synced test for infrastructure/engine/tokenization/incremental_detokenizer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "incremental_detokenizer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TokenizerLike"), "TokenizerLike missing"
    assert hasattr(mod, "DetokenizeResult"), "DetokenizeResult missing"
    assert hasattr(mod, "StopChecker"), "StopChecker missing"
    assert hasattr(mod, "IncrementalDetokenizer"), "IncrementalDetokenizer missing"
    assert hasattr(mod, "FastIncrementalDetokenizer"), "FastIncrementalDetokenizer missing"
    assert hasattr(mod, "SlowIncrementalDetokenizer"), "SlowIncrementalDetokenizer missing"
    assert hasattr(mod, "create_detokenizer"), "create_detokenizer missing"
    assert hasattr(mod, "detokenize_incrementally"), "detokenize_incrementally missing"

