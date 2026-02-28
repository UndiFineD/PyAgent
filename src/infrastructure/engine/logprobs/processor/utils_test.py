# Auto-synced test for infrastructure/engine/logprobs/processor/utils.py
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
    assert hasattr(mod, "compute_perplexity"), "compute_perplexity missing"
    assert hasattr(mod, "compute_entropy"), "compute_entropy missing"
    assert hasattr(mod, "normalize_logprobs"), "normalize_logprobs missing"

