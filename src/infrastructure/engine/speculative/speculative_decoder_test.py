# Auto-synced test for infrastructure/engine/speculative/speculative_decoder.py
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
    assert hasattr(mod, "ProposerType"), "ProposerType missing"
    assert hasattr(mod, "AcceptanceMethod"), "AcceptanceMethod missing"
    assert hasattr(mod, "SpeculativeToken"), "SpeculativeToken missing"
    assert hasattr(mod, "SpeculativeTree"), "SpeculativeTree missing"
    assert hasattr(mod, "ProposerStats"), "ProposerStats missing"
    assert hasattr(mod, "SpeculativeProposer"), "SpeculativeProposer missing"
    assert hasattr(mod, "NgramProposer"), "NgramProposer missing"
    assert hasattr(mod, "MedusaProposer"), "MedusaProposer missing"
    assert hasattr(mod, "VerificationResult"), "VerificationResult missing"
    assert hasattr(mod, "SpeculativeVerifier"), "SpeculativeVerifier missing"
    assert hasattr(mod, "SpeculativeDecoder"), "SpeculativeDecoder missing"
    assert hasattr(mod, "create_ngram_decoder"), "create_ngram_decoder missing"
    assert hasattr(mod, "create_medusa_decoder"), "create_medusa_decoder missing"

