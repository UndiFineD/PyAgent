# Auto-synced test for infrastructure/engine/inference/decoder/proposers.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "proposers.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DraftProposer"), "DraftProposer missing"
    assert hasattr(mod, "NgramProposer"), "NgramProposer missing"
    assert hasattr(mod, "SuffixNode"), "SuffixNode missing"
    assert hasattr(mod, "SuffixProposer"), "SuffixProposer missing"
    assert hasattr(mod, "ngram_match"), "ngram_match missing"

