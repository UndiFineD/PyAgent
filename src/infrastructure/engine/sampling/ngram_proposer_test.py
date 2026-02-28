# Auto-synced test for infrastructure/engine/sampling/ngram_proposer.py
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
    assert hasattr(mod, "MatchingStrategy"), "MatchingStrategy missing"
    assert hasattr(mod, "NgramConfig"), "NgramConfig missing"
    assert hasattr(mod, "ProposalStats"), "ProposalStats missing"
    assert hasattr(mod, "SuffixIndex"), "SuffixIndex missing"
    assert hasattr(mod, "NgramProposer"), "NgramProposer missing"
    assert hasattr(mod, "AdaptiveNgramProposer"), "AdaptiveNgramProposer missing"
    assert hasattr(mod, "SuffixTreeProposer"), "SuffixTreeProposer missing"
    assert hasattr(mod, "create_ngram_proposer"), "create_ngram_proposer missing"

