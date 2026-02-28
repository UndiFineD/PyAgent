# Auto-synced test for infrastructure/engine/speculative/spec_decode_metadata_v2.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "spec_decode_metadata_v2.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SpecDecodeConfig"), "SpecDecodeConfig missing"
    assert hasattr(mod, "VerificationStrategy"), "VerificationStrategy missing"
    assert hasattr(mod, "AcceptancePolicy"), "AcceptancePolicy missing"
    assert hasattr(mod, "SpecDecodeMetadataV2"), "SpecDecodeMetadataV2 missing"
    assert hasattr(mod, "TreeVerificationMetadata"), "TreeVerificationMetadata missing"
    assert hasattr(mod, "SpecDecodeMetadataFactory"), "SpecDecodeMetadataFactory missing"
    assert hasattr(mod, "VerificationResult"), "VerificationResult missing"
    assert hasattr(mod, "SpecDecodeVerifier"), "SpecDecodeVerifier missing"
    assert hasattr(mod, "BatchVerifier"), "BatchVerifier missing"
    assert hasattr(mod, "StreamingVerifier"), "StreamingVerifier missing"

