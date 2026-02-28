# Auto-synced test for infrastructure/engine/incremental_detokenizer.py
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
    assert hasattr(mod, "StopMatch"), "StopMatch missing"
    assert hasattr(mod, "check_stop_strings"), "check_stop_strings missing"
    assert hasattr(mod, "check_stop_strings_rust"), "check_stop_strings_rust missing"
    assert hasattr(mod, "IncrementalDetokenizer"), "IncrementalDetokenizer missing"
    assert hasattr(mod, "NoOpDetokenizer"), "NoOpDetokenizer missing"
    assert hasattr(mod, "BaseIncrementalDetokenizer"), "BaseIncrementalDetokenizer missing"
    assert hasattr(mod, "FastIncrementalDetokenizer"), "FastIncrementalDetokenizer missing"
    assert hasattr(mod, "SlowIncrementalDetokenizer"), "SlowIncrementalDetokenizer missing"
    assert hasattr(mod, "validate_utf8"), "validate_utf8 missing"
    assert hasattr(mod, "validate_utf8_rust"), "validate_utf8_rust missing"
    assert hasattr(mod, "INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET"), "INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET missing"

