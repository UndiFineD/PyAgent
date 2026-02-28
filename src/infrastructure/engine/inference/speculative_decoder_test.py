# Auto-synced test for infrastructure/engine/inference/speculative_decoder.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "speculative_decoder.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SpecMethod"), "SpecMethod missing"
    assert hasattr(mod, "SpeculativeConfig"), "SpeculativeConfig missing"
    assert hasattr(mod, "DraftProposal"), "DraftProposal missing"
    assert hasattr(mod, "VerificationResult"), "VerificationResult missing"
    assert hasattr(mod, "SpecDecodingMetrics"), "SpecDecodingMetrics missing"
    assert hasattr(mod, "DraftProposer"), "DraftProposer missing"
    assert hasattr(mod, "NgramProposer"), "NgramProposer missing"
    assert hasattr(mod, "SuffixProposer"), "SuffixProposer missing"
    assert hasattr(mod, "TreeSpeculator"), "TreeSpeculator missing"
    assert hasattr(mod, "SpeculativeDecoder"), "SpeculativeDecoder missing"
    assert hasattr(mod, "create_speculative_decoder"), "create_speculative_decoder missing"

