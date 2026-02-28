# Auto-synced test for infrastructure/engine/speculative/ngram_proposer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "ngram_proposer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "NgramConfig"), "NgramConfig missing"
    assert hasattr(mod, "NgramMatch"), "NgramMatch missing"
    assert hasattr(mod, "NgramProposalResult"), "NgramProposalResult missing"
    assert hasattr(mod, "NgramCache"), "NgramCache missing"
    assert hasattr(mod, "NgramProposer"), "NgramProposer missing"
    assert hasattr(mod, "WeightedNgramProposer"), "WeightedNgramProposer missing"
    assert hasattr(mod, "PromptLookupProposer"), "PromptLookupProposer missing"
    assert hasattr(mod, "HybridNgramProposer"), "HybridNgramProposer missing"
    assert hasattr(mod, "NgramProposerFactory"), "NgramProposerFactory missing"

